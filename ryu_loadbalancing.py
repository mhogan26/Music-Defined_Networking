from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import dpid as dpid_lib
from ryu.lib import stplib
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet, ether_types
from ryu.app import simple_switch_13
from ryu.lib import hub

from ryu.topology import event, switches
from ryu.topology.api import get_switch, get_link, get_host
import networkx as nx
import thread
import time
import pyaudio
import numpy as np
import struct
import scipy
from scipy.fftpack import fft, fftfreq
import socket

# ryu controller to update openflow rules when the mininet queue is too congested (listener_loadbalancing sends a message when it hears the queue is congested)
# the listening logic MUST NOT BE IN THE CONTROLLER (which is why there's the listener_loadbalancing code) because it causes problems with the controller
# it load balances by adding an openflow group with multiple rules forwarding rules (sends traffic along 2 different paths)
# this is specific to a diamond topology with four switches (1-2, 2-4, 1-3, 3-4) with hosts attached to switches 1 and 4


class SimpleSwitch13(simple_switch_13.SimpleSwitch13):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {'stplib': stplib.Stp}

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.stp = kwargs['stplib']

	self.topology_api_app = self
        self.net = nx.DiGraph()
        self.links = {}
	
	self.host_to_switch = {}
	
	self.datapaths = {}

        self.switches = []

	self.new_path = []

        self.paths = {}

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        thread.start_new_thread(self.get_links)

        thread.start_new_thread(self.monitor)

        #thread.start_new_thread(self.dpaths)

        # Sample of stplib config.
        #  please refer to stplib.Stp.set_config() for details.
        config = {dpid_lib.str_to_dpid('0000000000000001'):
                  {'bridge': {'priority': 0x8000}},
                  dpid_lib.str_to_dpid('0000000000000002'):
                  {'bridge': {'priority': 0x9000}},
                  dpid_lib.str_to_dpid('0000000000000003'):
                  {'bridge': {'priority': 0xa000}}}
        self.stp.set_config(config)
	
    def delete_flow(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        for dst in self.mac_to_port[datapath.id].keys():
            match = parser.OFPMatch(eth_dst=dst)
            mod = parser.OFPFlowMod(
                datapath, command=ofproto.OFPFC_DELETE,
                out_port=ofproto.OFPP_ANY, out_group=ofproto.OFPG_ANY,
                priority=1, match=match)
            datapath.send_msg(mod)
   


    def delete_existing_flows(self, d_id, match):  
	datapath = self.datapaths[int(d_id)]
        ofproto = datapath.ofproto
        ofp_parser=datapath.ofproto_parser
        mod = ofp_parser.OFPFlowMod(
        datapath, command=ofproto.OFPFC_DELETE,
        out_port=ofproto.OFPP_ANY, out_group=ofproto.OFPG_ANY,
                priority=1, match=match)
        datapath.send_msg(mod)


    def mod_flow_msg(self,datapath, act, m):
    #def mod_flow_msg(self,datapath, act, dst):
    	ofp = datapath.ofproto
    	ofp_parser = datapath.ofproto_parser

    	#cookie = cookie_mask = 0
    	#table_id = 0
    	#idle_timeout = hard_timeout = 0
    	#priority = 1
    	#buffer_id = ofp.OFP_NO_BUFFER
    	#match = ofp_parser.OFPMatch(eth_dst=dst)
    	actions = act
	inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                             actions)]
    	req = ofp_parser.OFPFlowMod(datapath=datapath,command=ofp.OFPFC_ADD,
                                priority=1, match=m, instructions=inst)
    	datapath.send_msg(req)

			
    @set_ev_cls(stplib.EventPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
	msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

	#ignore LLDP packets	
	if eth.ethertype == ether_types.ETH_TYPE_LLDP:
		return

        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        #self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]


        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            #match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            match = parser.OFPMatch(eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

        #MOVE???
        host_list = get_host(self.topology_api_app, None)
	for host in host_list:
		if host not in self.host_to_switch:
			self.host_to_switch[host.port.dpid] = [host.mac,host.port.port_no]

    @set_ev_cls(stplib.EventTopologyChange, MAIN_DISPATCHER)
    def _topology_change_handler(self, ev):
        dp = ev.dp
        dpid_str = dpid_lib.dpid_to_str(dp.id)
        msg = 'Receive topology change event. Flush MAC table.'
        self.logger.debug("[dpid=%s] %s", dpid_str, msg)

        if dp.id in self.mac_to_port:
            self.delete_flow(dp)
            del self.mac_to_port[dp.id]

    @set_ev_cls(stplib.EventPortStateChange, MAIN_DISPATCHER)
    def _port_state_change_handler(self, ev):
        dpid_str = dpid_lib.dpid_to_str(ev.dp.id)
        of_state = {stplib.PORT_STATE_DISABLE: 'DISABLE',
                    stplib.PORT_STATE_BLOCK: 'BLOCK',
                    stplib.PORT_STATE_LISTEN: 'LISTEN',
                    stplib.PORT_STATE_LEARN: 'LEARN',
                    stplib.PORT_STATE_FORWARD: 'FORWARD'}
        self.logger.debug("[dpid=%s][port=%d] state=%s",
                          dpid_str, ev.port_no, of_state[ev.port_state])


    @set_ev_cls(event.EventSwitchEnter)
    def _get_topology_data(self,ev):
        switch_list = get_switch(self.topology_api_app, None)
        if len(self.switches) < 1:
            self.switches=[switch.dp.id for switch in switch_list]


    def get_links(self):
        while 1:
            links_list = get_link(self.topology_api_app, None)
            if len(links_list) > -1:
                for link in links_list:
                    print (link.src.dpid,link.dst.dpid,{'port':link.src.port_no}) 
                links = [(link.src.dpid,link.dst.dpid,{'port':link.src.port_no}) for link in links_list]
                self.net.add_edges_from(links)
                links = [(link.dst.dpid,link.src.dpid,{'port':link.dst.port_no}) for link in links_list]
                self.net.add_edges_from(links)
                print self.net.nodes()
                #self.get_spec_paths()
                break
            time.sleep(.5)



    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
	datapath = ev.datapath
	if ev.state == MAIN_DISPATCHER:
		if not datapath.id in self.datapaths:
			self.datapaths[datapath.id] = datapath
	elif ev.state == DEAD_DISPATCHER:
		if datapath.id in self.datapaths:
			del self.datapaths[datapath.id]
    

    def get_spec_paths(self):
        self.paths[(1,4)] = []
        self.paths[(4,1)] = []
        for path in nx.all_simple_paths(self.net,1,4):   
            if path not in self.paths[(1,4)]:
                self.paths[(1,4)].append(path)
        for path in nx.all_simple_paths(self.net,4,1):
            if path not in self.paths[(4,1)]:
                self.paths[(4,1)].append(path)
 
        print self.paths

    def get_all_paths(self):
        for src in self.net.nodes():
            for dst in self.net.nodes():
                if src is not dst:
                    if (src,dst) not in self.paths.keys():
                        if (dst,src) not in self.paths.keys():
                            self.paths[(src,dst)] = []
                            k = (src,dst)
                        else:
                            k = (dst,src)
                    else:
                        k = (src,dst)
                    for path in nx.all_simple_paths(self.net,src,dst):
                        if path not in self.paths[k]:
                            self.paths[k].append(path)
        print self.paths



    def balance(self):
        print "LOAD BALANCE"
        #1 - 2 - 4
        #1 - 3 - 4
        #path1 = self.paths[(1,4)][0]
        #path2 = self.paths[(1,4)][1]
        #host1 = self.host_to_switch[4][0] 
        #host2 = self.host_to_switch[1][0]
        host1 = 'b6:9e:a5:04:5e:15'
        host2 = '46:a3:c2:bf:7b:cf'
        host3 = '6e:43:ea:28:fe:be'
        host4 = 'fe:ab:11:32:d4:b7'
        #host5 = '9e:68:84:07:1c:18'

        svals = [3,2,4,1]
        for s in svals:
            d = self.datapaths[s]
            ofp = d.ofproto
            if s == 1:
                ofproto = d.ofproto
                parser = d.ofproto_parser
                #m1 = parser.OFPMatch(eth_dst=host1)
                m2 = parser.OFPMatch(eth_dst=host2)
                m4 = parser.OFPMatch(eth_dst=host4)
                #print self.net
                #outport1 = self.net[s][2]['port']
                #outport2 = self.net[s][3]['port']
                outport1 = 3
                outport2 = 4
                # add group msg
                group_id = 2
                buckets = []
                bucket_weight = 5
                bucket_action1 = [parser.OFPActionOutput(outport1)]
                bucket_action2 = [parser.OFPActionOutput(outport2)]
                buckets.append(
                    parser.OFPBucket(
                        weight=5,
                        watch_port=outport1,
                        watch_group=2,
                        actions=bucket_action1
                    )
                )
                buckets.append(
                    parser.OFPBucket(
                        weight=5,
                        watch_port=outport2,
                        watch_group=2,
                        actions=bucket_action2
                    )
                )

                req = parser.OFPGroupMod(
                    d, ofp.OFPGC_ADD, ofp.OFPGT_SELECT,
                    group_id, buckets)
                d.send_msg(req)
                actions = [parser.OFPActionGroup(group_id)]
                self.mod_flow_msg(d,actions,m2)
                #self.mod_flow_msg(d,actions,m4)


            if s == 2:	#NO CHANGES, STILL FORWARDING TRAFFIC THE SAME WAY, assuming this is the default path
                #outport1 = self.net[s][4]['port']
                #outport2 = self.net[2][1]['port']
                outport1 = 2
                outport2 = 1
                # regular add flow messages
                #print "2: outport1 = {}, outport2 = {}".format(outport1,outport2)
                ofproto = d.ofproto
                parser = d.ofproto_parser
                m1 = parser.OFPMatch(eth_dst=host2)
                m2 = parser.OFPMatch(eth_dst=host1)
                a1 = [parser.OFPActionOutput(outport1)]
                a2 = [parser.OFPActionOutput(outport2)]
                #self.add_flow(d,65535,m1,a1)
                #self.add_flow(d,65535,m2,a2)


            if s == 3:
                #outport1 = self.net[s][4]['port']
                #outport2 = self.net[3][1]['port']
                outport1 = 2
                outport2 = 1
                # regular add flow messages
                #print "3: outport1 = {}, outport2 = {}".format(outport1,outport2)
                ofproto = d.ofproto
                parser = d.ofproto_parser
                m1 = parser.OFPMatch(eth_dst=host2)
                m2 = parser.OFPMatch(eth_dst=host1)
                a1 = [parser.OFPActionOutput(outport1)]
                a2 = [parser.OFPActionOutput(outport2)]
                self.add_flow(d,65535,m1,a1)
                self.add_flow(d,65535,m2,a2)


            if s == 4:
                ofproto = d.ofproto
                parser = d.ofproto_parser
                m1 = parser.OFPMatch(eth_dst=host1)
                m2 = parser.OFPMatch(eth_dst=host2)
                #outport1 = self.net[4][2]['port']
                #outport2 = self.net[4][3]['port']
                outport1 = 2
                outport2 = 3
                # delete existing flows
                self.delete_existing_flows(4,parser.OFPMatch(in_port=3))
                #hport = self.host_to_switch[4][1]
                hport = 4
                a2 = [parser.OFPActionOutput(hport)]
                #print "4: outport1 = {}, outport2 = {}, hostport = {}".format(outport1, outport2, self.host_to_switch[4][1])
                #self.add_flow(d,65535,m2,a2)
                # add group msg
                group_id = 4
                buckets = []
                bucket_weight = 5
                bucket_action1 = [parser.OFPActionOutput(outport1)]
                bucket_action2 = [parser.OFPActionOutput(outport2)]
                buckets.append(
                    parser.OFPBucket(
                        weight=5,
                        watch_port=outport1,
                        watch_group=4,
                        actions=bucket_action1
                    )
                )
                buckets.append(
                    parser.OFPBucket(
                        weight=5,
                        watch_port=outport2,
                        watch_group=ofp.OFPG_ANY,
                        actions=bucket_action2
                    )
                )
  
                req = parser.OFPGroupMod(
                    d, ofp.OFPGC_ADD, ofp.OFPGT_SELECT,
                    group_id, buckets)
                d.send_msg(req)
                actions = [parser.OFPActionGroup(group_id)]
                #self.add_flow(d, 65535, m1, actions)
                #self.mod_flow_msg(d,actions,m1)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)


    def dpaths(self):
        host1 = 'b6:9e:a5:04:5e:15'
        host2 = '46:a3:c2:bf:7b:cf'
        host3 = '6e:43:ea:28:fe:be'
        host4 = 'fe:ab:11:32:d4:b7'
        while 1:
            if len(self.datapaths.keys()) > 3:
                svals = [1,2,3,4]
                for s in svals:
                    d = self.datapaths[s]
                    ofproto = d.ofproto
                    parser = d.ofproto_parser
                    m1 = parser.OFPMatch(eth_dst=host1)
                    m2 = parser.OFPMatch(eth_dst=host2)
                    m3 = parser.OFPMatch(eth_dst=host3)
                    m4 = parser.OFPMatch(eth_dst=host4)

                    if s == 1:
                        h1port = 1
                        h3port = 2
                        h24port = 3 # going out to s2
                        a1 = [parser.OFPActionOutput(h1port)]
                        a3 = [parser.OFPActionOutput(h3port)]
                        a24 = [parser.OFPActionOutput(h24port)]
                        self.add_flow(d,65535,m1,a1)
                        self.add_flow(d,65535,m3,a3)
                        self.add_flow(d,65535,m2,a24)
                        self.add_flow(d,65535,m4,a24)

                    if s == 2:
                        h24port = 2 # going out to s4 
                        h13port = 1 # going out to s1
                        a24 = [parser.OFPActionOutput(h24port)]
                        a13 = [parser.OFPActionOutput(h13port)]
                        self.add_flow(d,65535,m1,a13)
                        self.add_flow(d,65535,m2,a24)
                        self.add_flow(d,65535,m3,a13)
                        self.add_flow(d,65535,m4,a24)

                    if s == 3:
                        h24port = 2 # going out to s4 
                        h13port = 1 # going out to s1
                    if s == 4:
                        h2port = 1
                        h4port = 4
                        h13port = 2 # going out to s2
                        a2 = [parser.OFPActionOutput(h2port)]
                        a4 = [parser.OFPActionOutput(h4port)]
                        a13 = [parser.OFPActionOutput(h13port)]
                        self.add_flow(d,65535,m1,a13)
                        self.add_flow(d,65535,m2,a2)
                        self.add_flow(d,65535,m3,a13)
                        self.add_flow(d,65535,m4,a4)


                break

            time.sleep(1)



    def monitor(self):
        balanced = False
        self.s.bind(('127.0.0.1',10000))
        self.s.listen(10)
        while True:
            connection,client_address = self.s.accept()
            while True:
                print "received"
                data = connection.recv(400)
                if 'b' in data and not balanced:
                    print "balance"
                    self.balance()
                    balanced = True


