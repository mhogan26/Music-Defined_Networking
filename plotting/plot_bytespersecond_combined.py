import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal
import wave
import struct
import numpy as np
import sys
import scipy
import operator


data = []
times = []

#dst file
with open(sys.argv[1],'r') as f:
	line = f.readline()
        while line:
		li = line.split(',')
		times.append(int(li[0]))
		data.append(int(li[1]))
		line = f.readline()

times1 = []
data1 = []
#src file
with open(sys.argv[2],'r') as f:
        line = f.readline()
        while line:
                li = line.split(',')
                times1.append(int(li[0]))
                data1.append(int(li[1]))
                line = f.readline()


plt.figure()
plt.plot(times1,data1,color='blue',linewidth=2.5,label='Sent by h1 to h2')
plt.plot(times,data,color='red',linewidth=2.5,label='Received by h2', linestyle='dashed')
plt.xlabel("Time [s]",fontsize=int(sys.argv[3]))
plt.ylabel("Bytes",fontsize=int(sys.argv[3]))
plt.xticks(fontsize=int(sys.argv[3]))
plt.yticks(fontsize=int(sys.argv[3]))
plt.legend()
plt.legend(prop={'size': int(sys.argv[3])})
plt.tight_layout()
plt.savefig("portknocking_bytespersec_combined.pdf")

