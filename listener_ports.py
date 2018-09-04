import socket
import sys
import pyaudio
import numpy as np
import random

# this is a server application to listen for sound messages from the switch. the switch should send a message containing a port number and this will play a sound at the frequency associated wiht the port number.
# it maps frequencies 200-16050 to ports 8600-8916 (it uses frequencies that are 50 hz apart)

def initstream():
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paFloat32,
			channels=1,
			rate=44100,
			output=True)
	stream.start_stream()
	return stream

def gensample(f):
	volume = 1.0     # range [0.0, 1.0]
        fs = 44100       # sampling rate, Hz, must be integer
        duration = .1   # in seconds, may be float
	return (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)


HOST = ''
PORT = 8888

freqs = np.arange(200,16050,50)
ports = np.arange(8600,8917,1)
#random.shuffle(ports)
mappings = dict(zip(ports,freqs))

stream = initstream()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
	s.bind((HOST,PORT))
except socket.error as msg:
	print msg
	sys.exit()

s.listen(10)
pkts = 0
while True:
	connection,client_address = s.accept()
	#print "connected"
	while True:
		data = connection.recv(20)
		if data:
			print data
			d = data.split(",")
                        src = int(d[0])
                        dst = int(d[1])
			if dst == 0:
				connection.close()
				break	
			pkts += 1
			if pkts > 0:
			#if pkts%5 == 0:
				#stream.start_stream()
				if src in ports:
					stream.write(gensample(mappings[src]))
				if dst in ports:
					stream.write(gensample(mappings[dst]))
				#stream.stop_stream()
			connection.close()
			break


