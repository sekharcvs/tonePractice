import pyaudio
import numpy as np
from scipy.io.wavfile import write
import pdb
import csv

p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float

nKeys = 88 # Number of total frequencies allowed
nTones = 3
maxKeysDiff = 5 # The maximum note difference allowed
# Pick a beginning frequency and generate a ouretone at that frequency
n = np.round(np.random.uniform(-0.5, nKeys + 0.5, size=1))
factor = 2**((n - 49.0)/12.0)
f = 440.0 * factor       # sine frequency, Hz, may be float

fArray = np.zeros(nTones)
fArray[0] = f
# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*fArray[0]/fs)).astype(np.float32)
win = np.hanning(max(np.shape(samples)))
samples = win * samples

for i in range(nTones-1):
        d = np.round(np.random.uniform(-maxKeysDiff - 0.5, maxKeysDiff + 0.5, size=1))
        factor = 2**(d/12.0)
        fArray[i+1] = f * factor
        temp = win * (np.sin(2*np.pi*np.arange(fs*duration)*fArray[i+1]/fs)).astype(np.float32)
        samples = np.append(samples, temp)
        # pdb.set_trace()

            
# Generate Harmonics
s = np.sign(samples)
signal = samples ** 2
signal = volume * s * signal/max(abs(signal))

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)


# pdb.set_trace()
# play. May repeat with different volume values (if done interactively) 
stream.write(signal)
stream.stop_stream()
stream.close()

p.terminate()

# write as a wave file
write('test.wav', fs, signal)

# write the list of frequencies
np.savetxt('frequencies.txt', fArray, fmt='%.2f', delimiter='\n')
