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

with open(sys.argv[1],'r') as f:
	line = f.readline()
        while line:
		li = line.split(',')
		times.append(int(li[0]))
		data.append(int(li[1]))
		line = f.readline()


plt.figure()
plt.plot(times,data,color='blue')
plt.xlabel("Time [s]",fontsize=int(sys.argv[2]))
plt.ylabel("Bytes",fontsize=int(sys.argv[2]))
plt.xticks(fontsize=int(sys.argv[2]))
plt.yticks(fontsize=int(sys.argv[2]))
plt.tight_layout()
plt.savefig("portknocking_bytespersec.pdf")

