import sys

from PIL import Image
from numpy import asarray, uint16, array
from math import floor

img = Image.open(sys.argv[1])
numpydata = asarray(img.convert('RGB'), 'uint8')
length = len([item for sub_list in numpydata for item in sub_list])


# assuming the format used by color_t is ggggbbbbaaaarrrr

# why do we crush the pixels?
# we need to cram each color into 4 bits!
def crush(pixel):
    source_max_val = 0b11111111 + 1  # uint8
    target_max_val = 0b1111 + 1  # we want to crush to 4 bit color

    return [floor((p/source_max_val) * target_max_val) for p in pixel]


def colorArrToARGB(pixel):
    pixelCrushed = crush(pixel)
    # leaving alpha as 0xf
    return format((pixelCrushed[0] << 0) + (pixelCrushed[1] << 12) + (pixelCrushed[2] << 8) + (0xf<<4), '#06x')


def printRow(row):
    print('\t', end='')
    [print(f"{colorArrToARGB(x)},", end='') for x in row]
    print()


# print in CPP style output! (copy-paste friendly)
print(f"const color_t spritesheet[{length}] = \u007b")
[printRow(x) for x in numpydata]
print('};')
