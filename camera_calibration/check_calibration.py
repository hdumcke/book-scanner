import os
import cv2
import yaml
import numpy as np

in_dir = 'left'
in_dir = 'right'

with open("./%s_camera.yaml" % in_dir, 'r') as f:
    data = yaml.safe_load(f)

camera_matrix = np.array(data["camera_matrix"])
distortion_coefficients0 = np.array(data["dist_coeff"])

if False:
    for i in range(100):
        file_name = "%s.png" % str(i).zfill(3)
        file = os.path.join(in_dir, file_name)
        image = cv2.imread(file)
        img_undist = cv2.undistort(image,camera_matrix,distortion_coefficients0,None)
        cv2.imshow("file_name", image)
        cv2.imshow("Undistorted", img_undist)
        cv2.waitKey(5)

with open("./%s_camera_alt.yaml" % in_dir, 'r') as f:
    data = yaml.safe_load(f)

camera_matrix = np.array(data["camera_matrix"])
distortion_coeffs = np.array(data["dist_coeff"])

if True:
    for i in range(100):
        file_name = "%s.png" % str(i).zfill(3)
        file = os.path.join(in_dir, file_name)
        image = cv2.imread(file)
        img_undist = cv2.undistort(image,camera_matrix,distortion_coeffs,None)
        cv2.imshow("file_name", image)
        cv2.imshow("Undistorted", img_undist)
        cv2.waitKey(5)
