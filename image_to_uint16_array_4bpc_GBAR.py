import sys

from PIL import Image
from numpy import asarray, uint16, array
from math import floor
import argparse
import os

parser = argparse.ArgumentParser(
    prog='image_to_uint16_array_4bpc_GBAR.py',
    description='Convert image input into 16bit 4bit per channel pixel array (ordering=GBAR)',
    epilog='submit bugs to https://github.com/JulianNymark/scripts/issues')

parser.add_argument('file_in')
parser.add_argument('-o', '--file_out')
parser.add_argument('-p', '--file_preamble', help='prepend file output with contents of this file')

args = parser.parse_args()
print(args)
# exit(0)

file_out = open(args.file_out, 'w') if args.file_out else None
file_without_ext = os.path.basename(args.file_in).split('.')[0]
file_preamble = open(args.file_preamble, 'r') if args.file_preamble else None

img = Image.open(args.file_in)
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
    return format((pixelCrushed[0] << 0) + (pixelCrushed[1] << 12) + (pixelCrushed[2] << 8) + (0xf << 4), '#06x')


def printRow(row):
    print('\t', end='', file=file_out)
    [print(f"{colorArrToARGB(x)},", end='', file=file_out) for x in row]
    print(file=file_out)


# print in CPP style output! (copy-paste friendly)
if (file_preamble):
    print(file_preamble.read(), file=file_out)
print(f"const uint16_t {file_without_ext}[{length}] = \u007b", file=file_out)
[printRow(x) for x in numpydata]
print('};', file=file_out)
