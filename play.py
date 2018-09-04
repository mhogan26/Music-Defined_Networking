import sys
import pyaudio
import numpy as np
import time

# simple script to play a sound

start = time.time()
p = pyaudio.PyAudio()

volume = 1.0     # range [0.0, 1.0]
#volume = 0.0
fs = 44100       # sampling rate, Hz, must be integer
duration = 1   # in seconds, may be float
#duration = 30
f = float(sys.argv[1]) # sine frequency, Hz, may be float

beforesamps = time.time()

# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

gensamps = time.time()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                #frames_per_buffer=1024,
                output=True)
streamopen = time.time()

# play. May repeat with different volume values (if done interactively) 
stream.write(samples)

streamwritten = time.time()

stream.stop_stream()
#stream.close()

#p.terminate()

done = time.time()





#print "start until before samps: {0:.16f}".format(1000*(beforesamps-start))
#print "gen samps time: {0:.16f}".format(1000*(gensamps-beforesamps))
#print "stream open time: {0:.16f}".format(1000*(streamopen-gensamps))
#print "stream write time: {0:.16f}".format(1000*(streamwritten-streamopen))
#print "terminate time: {0:.16f}".format(1000*(done-streamwritten))
#print "total time: {0:.16f}".format(1000*(done-start))
