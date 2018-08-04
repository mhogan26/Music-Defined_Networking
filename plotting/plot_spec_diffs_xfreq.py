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


def getAbsSpecDiff(data1,frate1,data2,frate2):
	f1, t1, Sxx1 = scipy.signal.spectrogram(data1,frate1, nfft=44100)
	f2, t2, Sxx2 = scipy.signal.spectrogram(data2,frate2, nfft=44100)
	sum1 = {}
	sum2 = {}

	for i in range(0,len(f1)):
		sum1[f1[i]] = sum(Sxx1[i])
		sum2[f1[i]] = sum(Sxx2[i])
		
	diffs = {}
	for k in sum1.keys():
		diffs[k] = abs(sum1[k]-sum2[k])
	return diffs

data1 = openWav(sys.argv[1])
frate1 = getFrate(sys.argv[1])
data2 = openWav(sys.argv[2])
frate2 = getFrate(sys.argv[2])

data3 = openWav(sys.argv[3])
frate3 = getFrate(sys.argv[3])

abs_diffs1 = getAbsSpecDiff(data1,frate1,data2,frate2)
abs_diffson = getAbsSpecDiff(data1,frate1,data3,frate3)

plt.figure()
plt.plot(abs_diffs1.keys(), abs_diffs1.values(), color='blue',linewidth=2.5,label='server OFF - server ON')
plt.plot(abs_diffson.keys(), abs_diffson.values(),color='red',linewidth=2.5,linestyle='dashed',label='server ON - server ON')
plt.xlabel("Frequency (Hz)",fontsize=int(sys.argv[4]))
plt.ylabel(r"|$\Delta$ Magnitude|",fontsize=int(sys.argv[4]))
plt.xticks(fontsize=int(sys.argv[4]))
plt.yticks(fontsize=int(sys.argv[4]))
plt.ticklabel_format(style='sci')
ax = plt.gca()
ax.yaxis.get_offset_text().set_size(int(sys.argv[4]))
plt.legend(prop={'size': int(sys.argv[4])})
plt.tight_layout()
plt.savefig("specdiffs.pdf")

