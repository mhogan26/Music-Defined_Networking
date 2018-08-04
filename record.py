
import pyaudio
import wave
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 70
#WAVE_OUTPUT_FILENAME = "office/office_mic1_2_fanturningon_4(highergain).wav"

#FORMAT = pyaudio.paFloat32
WAVE_OUTPUT_FILENAME = "portscanning_withnoise.wav" 

audio = pyaudio.PyAudio()

device_index = None
for i in range(audio.get_device_count()):
	devinfo = audio.get_device_info_by_index(i)
        #print devinfo['name']
	if 'Built-in' in devinfo['name']:
		continue
	#elif "Mix" in devinfo['name']:
	else: # "USB" in devinfo['name']:
		device_index = i
		print devinfo['name']
		break
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                input_device_index = device_index,
                frames_per_buffer=CHUNK)
print "recording..."
frames = []
 
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)	
print "finished recording"
 
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
