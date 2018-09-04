# Music-Defined_Networking

plotting: these are the scripts to plot the various graphs used in the paper

tesbedbinaries: binaries for the switches in the tesbed. the first number is the frequency the switch is playing sounds at and the second number is the last digit in the ip address (10.0.0.x) the switch is sending sound messages to (to change the ip on the raspberry pis temporarily: sudo ifconfig eth0:0 10.0.0.1 up). they send tcp sound messages to port 8888.

binaries: various binaries used to test different sound applications, including the binary for used for the port knocking/elephant flow applications. unless specified in the comment, they send sound messages to port 8888, ip 10.0.1.8 (default controller ip for the switches).
