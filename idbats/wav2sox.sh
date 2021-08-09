#!/bin/bash    
FILES=*.wav
mkdir imgs
    for f in $FILES
    do
        #echo ${f%%.*}
        sox $f -n spectrogram -o imgs/${f%%.*}.png
    done
