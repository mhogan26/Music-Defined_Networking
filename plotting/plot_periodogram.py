import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal
import wave
import struct
import numpy as np
import sys
import scipy

def openWav(fname):
        wav_file = wave.open(fname, 'r')
        data_size = wav_file.getnframes()
        data = wav_file.readframes(data_size)
        frate = wav_file.getframerate()
        wav_file.close()
        data = struct.unpack('{n}h'.format(n=data_size), data)
        data = np.array(data)
        return data

def getFrate(fname):
        wav_file = wave.open(fname, 'r')
        data_size = wav_file.getnframes()
        data = wav_file.readframes(data_size)
        frate = wav_file.getframerate()
        return frate

data1 = openWav(sys.argv[1])
frate1 = getFrate(sys.argv[1])

f, Pxx_den = signal.periodogram(data1,frate1)



plt.semilogy(f, Pxx_den)
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')
plt.xlim(800,1600)
plt.savefig("periodogram.pdf")





