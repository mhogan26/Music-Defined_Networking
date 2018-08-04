import wave
import struct
import numpy as np
import librosa
import librosa.display
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys

def openWav(fname):
        wav_file = wave.open(fname, 'r')
        data_size = wav_file.getnframes()
        data = wav_file.readframes(data_size)
        frate = wav_file.getframerate()
        wav_file.close()
        data = struct.unpack('{n}h'.format(n=data_size), data)
        data = np.array(data)
        return data

def getFrate(fname):
        wav_file = wave.open(fname, 'r')
        data_size = wav_file.getnframes()
        data = wav_file.readframes(data_size)
        frate = wav_file.getframerate()
        return frate


data = openWav(sys.argv[1])
FRATE = getFrate(sys.argv[1])

# create (mel) spectrogram
S = librosa.feature.melspectrogram(data.astype(float), FRATE, n_mels=128)
log_S = librosa.power_to_db(S, ref=np.max)
plt.figure()
librosa.display.specshow(log_S, sr=FRATE, x_axis='time', y_axis='mel')
#plt.title('mel power spectrogram')
cbar = plt.colorbar(format='%+02.0f dB')
cbar.ax.tick_params(labelsize=int(sys.argv[2]))
#plt.axvline(x=2.7,linestyle='dashed',linewidth=4,color='#13D9D9',label="Queue length > threshold")
#plt.axvline(x=9.4,linestyle='dashed',linewidth=4,color='#FFE527',label="75 packets")
#plt.axvline(x=12.6,linestyle='dashed',linewidth=4,color='#22D913',label="25 packets")

#plt.axvline(x=5.3,linestyle='dashed',linewidth=4,color='#22D913',label="Low threshold")
#plt.axvline(x=9.4,linestyle='-.',linewidth=4,color='#13D9D9',label="High threshold")
#plt.axvline(x=12.6,linestyle='dashed',linewidth=3,color='#22D913',label="25 packets")
#plt.axvline(x=12.6,linestyle='dashed',linewidth=4,color='#22D913')

plt.xlabel("Time (s)",fontsize=int(sys.argv[2]))
plt.ylabel("Frequency (Hz)",fontsize=int(sys.argv[2]))
plt.xticks(np.arange(0,50,10),np.arange(0,50,10))
plt.xticks(fontsize=int(sys.argv[2]))
plt.yticks(fontsize=int(sys.argv[2]))
#plt.yticks(np.arange(0,900,100),fontsize=int(sys.argv[2]))
#plt.xlim(23,36)
#plt.ylim(ymin=2048)
#plt.legend(loc='upper right',framealpha=1)
#plt.legend(prop={'size': 16})
#plt.locator_params(axis='x', nbins=5)
plt.tight_layout()
#plt.gray()
plt.savefig('melspectrogram.pdf')

