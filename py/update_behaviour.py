import cv2

from py.image_colorizer import ImageColorizer
from py.image_colorizer_multiprocess import ImageColorizerMultiprocess
from update_grid import UpdateGrid
import numpy as np


def auto_canny(image, colored, sigma=0.33):
    image = cv2.GaussianBlur(image, (17, 17), 0)
    cv2.imshow('', image)
    cv2.waitKey(0)
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    edged = cv2.bilateralFilter(edged, 7, 100, 100)
    lines = cv2.HoughLinesP(edged, 1, np.pi / 180, 120)
    if lines is not None:
        for line in lines:
            cv2.line(colored, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (255, 255, 255), thickness=1)

    cv2.imshow('', colored)
    cv2.waitKey(0)

    # contours, hierarchy = cv2.findContours(edged,
    #                                        cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # for contour in contours:
    #     for i in range(colored.shape[0]):
    #         for j in range(colored.shape[1]):
    #             dist = cv2.pointPolygonTest(contour, (j, i), True)
    #             if dist == 0:
    #                 colored[i][j][0] = 255
    #                 colored[i][j][1] = 255
    #                 colored[i][j][2] = 255
    # cv2.imshow('', colored)
    # cv2.waitKey(colored)
    return colored


class UpdateBehaviour:
    def __init__(self, matrix):
        self._main_grid = UpdateGrid(matrix, 40, 40)
        self.cells = set()

    def on_click(self, e):
        cells_to_update = self._main_grid.on_click(e)
        self.cells.add(cells_to_update)

    def on_motion(self, e):
        cells_to_update = self._main_grid.on_click(e)
        self.cells.add(cells_to_update)

    def perform(self, bw, color):
        a = UpdateGrid(bw, 40, 40)
        b = UpdateGrid(color, 40, 40)

        min_x = None
        max_x = None
        min_y = None
        max_y = None
        for cell in self.cells:
            if min_x is None:
                min_x = cell[0]
            else:
                min_x = min(min_x, cell[0])

            if min_y is None:
                min_y = cell[1]
            else:
                min_y = min(min_y, cell[1])

            if max_x is None:
                max_x = cell[2]
            else:
                max_x = max(max_x, cell[2])

            if max_y is None:
                max_y = cell[3]
            else:
                max_y = max(max_y, cell[3])

        aaa = a.get_sub_array(min_x, min_y, max_x, max_y)
        bbb = b.get_sub_array(min_x, min_y, max_x, max_y)
        # cv2.imshow('', aaa)
        # cv2.waitKey(0)
        cv2.imshow('', auto_canny(aaa, bbb))
        cv2.waitKey(0)
        c = ImageColorizerMultiprocess(aaa, auto_canny(aaa, bbb))
        cv2.imshow('', c.colorize())
        cv2.waitKey(0)
        return self._main_grid.get_sub_array(min_x, min_y, max_x, max_y)
