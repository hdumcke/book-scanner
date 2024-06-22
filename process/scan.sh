#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source ~/.virtualenvs/screen-commander/bin/activate
screen-commander run $BASEDIR/../screen-commander/scanner.yaml
counter=0
while true;
do
    rm -rf /tmp/left.*
    rm -rf /tmp/right.*
    screen-commander execute $BASEDIR/../screen-commander/take-picture.yaml
    while ! test -f /tmp/left.done; do
    	sleep 1 
    done
    while ! test -f /tmp/right.done; do
    	sleep 1 
    done
    mv /tmp/right.dng $BASEDIR/../output/$(printf "img%04d.dng" "$counter")
    mv /tmp/right.jpg $BASEDIR/../output/$(printf "img%04d.jpg" "$counter")
	counter=$((counter+1))
    mv /tmp/left.dng $BASEDIR/../output/$(printf "img%04d.dng" "$counter")
    mv /tmp/left.jpg $BASEDIR/../output/$(printf "img%04d.jpg" "$counter")
	counter=$((counter+1))
    echo "new scan (no|n)?"
    read input
    echo $input
    if [[ "$input" =~ ^(no|n)$ ]]; then
    	break
	fi
done
screen-commander kill $BASEDIR/../screen-commander/scanner.yaml
