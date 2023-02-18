import sys

from PIL import Image
from numpy import asarray, uint16, array

img = Image.open(sys.argv[1])
numpydata = asarray(img.convert('RGB'), 'uint16')
length = len([item for sub_list in numpydata for item in sub_list])

def colorArrToARGB(pixel):
    return format((0x0<<12) + (pixel[0]<<8) + (pixel[1]<<4) + (pixel[2]), '#06x')

def printRow(row):
    print('\t', end='')
    [print(f"{colorArrToARGB(x)},",end='') for x in row]
    print()

print(f"const color_t spritesheet[{length}] = \u007b")
[printRow(x) for x in numpydata]
print('};')

