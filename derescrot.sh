#!/bin/bash
set -euxo pipefail

# dependencies = [scrot, slop, xclip, feh]

# this script exists because
# gnome-screenshot won't allow
# -a AND -d at the same time...sad..smh

region="$(slop -f %x,%y,%w,%h)"
sleep 2s;
scrot -a "$region" /tmp/screenshot-$(date +%F_%T).png -e 'xclip -selection c -t image/png < $f && feh $f'
