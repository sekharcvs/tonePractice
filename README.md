# tonePractice

Utility to practice understanding of relative frequencies of tones played.

*Requirements:*
Python2.x
The following packages installed in python:
numpy
scipy
os
sys
optparse

*Details:*
The aim is to be able to guess is the number of keys that differ from one tone played to the next one (keys difference measured when the corresponding keys on a piano are played to match the same fundamentals of the tones played).

A customizable number of tones are played (use -n, -N or --nTones option)
We can customize the difference in the number of keys across consecutive tones played (use -m, -M or --maxKeysDiff option)

*Usage:*

tonePractice.py [options]

_Options:_
  -h, --help            show this help message and exit
  -n NTONES, -N NTONES, --nTones=NTONES
                        Total number of tones to play. Higher the tougher.
  -m MAXKEYSDIFF, -M MAXKEYSDIFF, --maxKeysDiff=MAXKEYSDIFF
                        Maximum number of keys difference between adjacent
                        notes. Higher the tougher.

*Outputs:*
test.wav - a wave file of the tones played
frequencies.txt - Fundamental frequencies of the tones played
keysDiffs.txt - Number of keys' difference across the tones played (according to a standard piano).
_NOTE: as an example the ratio of <frequency in the second line of frequencies.txt> and the <frequency in the first lines of frequencies.txt> is equal to 2^((<diff value in first line in KeysDiff.txt>)/12)_

*Example:*
tonePractice.py -n 3 -m 5

