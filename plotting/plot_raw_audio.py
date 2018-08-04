import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import wave
import struct
import numpy as np
import sys

def openWav(fname):
        wav_file = wave.open(fname, 'r')
        data_size = wav_file.getnframes()
        data = wav_file.readframes(data_size)
        frate = wav_file.getframerate()
        wav_file.close()
        data = struct.unpack('{n}h'.format(n=data_size), data)
        data = np.array(data)
        return [data,frate]



data,frate = openWav(sys.argv[1])
t = np.linspace(0,round(float(len(data))/float(frate)),len(data))
plt.figure()
plt.plot(t,data,color='blue',linewidth=.5)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.savefig("raw.pdf")


