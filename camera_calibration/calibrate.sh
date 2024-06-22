#!/bin/bash

cd ~/is-aruco-calib-py
source .venv/bin/activate
is-aruco-calib-intrinsic ./etc/conf/calibrate-charuco.json
