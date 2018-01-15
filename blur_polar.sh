#!/bin/bash
TEMP_DIR=/tmp/blur_polar/

DIMS=$(identify $1 | cut -d' ' -f3)
echo "DIMS: "$DIMS

WIDTH=$(echo $DIMS | cut -d'x' -f1)
HEIGHT=$(echo $DIMS | cut -d'x' -f2)

# lol / 2
RADIUS=$(python -c 'import sys; import math; print(math.floor(int(sys.argv[1])) / 2)' $WIDTH)

mkdir -p $TEMP_DIR
convert -size $DIMS gradient: -rotate 90 \
	+distort Polar "$RADIUS,0,.5,.5" +repage -crop $DIMS -flop $TEMP_DIR"gradient_polar.jpg"
convert -size $DIMS $TEMP_DIR"gradient_polar-0.jpg" -background white \
	-channel B -combine $TEMP_DIR"blur_map_angle.jpg"
convert -size $DIMS radial-gradient: -negate \
	-gravity center +repage $TEMP_DIR"gradient_radial.jpg"
convert -size $DIMS $TEMP_DIR"gradient_radial.jpg" $TEMP_DIR"gradient_radial.jpg" $TEMP_DIR"gradient_polar-0.jpg" \
	-channel RGB -combine $TEMP_DIR"blur_map_polar.jpg"
convert $1 $TEMP_DIR"blur_map_polar.jpg" \
	-compose blur -define compose:args=5x0+0+360 -composite \
	blur_polar.jpg
