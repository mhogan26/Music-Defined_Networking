#!/usr/bin/env python
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link,TCLink,Intf
from mininet.node import RemoteController

# creates diamond topo in mininet
# 4 hosts total, two attached to s1 and two attached to s4 

if '__main__' == __name__:

  net = Mininet(link=TCLink)

  h1 = net.addHost('h1', mac='b6:9e:a5:04:5e:15')

  h2 = net.addHost('h2', mac='46:a3:c2:bf:7b:cf')

  h3 = net.addHost('h3', mac='6e:43:ea:28:fe:be')

  h4 = net.addHost('h4', mac='fe:ab:11:32:d4:b7')

  #h5 = net.addHost('h5', mac='9e:68:84:07:1c:18')

  s1 = net.addSwitch('s1')

  s2 = net.addSwitch('s2')

  s3 = net.addSwitch('s3')

  s4 = net.addSwitch('s4')


  c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

  linkopts0=dict(bw=20, delay='1ms', loss=0, max_queue_size=20, use_tbf=True)

  linkopts1=dict(bw=5, loss=0, max_queue_size=100, use_tbf=True)

  linkopts2=dict(bw=5, delay='1ms', loss=0, max_queue_size=100, use_tbf=True)

  linkopts3=dict(bw=5, delay='1ms', loss=0, max_queue_size=100, use_tbf=True)

  linkopts4=dict(bw=5, delay='1ms', loss=0, max_queue_size=100, use_tbf=True)

  #linkopts5=dict(bw=5, delay='1ms', loss=0, max_queue_size=100, use_tbf=True)


  net.addLink(h1, s1, cls=TCLink, **linkopts0)

  net.addLink(h3, s1, cls=TCLink, **linkopts0)

  net.addLink(h4, s4, cls=TCLink, **linkopts0)

  #net.addLink(h5, s1, cls=TCLink, **linkopts0)

  net.addLink(s1, s2, cls=TCLink, **linkopts1)
  
  net.addLink(s1, s3, cls=TCLink, **linkopts2)

  net.addLink(s2, s4, cls=TCLink, **linkopts3)

  net.addLink(s3, s4, cls=TCLink, **linkopts4)

  net.addLink(s4, h2, cls=TCLink, **linkopts0)

  net.build()

  c0.start()

  s1.start([c0])

  s2.start([c0])

  s3.start([c0])

  s4.start([c0])

  CLI(net)

  net.stop()
