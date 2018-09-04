from time import sleep, time
from subprocess import *
import re
#import play2
import pyaudio
import numpy as np

# continuously checks mininet queue size (switch1-eth3 queue) every interval_sec seconds
# plays either 600hz,700hz,or 800hz depending on size
# plays 900hz to signal end of test

default_dir = '.'


def monitor_qlen(stream,sample500,sample600,sample700,interval_sec=2):
  pat_queued =re.compile(r'backlog\s[^\s]+\s([\d]+)p')
  cmd = "tc -s qdisc show dev s1-eth3"
  ret = []
  #open("qlen.txt","w").write('')
  t0 = "%f" % time()

  
  sleep(.5)

  for i in range(0,100): 
    precommand = time()
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.stdout.read()
    matches = pat_queued.findall(output)
    if matches and len(matches) > 1:
      ret.append(matches[1])
      qlength = matches[1]
      knowlength = time()
      if int(qlength) < 25: 
	stream.write(sample500)
        #play2.main("500.0",1.0)
      elif int(qlength) < 75:
	stream.write(sample600)
        #play2.main("600.0",1.0)
      else:
	stream.write(sample700)
        #play2.main("700.0",1.0)
      sentsound = time()
      #t1 = "%f" % time()
      #print "{0:.16f}".format(1000*(sentsound-knowlength))
      #print("{} {}".format(float(t1)-float(t0), qlength))
      print "precommand {0:.16f}, knowlength {1:.16f}, sentsound {2:.16f}, length {3}, count {4}".format(precommand, knowlength, sentsound, qlength, (i+1))
      #open("qlen.txt","a").write(str(float(t1)-float(t0))+' '+matches[1]+'\n')
    sleep(interval_sec)


p = pyaudio.PyAudio()
volume = 1.0
fs = 48000
duration = .022


sample600 = (np.sin(2*np.pi*np.arange(fs*duration)*600.0/fs)).astype(np.float32).tostring()
sample700 = (np.sin(2*np.pi*np.arange(fs*duration)*700.0/fs)).astype(np.float32).tostring()
sample800 = (np.sin(2*np.pi*np.arange(fs*duration)*800.0/fs)).astype(np.float32).tostring()
sample900 = (np.sin(2*np.pi*np.arange(fs*.1)*900.0/fs)).astype(np.float32).tostring()

stream = p.open(format=pyaudio.paFloat32,
		channels=1,
		rate=fs,
		output=True)

monitor_qlen(stream,sample600,sample700,sample800)

#play2.main("900.0", 1.0)
stream.write(sample900)
stream.stop_stream()
stream.close()
p.terminate()






