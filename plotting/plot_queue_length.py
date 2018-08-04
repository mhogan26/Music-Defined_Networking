import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import numpy as np

times = []
l = []
with open(sys.argv[1],'r') as f:
	line = f.readline()
	while line:
		li = line.split()
		times.append(float(li[0]))
		l.append(int(li[1]))
		line = f.readline()

'''
blue_l = l[0:l.index(25)]
blue_t = times[0:l.index(25)]
red_l = l[l.index(25):l.index(75)]
red_t = times[l.index(25):l.index(75)]
magenta_l = l[l.index(75):l.index(16)]
magenta_t = times[l.index(75):l.index(16)]
blue2_l = l[l.index(16):]
blue2_t = times[l.index(16):]
'''


plt.figure()
plt.plot(times,l,color='blue',linewidth=2.5)
plt.axvline(x=5.3,linestyle='dashed',linewidth=3,color='#22D913',label="Low threshold")
plt.axvline(x=9.4,linestyle='-.',linewidth=3,color='#13D9D9',label="High threshold")
#plt.axvline(x=12.6,linestyle='dashed',linewidth=3,color='#22D913',label="25 packets")
plt.axvline(x=12.6,linestyle='dashed',linewidth=3,color='#22D913')
#plt.axhline(y=25,linestyle='dashed',linewidth=.5,color='red')
#plt.axhline(y=75,linestyle='dashed',linewidth=.5,color='magenta')
#plt.plot(blue_t,blue_l,color='blue',linewidth=1)
#plt.plot(red_t,red_l,color='red',linewidth=1)
#plt.plot(magenta_t,magenta_l,color='magenta',linewidth=1)
#plt.plot(blue2_t,blue2_l,color='blue',linewidth=1)
plt.ylim(0,145)
plt.legend()
plt.legend(prop={'size': int(sys.argv[2])},loc='upper right',framealpha=1)
plt.xlabel("Time (s)",fontsize=int(sys.argv[2]))
plt.ylabel("Inst Queue Length (packets)",fontsize=int(sys.argv[2]))
plt.xticks(np.arange(0,20,3),fontsize=int(sys.argv[2]))
plt.yticks(fontsize=int(sys.argv[2]))
plt.tight_layout()
plt.savefig("qlength.pdf")



