__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import cv2


class ColorizationPostprocessor:
    def post_process(self, mbb, original_bw, input_bw, output_colored):
        propagate_up, propagate_right, propagate_down, propagate_left = self._check_if_matrix_is_colored_on_edges(
            input_bw, output_colored)

        needs_propagate = propagate_up or propagate_right or propagate_down or propagate_left
        new_mbb = [0, 0, 0, 0]
        if propagate_up:
            new_mbb[1] = max(mbb[1] - 100, 0)
        if propagate_right:
            new_mbb[2] = min(mbb[2] + 100, original_bw.shape[1])
        if propagate_down:
            new_mbb[3] = min(mbb[3] + 100, original_bw.shape[0])
        if propagate_left:
            new_mbb[0] = max(mbb[0] - 100, 0)

        return needs_propagate, new_mbb

    @staticmethod
    def _check_if_matrix_is_colored_on_edges(input_bw, colored_matrix):
        diff = cv2.cvtColor(colored_matrix.copy(), cv2.COLOR_BGR2GRAY) - cv2.cvtColor(colored_matrix,
                                                                                      cv2.COLOR_BGR2GRAY)

        left_colored_pixels_counter = 0
        right_colored_pixels_counter = 0
        up_colored_pixels_counter = 0
        down_colored_pixels_counter = 0

        height = diff.shape[0]
        width = diff.shape[1]

        for r in range(height):
            if diff[r][0] != 0:
                left_colored_pixels_counter += 1

            if diff[r][colored_matrix.shape[1] - 1] != 0:
                right_colored_pixels_counter += 1

        for c in range(width):
            if diff[0][c] != 0:
                up_colored_pixels_counter += 1

            if diff[colored_matrix.shape[0] - 1][c] > 0:
                down_colored_pixels_counter += 1

        return up_colored_pixels_counter > width / 2, right_colored_pixels_counter > height / 2, \
               down_colored_pixels_counter > width / 2, left_colored_pixels_counter > height / 2
