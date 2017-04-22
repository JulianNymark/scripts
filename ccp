#!/bin/bash

# Clipboard CoPy files
# copy files listed in the clipboard from working directory -> destination

if [ $# != 1 ]; then
    echo "Usage:"
    echo "> ccp destination"
    exit 1
fi

files="$(xclip -o)"

for i in $files; do
    cp $i $1
done
