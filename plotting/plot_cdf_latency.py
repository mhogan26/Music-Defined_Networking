import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import wave
import struct
import numpy as np
import sys
import operator


q_times = {}
l_times = {}

#queue file
with open(sys.argv[1],'r') as f:
	line = f.readline()
	j = 0
	while line:
		ts = line.split(',')
		precommand = float(ts[0].split()[1])
		knowlength = float(ts[1].split()[1])	
		sentsound = float(ts[2].split()[1])
		q_times[j] = [precommand,knowlength,sentsound]
		line = f.readline()
		j += 1

#listener file
with open(sys.argv[2],'r') as f:
	line = f.readline()
	i = 0
        while line:
		ts = line.split(',')
		readstream = float(ts[0].split()[1])
		heard = float(ts[1].split()[1])
		fftdone = float(ts[2].split()[1])
		fftfreqsdone = float(ts[3].split()[1])
		afterhzconv = float(ts[4].split()[1])
		recognizesound = float(ts[5].split()[1])
		l_times[i] = [heard,fftdone,fftfreqsdone,recognizesound] 
		line = f.readline()
		i += 1


#total_time = []
#queue_total_time = []
#listener_total_time = []
#until_fft_time = []
#sound_aftersent_rcvd_time = []
#fft_total_time = []
fft_time = []
#fft_freqs_time = []
#send_sound_time = []
#knowlength_thru_fft = []
#beforesend = []
#knowlength_aftersend = []
for k in q_times.keys():
	#total_time.append(1000*(l_times[k][-1] - q_times[k][0]))
	#queue_total_time.append(1000*(q_times[k][-1] - q_times[k][0]))
	#listener_total_time.append(1000*(l_times[k][-1] - l_times[k][0]))
	#until_fft_time.append(1000*(l_times[k][0] - q_times[k][0]))
	#sound_aftersent_rcvd_time.append(1000*(l_times[k][0] - q_times[k][2]))
	#fft_total_time.append(1000*(l_times[k][2] - l_times[k][0]))	
	fft_time.append(1000*(l_times[k][2] - l_times[k][1]))
	#fft_freqs_time.append(1000*(l_times[k][2] - l_times[k][1]))
	#send_sound_time.append(1000*(q_times[k][2] - q_times[k][1]))
	#knowlength_thru_fft.append(1000*(l_times[k][3] - q_times[k][1]))
	#beforesend.append(1000*(q_times[k][1] - q_times[k][0]))
	#knowlength_aftersend.append(1000*(q_times[k][-1] - q_times[k][1]))

#print knowlength_thru_fft

#sorted_total_time = np.sort(total_time)
#total_time_yvals=np.arange(len(sorted_total_time))/float(len(sorted_total_time)-1)

#sorted_queue_total_time = np.sort(queue_total_time)
#queue_total_time_yvals=np.arange(len(sorted_queue_total_time))/float(len(sorted_queue_total_time)-1)

#sorted_listener_total_time = np.sort(listener_total_time)
#listener_total_time_yvals=np.arange(len(sorted_listener_total_time))/float(len(sorted_listener_total_time)-1)

#sorted_until_fft_time = np.sort(until_fft_time)
#until_fft_time_yvals=np.arange(len(sorted_until_fft_time))/float(len(sorted_until_fft_time)-1)

#sorted_sound_aftersent_rcvd_time = np.sort(sound_aftersent_rcvd_time)
#sound_aftersent_rcvd_time_yvals=np.arange(len(sorted_sound_aftersent_rcvd_time))/float(len(sorted_sound_aftersent_rcvd_time)-1)

#sorted_fft_total_time = np.sort(fft_total_time)
#fft_total_time_yvals=np.arange(len(sorted_fft_total_time))/float(len(sorted_fft_total_time)-1)

sorted_fft_time = np.sort(fft_time)
fft_time_yvals=np.arange(len(sorted_fft_time))/float(len(sorted_fft_time)-1)

#sorted_fft_freqs_time = np.sort(fft_freqs_time)
#fft_freqs_time_yvals=np.arange(len(sorted_fft_freqs_time))/float(len(sorted_fft_freqs_time)-1)

#sorted_send_sound_time = np.sort(send_sound_time)
#send_sound_time_yvals=np.arange(len(sorted_send_sound_time))/float(len(sorted_send_sound_time)-1)

#sorted_knowlength_thru_fft = np.sort(knowlength_thru_fft)
#knowlength_thru_fft_yvals = np.arange(len(sorted_knowlength_thru_fft))/float(len(sorted_knowlength_thru_fft)-1)

#sorted_beforesend = np.sort(beforesend)
#beforesend_yvals = np.arange(len(sorted_beforesend))/float(len(sorted_beforesend)-1)

plt.figure()
#plt.plot(knowlength_aftersend)
#plt.plot(sorted_total_time, total_time_yvals, color='red',label='total time')
#plt.plot(sorted_queue_total_time, queue_total_time_yvals, color='orange', label='total queue time')
#plt.plot(sorted_listener_total_time, listener_total_time_yvals, color='yellow', label='total listener time')
#plt.plot(sorted_until_fft_time, until_fft_time_yvals, color='green', label='until fft time')
#plt.plot(sorted_sound_aftersent_rcvd_time, sound_aftersent_rcvd_time_yvals, color='blue', label='after sound sent until recvd time')
#plt.plot(sorted_fft_total_time, fft_total_time_yvals, color='cyan', label='fft total time')
plt.plot(sorted_fft_time, fft_time_yvals, color='blue', linewidth=3,label='fft time')
#plt.plot(sorted_fft_freqs_time, fft_freqs_time_yvals, color='purple', label='fft freqs time')
#plt.plot(sorted_send_sound_time, send_sound_time_yvals, color='pink', label = 'send sound time')
#plt.plot(sorted_knowlength_thru_fft,knowlength_thru_fft_yvals,color='gold',label='know length until after fft')
#plt.plot(sorted_beforesend,beforesend_yvals,color='gray',label='before send')
plt.xlabel("FFT Completion Time [ms]",fontsize=int(sys.argv[3]))
plt.ylabel("CDF",fontsize=int(sys.argv[3]))
plt.xticks(np.arange(.15,sorted_fft_time[-1],.1),fontsize=int(sys.argv[3]))
plt.yticks(fontsize=int(sys.argv[3]))
#plt.legend()
#plt.legend(prop={'size': int(sys.argv[3])})
plt.tight_layout()
plt.savefig("latency_cdf.pdf")


