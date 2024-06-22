#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sudo apt update
sudo apt -y full-upgrade
sudo apt-get install -y vim xrdp libopencv-dev python3-opencv python3-venv

cd $BASEDIR/camera_calibration
./install.sh
