import numpy as np
from scipy.io.wavfile import write
import os
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--nTones", "-n", "-N", dest="nTones",
                  help="Total number of tones to play. Higher the tougher.")
parser.add_option("--maxKeysDiff", "-m", "-M", dest="maxKeysDiff",
                  help="Maximum number of keys difference between adjacent notes. Higher the tougher.")

(options, args) = parser.parse_args()


volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float
isFloat = True

# For key table refer to: https://en.wikipedia.org/wiki/Piano_key_frequencies
# Anchor key number 49 corresponds to a frequency of 440Hz.
minKey = 33 # Lowest key that is allowed to be played
maxKey = 88 # Highest key that is allowed to be played

anchorKey = 49
anchorFreq = 440

nTones = int(options.nTones)
maxKeysDiff = int(options.maxKeysDiff) # The maximum note difference allowed

fArray = np.zeros(nTones)

# Pick a beginning frequency and generate a ouretone at that frequency
n = np.round(np.random.uniform(33 - 0.5, maxKey + 0.5, size=1))
lastKey = n

factor = 2**((n - anchorKey)/12.0)
f = float(anchorFreq) * factor       # sine frequency, Hz, may be float
fArray[0] = f
# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*fArray[0]/fs)).astype(np.float32)
win = np.hanning(max(np.shape(samples)))
samples = win * samples

keyDiffs = np.zeros(nTones-1)
for i in range(nTones-1):
        d = np.round(np.random.uniform(-maxKeysDiff - 0.5, maxKeysDiff + 0.5, size=1))
        d = max(minKey - lastKey, min(maxKey - lastKey, d))
        keyDiffs[i] = d

        factor = 2**(d/12.0)
        fArray[i+1] = fArray[i] * factor
        temp = win * (np.sin(2*np.pi*np.arange(fs*duration)*fArray[i+1]/fs)).astype(np.float32)
        samples = np.append(samples, temp)

# Generate Harmonics
s = np.sign(samples)
signal = samples ** 2
signal =  s * abs(volume * signal/max(abs(signal)))
if isFloat is False:
        signal = 32768 * signal.astype(np.int16)

# write as a wave file
write('test.wav', fs, signal)
os.system('afplay ./test.wav')

while True:
        print("Decide the note differences and press:\n\
           c to show the results\n\
           r to repeat the tones")
        char = sys.stdin.read(1)
        sys.stdin.read(1)
        if char == 'c':
                break
        else:
                if char == 'r':
                        os.system('afplay ./test.wav')
                else:
                        print("Unrecognized character entered. Try again.\n")


print(str(keyDiffs))


# write the list of frequencies
np.savetxt('frequencies.txt', fArray, fmt='%.2f', delimiter='\n')
np.savetxt('keysDiffs.txt', keyDiffs, fmt='%d', delimiter='\n')
