import time
import pyaudio
import numpy as np
import struct
import scipy
from scipy.fftpack import fft, fftfreq
import socket
import wave

# this listens to sounds for a given number of seconds (INPUT_BLOCK_TIME)
# if the sound is louder than THRESHOLD, it computes the fft of the sound and determines how loud each frequency is
# (this is listening for 600hz, 700hz, 800hz, and 900hz)
# if the frequency is at least as loud as thresh, that means the sound played is that frequency 
# this is currently commented out, but if it hears 800hz (corresponding to highest queue size), it sends a message to the controller to update the openflow rules to balance the flow

THRESHOLD = 30 # dB
RATE = 48000
INPUT_BLOCK_TIME = 0.05 #  ms
INPUT_FRAMES_PER_BLOCK = int(RATE * INPUT_BLOCK_TIME)
#INPUT_FRAMES_PER_BLOCK = 1024

def find_input_device(pa):
	device_index = None
	for i in range(pa.get_device_count()):
		devinfo = pa.get_device_info_by_index(i)
		if 'USB' in devinfo['name']:
			device_index = i
			break
		else:
			continue
	return device_index

def get_rms(block):
	return np.sqrt(np.mean(np.square(block)))



def listen():
	'''
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
                s.connect(('127.0.0.1',10000))
        except Exception as e:
                print "failed"
	'''

	#frames = []
        pa = pyaudio.PyAudio()
	device_index = find_input_device(pa)
	stream = pa.open(  format = pyaudio.paInt16,
				channels = 1,
				rate = RATE,
				input = True,
				input_device_index = device_index,
				frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

	balanced = False
	scount = 0
	while True:
	#for i in range(0,30):
		stream.start_stream()
		readstream = time.time()
		try:
			frames = ""
			for i in range(0,int(RATE / INPUT_FRAMES_PER_BLOCK * INPUT_BLOCK_TIME)):
				raw_block = stream.read(INPUT_FRAMES_PER_BLOCK, exception_on_overflow = False)
				frames = frames+raw_block
			count = len(frames) / 2
			format = '%dh' % (count)
			snd_block = np.array(struct.unpack(format, frames))
			stream.stop_stream()
		except Exception as e:
			break
		amplitude = get_rms(snd_block)
		knowamplitude = time.time()
		if amplitude > THRESHOLD:
			#print 1000*(knowamplitude-readstream)
			heardsound = time.time()
			#stream.stop_stream()
			w = fft(snd_block)
			fftdone = time.time()
			freqs = fftfreq(w.size)
			fftfreqsdone = time.time()
			#freq_in_hertz = [int(x) for x in map(lambda x: x*RATE,freqs)]
			afterhzconv = time.time()
                        print np.abs(w)[30]
			thresh = 175000
			recognizesound = 0
			#stream.start_stream()
			if np.abs(w)[30] > thresh:
			#if np.abs(w)[freq_in_hertz.index(600)] > thresh:
				recognizesound = time.time()
				#print freq_in_hertz.index(500)	
				#s.send("n")
				#stream.stop_stream()
				scount += 1
				#print scount
				print 1000*(knowamplitude-readstream)
				print "readstream {0:.16f}, heardsound {1:.16f}, fftdone {2:.16f}, fftfreqsdone {3:.16f}, afterhzconv {4:.16f}, recognizesound {5:.16f}, count {6}, sound 600, magnitude {7}".format(readstream, heardsound, fftdone, fftfreqsdone, afterhzconv, recognizesound, scount, np.abs(w)[30])
				#stream.start_stream()

			if np.abs(w)[35] > thresh:
			#if np.abs(w)[freq_in_hertz.index(700)] > thresh:	
				#s.send("n")
				recognizesound = time.time()
				#stream.stop_stream()
				scount += 1
				print "readstream {0:.16f}, heardsound {1:.16f}, fftdone {2:.16f}, fftfreqsdone {3:.16f}, afterhzconv {4:.16f}, recognizesound {5:.16f}, count {6}, sound 700, magnitude {7}".format(readstream, heardsound, fftdone, fftfreqsdone, afterhzconv, recognizesound, scount, np.abs(w)[35])
				#stream.start_stream()

			if np.abs(w)[40] > (thresh + 50000):
			#if np.abs(w)[freq_in_hertz.index(800)] > thresh:
				if not balanced:
                                        #print "balance"
					#balanced = True
					#s.send("b")
					recognizesound = time.time()
					#stream.stop_stream()
					scount += 1
					print "readstream {0:.16f}, heardsound {1:.16f}, fftdone {2:.16f}, fftfreqsdone {3:.16f}, afterhzconv {4:.16f}, recognizesound {5:.16f}, count {6}, sound 800, magnitude {7}".format(readstream, heardsound, fftdone, fftfreqsdone, afterhzconv, recognizesound, scount, np.abs(w)[40])
					#stream.start_stream()

			if np.abs(w)[45] > thresh:	# 45 is index 900hz
				#stream.stop_stream()
				break
			#print "heardsound {0:.16f}, fftdone {1:.16f}, fftfreqsdone {2:.16f}, recognizesound {3:.16f}, count {4}".format(heardsound, fftdone, fftfreqsdone, recognizesound, scount)

		else:
			pass
		#time.sleep(.0005)
		#stream.stop_stream()

	stream.stop_stream()
	stream.close()

	'''	
	w = wave.open("loadbalancing.wav",'wb')
	w.setnchannels(1)
	w.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
	w.setframerate(RATE)
	w.writeframes(b''.join(frames))
	w.close()
	'''

#listen()


#'''
if __name__ == '__main__':

	listen()

#'''


