#!/bin/bash

cd ~
git clone https://github.com/hdumcke/is-aruco-calib-py.git
cd ~/is-aruco-calib-py
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip3 install .
