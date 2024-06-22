#!/bin/bash

cd ~/is-aruco-calib-py
source .venv/bin/activate
is-aruco-calib-marker ./etc/conf/create-charuco.json
