import pdb
import os
import cv2
import numpy as np

in_dir = 'left'


def sharp(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(src=image, ddepth=-1, kernel=kernel)


conf = {
    "dictionary": "DICT_4X4_50",
    # "marker_length": 0.150,
    # "square_length": 0.190,
    "marker_length": 1600,
    "square_length": 2000,
    "n_squares_x": 6,
    "n_squares_y": 4,
    "samples": 100,
    "legacy_pattern": True
}
conf1 = {
    "marker_length": 0.0355,
    "square_length": 0.045,
}

aruco_dict = cv2.aruco.getPredefinedDictionary(dict=cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
aruco_detector = cv2.aruco.ArucoDetector(
    dictionary=aruco_dict,
    detectorParams=aruco_params,
)

margins = conf["square_length"] - conf["marker_length"]
width = int(conf["n_squares_x"] * conf["square_length"] + (2 * margins))
height = int(conf["n_squares_y"] * conf["square_length"] + (2 * margins))

charuco_board = cv2.aruco.CharucoBoard(
    size=(conf["n_squares_x"], conf["n_squares_y"]),
    squareLength=conf1["square_length"],
    markerLength=conf1["marker_length"],
    dictionary=aruco_dict,
)
charuco_board.setLegacyPattern(conf["legacy_pattern"])
charuco_detector = cv2.aruco.CharucoDetector(charuco_board)

# image = charuco_board.generateImage(
#     (width, height),
#     marginSize=int(margins),
#     borderBits=1,
# )

all_corners = np.array([])
all_ids = np.array([])
num_detected_markers = []

for i in range(100):
    file_name = "%s.png" % str(i).zfill(3)
    file = os.path.join(in_dir, file_name)
    image = cv2.imread(file)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sharped = sharp(image_gray)
    aruco_corners, aruco_ids, _ = aruco_detector.detectMarkers(image=sharped)
    criteria = (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 100, 0.001)
    for aruco_corner in aruco_corners:
        aruco_corner = cv2.cornerSubPix(
            sharped, aruco_corner, (3, 3), (-1, -1), criteria
        )
    charuco_corners, charuco_ids, _, _ = charuco_detector.detectBoard(
        image=sharped,
        markerCorners=aruco_corners,
        markerIds=aruco_ids,
    )
    if charuco_ids is None or charuco_corners is None:
        print("Markers not found")
        continue

    # Append marker data
    if np.size(all_corners) == 0:
        all_corners = charuco_corners
        all_ids = charuco_ids
    else:
        all_corners = np.append(all_corners, charuco_corners, axis=0)
        all_ids = np.append(all_ids, charuco_ids, axis=0)
    num_detected_markers.append(len(charuco_ids))

    if False:
        image_copy = cv2.aruco.drawDetectedMarkers(
            image=image.copy(),
            corners=aruco_corners,
            ids=aruco_ids,
        )

        image_copy = cv2.aruco.drawDetectedCornersCharuco(
            image=image_copy.copy(),
            charucoCorners=charuco_corners,
            charucoIds=charuco_ids,
            cornerColor=(255, 125, 125),
        )
        cv2.imshow("Shaped", sharped)
        cv2.imshow("Markers", image_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

print("CAMERA CALIBRATION")

imsize = sharped.shape

cameraMatrixInit = np.array([[ 1000.,    0., imsize[0]/2.],
                            [    0., 1000., imsize[1]/2.],
                            [    0.,    0.,           1.]])

distCoeffsInit = np.zeros((5,1))
flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)
#flags = (cv2.CALIB_RATIONAL_MODEL)
pdb.set_trace()
(ret, camera_matrix, distortion_coefficients0,
rotation_vectors, translation_vectors,
stdDeviationsIntrinsics, stdDeviationsExtrinsics,
perViewErrors) = cv2.aruco.calibrateCameraCharucoExtended(
                      charucoCorners=all_corners,
                      charucoIds=all_ids,
                      board=charuco_board,
                      imageSize=imsize,
                      cameraMatrix=cameraMatrixInit,
                      distCoeffs=distCoeffsInit,
                      flags=flags,
                      criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))

num_detected_markers = np.array(num_detected_markers)
pdb.set_trace()
error, camera_matrix, distortion_coeffs, _, _, = cv2.aruco.calibrateCameraCharuco(
    charucoCorners=all_corners,
    charucoIds=all_ids,
    board=charuco_board,
    imageSize=sharped.shape,
    cameraMatrix=None,
    distCoeffs=None,
)
