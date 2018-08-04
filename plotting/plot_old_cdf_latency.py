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


c_times = []
q_times = []

#controller file
with open(sys.argv[1],'r') as f:
	line = f.readline()
	while line:
		if line.startswith("1"):
			c_times.append(float(line.strip()))
		line = f.readline()

#queue file
with open(sys.argv[2],'r') as f:
	line = f.readline()
        while line:
		q_times.append(float(line.strip()))
		line = f.readline()

print len(c_times)

data = [1000*x for x in map(operator.sub,c_times,q_times)]
sorted_data = np.sort(data)

yvals=np.arange(len(sorted_data))/float(len(sorted_data)-1)

print sorted_data

plt.figure()
plt.plot(sorted_data,yvals,color='blue')
plt.xlabel("Message Latency [ms]",fontsize=int(sys.argv[3]))
plt.ylabel("CDF",fontsize=int(sys.argv[3]))
plt.xticks(fontsize=int(sys.argv[3]))
plt.yticks(fontsize=int(sys.argv[3]))
plt.tight_layout()
plt.savefig("latency_cdf.pdf")

