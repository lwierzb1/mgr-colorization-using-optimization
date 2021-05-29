# Instructions
# Place the BW video, marked image frame in the same directory as this python file
# Under the if __name__ == '__main__': fill in the grey_name, marked_name, and color_name. Run the python script

import time
import math
import sys

import cv2
import numpy as np

from color_transfer import ColorTransfer
from video_optimization_colorizer import VideoOptimizationColorizer
from video_transfer_colorizer import VideoTransferColorizer


def import_images(grey_name, marked_name):
    cap = cv2.VideoCapture(grey_name)

    marked_frame = cv2.imread(marked_name)
    marked_frame_grey = cv2.cvtColor(marked_frame, cv2.COLOR_BGR2GRAY)

    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    old_frame_grey = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

    # Define which pixels have been colorized
    old_frame_norm = cv2.normalize(old_frame_grey.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)
    marked_frame_norm = cv2.normalize(marked_frame_grey.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)

    threshold = 0.03
    color_frame = abs(old_frame_norm - marked_frame_norm) > threshold

    return cap, marked_frame, color_frame, old_gray


def parameters():
    # params for ShiTomasi corner detection
    feature_params = dict(maxCorners=100,
                          qualityLevel=0.3,
                          minDistance=7,
                          blockSize=7)
    # Parameters for lucas kanade optical flow
    lk_params = dict(winSize=(15, 15),
                     maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    return feature_params, lk_params


def colorlist_populate(count, color_list, color_list_new):
    if count == 0:
        for i in range(color_frame.shape[0]):  # row, height
            for j in range(color_frame.shape[1]):  # columns, width
                if color_frame[i, j]:
                    color_list.append([i, j])

        color_list = np.asarray(color_list, dtype=np.float64)
        # print(color_list)
    else:
        color_list = np.asarray([i[0] for i in color_list_new], dtype=np.float64)
        color_list_new = []
        # print(color_list)

    return color_list, color_list_new


if __name__ == '__main__':
    grey_name = "D:/studia/mgr/sources/mgr-colorization-using-optimization/test/video/output.avi "  # BW video
    marked_name = "D:/studia/mgr/sources/mgr-colorization-using-optimization/test/video/a.bmp"  # BW image with color markings. Only use BMP
    marked_name2 = "D:/studia/mgr/sources/mgr-colorization-using-optimization/test/video/result.bmp"  # BW image with color markings. Only use BMP
    color_name = "C:/Users/Lukasz/Downloads/OMCS6475_FinalProject-master/toddlermarked"  # Specify the file name of the final colorized image. LEAVE OUT FILE EXTENSION

    # for i in range(1, 11):
    #     t = time.time()
    a1 = 'D:/studia/mgr/sources/mgr-colorization-using-optimization/test_hd/5_bw.bmp'
    a2 = 'D:/studia/mgr/sources/mgr-colorization-using-optimization/test_hd/5_result.bmp'
    #
    c = ColorTransfer()
    res = c.transfer(cv2.imread(a2), cv2.imread(a1))
    #     cv2.imwrite(str(i) + '__transfer.bmp', res)
    #     stop = time.time()
    #     print('[]' + '(' + str(i) + ')', stop - t)

    # v = VideoOptimizationColorizer(None, grey_name)
    # v.colorize_video(marked_name)

    v = VideoTransferColorizer(None, grey_name)
    v.colorize_video(cv2.imread(a2))

    # grey_name = "bizbw.mp4"  # BW video
    # marked_name = "bizmarked00.bmp"  # BW image with color markings. Only use BMP
    # color_name = "bizcolored"  # Specify the file name of the final colorized image. Only use BMP

    cap, marked_frame, color_frame, old_gray = import_images(grey_name, marked_name)
    feature_params, lk_params = parameters()

    p0 = cv2.goodFeaturesToTrack(old_gray, mask=None,
                                 **feature_params)  # Determine what features to track in source video
    count = 0
    color_list = []
    color_list_new = []

    while cap.isOpened():
        ret, frame = cap.read()

        # end with last frame in video
        if frame is None:
            break

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('', frame_gray)
        frame_circle = frame.copy()

        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        # Select good points
        good_new = p1[st == 1]
        good_old = p0[st == 1]

        color_list, color_list_new = colorlist_populate(count, color_list, color_list_new)

        # https://stackoverflow.com/questions/209840/map-two-lists-into-a-dictionary-in-python
        getTransform = {tuple(p0): p1 - p0 for p0, p1 in (zip(list(good_old), list(good_new)))}

        for i, c in enumerate(color_list):
            min_dist = sys.maxsize
            min_dist_point = None
            color_p = marked_frame[int(c[0]), int(c[1])]
            for p in good_old:
                current_dist = math.sqrt(((p[0] - c[0]) ** 2) + ((p[1] - c[1]) ** 2))
                if current_dist < min_dist:
                    min_dist = current_dist
                    min_dist_point = p

            v0 = getTransform[tuple(min_dist_point)]
            # print(v0)

            v0 = np.array([v0[1], v0[0]])

            color_list_new.append((c + v0, color_p))

        for (coord, color) in color_list_new:
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))
            if 0 <= int(coord[0]) < frame_height and 0 <= int(coord[1]) < frame_width:
                frame_circle[int(coord[0]), int(coord[1])] = color.tolist()

        cv2.imshow('', frame_circle)
        cv2.waitKey(0)
        # cv2.imwrite(color_name + "{}.bmp".format(count), frame_circle)

        print(color_name + "{}.bmp".format(count))
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)

        marked_frame = frame_circle
        old_frame_grey = old_gray

        # colorizehjvideoimage.colorize(frame, frame_circle, color_name)

        count += 1

    # When everything done, release the video capture and video write objects
    cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
