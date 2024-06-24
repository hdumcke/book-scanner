import rawpy
import cv2
import os
import yaml
import numpy as np

in_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'output')
out_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'output_processed')
calibatrion_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'camera_calibration')

mtx = []
dist = []
with open(os.path.join(calibatrion_dir, 'right_camera.yaml')) as f:
    loadeddict = yaml.safe_load(f)
    mtx.append(loadeddict.get('camera_matrix'))
    dist.append(loadeddict.get('dist_coeff'))
with open(os.path.join(calibatrion_dir, 'left_camera.yaml')) as f:
    loadeddict = yaml.safe_load(f)
    mtx.append(loadeddict.get('camera_matrix'))
    dist.append(loadeddict.get('dist_coeff'))

# Adapt camera matrix for twice as many pixel as used during calibration
for i in range(2):
    mtx[i][0][0] = 2.0 * mtx[i][0][0]
    mtx[i][0][2] = 2.0 * mtx[i][0][2]
    mtx[i][1][1] = 2.0 * mtx[i][1][1]
    mtx[i][1][2] = 2.0 * mtx[i][1][2]

mtx = np.array(mtx)
dist = np.array(dist)

onlyfiles = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
num_of_files = 0
for i in range(len(onlyfiles)):
    num_of_files = max(num_of_files, int(onlyfiles[i].split('.')[0][-4:]))
num_of_files += 1

for i in range(num_of_files):
    file_name = "img%s.dng" % str(i).zfill(4)
    file = os.path.join(in_dir, file_name)
    with rawpy.imread(file) as raw:
        rgb = raw.postprocess()

    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape[:2]

#    import pdb
#    pdb.set_trace()
#    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx[i % 2], dist[i % 2], (w, h), 1, (w, h))
#    dst = cv2.undistort(gray, mtx[i % 2], dist[i % 2], None, newcameramtx)
    dst = cv2.undistort(gray, mtx[i % 2], dist[i % 2], None)
    cv2.imshow("Undistorted", dst)
    cv2.imshow("Distorted", gray)
    cv2.waitKey(0)

cv2.destroyAllWindows()
