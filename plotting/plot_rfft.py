import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal
import wave
import struct
import numpy as np
import sys
import scipy
from scipy.fftpack import fft, rfft, fftfreq, rfftfreq
import operator

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
data2 = openWav(sys.argv[2])
frate2 = getFrate(sys.argv[2])

w1 = rfft(data1)
f1 = rfftfreq(w1.size)
f1_hz = [int(x) for x in map(lambda x: x*frate1, f1)]

w2 = rfft(data2)
f2 = rfftfreq(w2.size)
f2_hz = map(lambda x: x*frate2, f2)

#print len(f2_hz)

#print abs(sum(map(operator.sub,w1,w2)))

idx8 = f1_hz.index(799)
#idx9 = f1_hz.index(900)
#idx10 = f1_hz.index(1000)+1
#idx11 = f1_hz.index(1099)+1
#idx12 = f1_hz.index(1199)


plt.figure()
plt.plot(f1_hz,np.abs(w1),color='blue',linewidth=2.5,label='on')
#plt.plot(f2_hz,np.abs(w2),color='red',linewidth=.5,label='off')
#plt.legend(prop={'size': int(sys.argv[3])})
plt.xlim(500,1600)
plt.xlabel("Frequency (Hz)",fontsize=int(sys.argv[3]))
plt.ylabel("Magnitude",fontsize=int(sys.argv[3]))
#plt.ylabel("",fontsize=int(sys.argv[3]))
plt.xticks(fontsize=int(sys.argv[3]))
plt.yticks(fontsize=int(sys.argv[3]))
plt.text(750,38000000, 's1', fontsize=int(sys.argv[3]))
plt.text(860,43000000, 's2', fontsize=int(sys.argv[3]))
plt.text(980,52000000, 's3', fontsize=int(sys.argv[3]))
plt.text(1130,100000000, 's4', fontsize=int(sys.argv[3]))
plt.text(1180,58000000, 's5', fontsize=int(sys.argv[3]))
#plt.annotate('switch 1',xy=(800,np.abs(w1)[idx8]),xytext=(600,45000000),arrowprops=dict(facecolor='black', shrink=0.05,width=.1,headwidth=8),fontsize=int(sys.argv[3]))
#plt.annotate('switch 2',xy=(900,np.abs(w1)[idx9]),xytext=(700,55000000),arrowprops=dict(facecolor='black', shrink=0.05,width=.1,headwidth=8),fontsize=int(sys.argv[3]))
#plt.annotate('switch 3',xy=(1000,np.abs(w1)[idx10]),xytext=(875,65000000),arrowprops=dict(facecolor='black', shrink=0.05,width=.1,headwidth=8),fontsize=int(sys.argv[3]))
#plt.annotate('switch 4',xy=(1100,np.abs(w1)[idx11]),xytext=(1250,100000000),arrowprops=dict(facecolor='black', shrink=0.05,width=.1,headwidth=8),fontsize=int(sys.argv[3]))
#plt.annotate('switch 5',xy=(1200,np.abs(w1)[idx12]),xytext=(1300,60000000),arrowprops=dict(facecolor='black', shrink=0.05,width=.1,headwidth=8),fontsize=int(sys.argv[3]))
ax = plt.gca()
ax.yaxis.get_offset_text().set_size(int(sys.argv[3]))
plt.tight_layout()
plt.savefig("rffts.pdf")


