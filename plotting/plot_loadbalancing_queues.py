import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys

q1times = []
q1lengths = []

# queue 1 (congested)
with open(sys.argv[1], 'r') as f:
	line = f.readline()
	while line:
		l = line.split()
		q1times.append(float(l[0]))
		q1lengths.append(int(l[1]))
		line = f.readline()

q2times = []
q2lengths = []

# queue 2
with open(sys.argv[2], 'r') as f:
	line = f.readline()
	while line:
		l = line.split()
		q2times.append(float(l[0]))
		q2lengths.append(int(l[1]))	
		line = f.readline()

# put times in seconds starting from 0
q1t = [x - q1times[0] for x in q1times]
q2t = [x - q2times[0] for x in q2times]

plt.figure()
plt.plot(q1t[0:25], q1lengths[0:25], color='blue', linewidth=3, label='Outgoing queue s1 -> s2')
plt.plot(q2t[0:25], q2lengths[0:25], color='red', linewidth=3, linestyle='-.', label='Outgoing queue s1 -> s3')
plt.xlabel("Time (s)",fontsize=int(sys.argv[3]))
plt.ylabel("Inst Queue Length (packets)",fontsize=int(sys.argv[3]))
plt.axvline(x=2.7,ymax=.8,linestyle='dashed',linewidth=4,color='#13D9D9')
plt.xticks(fontsize=int(sys.argv[3]))
plt.yticks(fontsize=int(sys.argv[3]))
plt.legend()
plt.legend(prop={'size': int(sys.argv[3])})
plt.tight_layout()
plt.ylim(0,130)
plt.savefig("loadbalancing_queues.pdf", bbox_inches='tight')


