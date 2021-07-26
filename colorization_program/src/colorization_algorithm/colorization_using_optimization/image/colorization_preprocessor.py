__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import cv2
import numpy as np

from colorization_program.src.colorization_algorithm.colorization_using_optimization.image.update_grid import UpdateGrid
from colorization_program.src.config.singleton_config import SingletonConfig


def _prepare_data_for_colorization(bw_matrix, colored_matrix, sigma=0.33):
    if not SingletonConfig().edge_detection:
        return colored_matrix.copy()
    diff = cv2.cvtColor(bw_matrix, cv2.COLOR_BGR2GRAY) - cv2.cvtColor(colored_matrix, cv2.COLOR_BGR2GRAY)

    median = np.median(bw_matrix)
    lower = int(max(0, (1.0 - sigma) * median))
    upper = int(min(255, (1.0 + sigma) * median))
    filtered = cv2.bilateralFilter(bw_matrix.copy(), 17, 100, 100)
    edged = cv2.Canny(filtered, lower, upper)
    result = colored_matrix.copy()

    for y in range(edged.shape[0]):
        for x in range(edged.shape[1]):
            if edged[y, x] != 0:
                if not _check_if_color_is_nearby_row(diff, y, x, 50) and not _check_if_color_is_nearby_col(diff, y, x,
                                                                                                           50):
                    result[y, x] = edged[y, x]

    return result


def _check_if_color_is_nearby_row(matrix, row, col, r):
    left = False
    right = False

    for r_idx in range(row, min(row + r, matrix.shape[0])):
        if matrix[r_idx][col] > 0:
            right = True

    for r_idx in range(max(0, row - r), row):
        if matrix[r_idx][col] > 0:
            left = True

    return left and right


def _check_if_color_is_nearby_col(matrix, row, col, r):
    left = False
    right = False

    for c_idx in range(col, min(col + r, matrix.shape[1])):
        if matrix[row][c_idx] > 0:
            right = True

    for c_idx in range(max(0, col - r), col):
        if matrix[row][c_idx] > 0:
            left = True

    return left and right


class ColorizationPreprocessor:
    def __init__(self, pencil_config_subject):
        self._pencil_config_subject = pencil_config_subject
        self._GRID_SIZE_ROW = 100
        self._GRID_SIZE_COLUMN = 100

    def prepare_input_for_colorization(self, colorized_cells, bw_matrix, color_matrix):
        bw_gridded = self._create_grid(bw_matrix)
        color_gridded = self._create_grid(color_matrix)
        min_x, min_y, max_x, max_y = self._get_mbb(colorized_cells)

        sub_bw_gridded_image = bw_gridded.get_sub_array(min_x, min_y, max_x, max_y)
        sub_color_gridded_image = color_gridded.get_sub_array(min_x, min_y, max_x, max_y)
        prepared_color_gridded_image = _prepare_data_for_colorization(sub_bw_gridded_image, sub_color_gridded_image)

        return (min_x, min_y, max_x, max_y), (sub_bw_gridded_image, prepared_color_gridded_image)

    def _create_grid(self, matrix):
        grid = UpdateGrid(matrix, self._GRID_SIZE_ROW, self._GRID_SIZE_COLUMN)
        self._pencil_config_subject.attach(grid.pencil_config_observer)
        return grid

    @staticmethod
    def _get_mbb(colorized_cells):
        min_x = None
        max_x = None
        min_y = None
        max_y = None
        for cell in colorized_cells:
            if min_x is None:
                min_x = cell[0]
            elif min_x is not None and cell[0] is not None:
                min_x = min(min_x, cell[0])

            if min_y is None:
                min_y = cell[1]
            elif min_y is not None and cell[1] is not None:
                min_y = min(min_y, cell[1])

            if max_x is None:
                max_x = cell[2]
            elif max_x is not None and cell[2] is not None:
                max_x = max(max_x, cell[2])

            if max_y is None:
                max_y = cell[3]
            elif max_y is not None and cell[3] is not None:
                max_y = max(max_y, cell[3])

        return min_x, min_y, max_x, max_y
