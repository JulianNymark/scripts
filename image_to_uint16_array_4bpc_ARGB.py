import sys

from PIL import Image
from numpy import asarray, uint16, array

img = Image.open(sys.argv[1])
numpydata = asarray(img, 'uint16')

def colorArrToARGB(pixel):
    return hex((0xf<<12) + (pixel[0]<<8) + (pixel[1]<<4) + (pixel[2]))

def printRow(row):
    print('\t', end='')
    [print(f"{colorArrToARGB(x)},",end='') for x in row]
    print()

print(f"const color_t spritesheet[{numpydata.size}] = \u007b")
[printRow(x) for x in numpydata]
print('};')

