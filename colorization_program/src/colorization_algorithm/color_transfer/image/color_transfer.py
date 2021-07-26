__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import math
import random

import cv2
import numba
import numpy as np

from colorization_program.src.config.singleton_config import SingletonConfig


@numba.jit(parallel=True, nopython=True, fastmath=True, cache=True)
def _colorize_parallel(gray, gray_std_dev, sample_values, jitter_samples, colored, result):
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            val = gray[i, j] + gray_std_dev[i, j]

            min_idx = np.argmin(np.abs(sample_values - val))
            x = jitter_samples[min_idx][0]
            y = jitter_samples[min_idx][1]

            a = colored[y, x, 1]
            b = colored[y, x, 2]
            result[i, j] = [gray[i, j], a, b]


def _colorize_core(jitter_samples, ref_std_dev, gray_std_dev, gray, colored):
    result = np.empty((gray.shape[0], gray.shape[1], 3))
    sample_values = []
    for i in range(len(jitter_samples)):
        x = jitter_samples[i][0]
        y = jitter_samples[i][1]
        sample_values.append(colored[y, x, 0] + ref_std_dev[y, x])

    _colorize_parallel(gray, gray_std_dev, np.array(sample_values), jitter_samples, colored, result)
    return result


class ColorTransfer:
    def __init__(self):
        self._colored = None
        self._gray = None

    def k_mean(self, image):
        pixel_values = image.reshape((-1, 3))
        pixel_values = np.float32(pixel_values)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        k = 8
        _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        return labels, centers

    def transfer(self, colored, gray):
        self._colored = colored
        self._colored = cv2.cvtColor(self._colored, cv2.COLOR_BGR2Lab)
        self._gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

        return self._colorize()

    def _colorize(self):
        if SingletonConfig().k_means:
            jitter_samples = self._get_k_samples(self._colored)
        else:
            jitter_samples = self._get_jitter_samples(self._colored)

        ref_std_dev = self._neighbor_std_dev(self._colored)
        gray_std_dev = self._neighbor_std_dev(self._gray)

        result = _colorize_core(np.array(jitter_samples), ref_std_dev, gray_std_dev, self._gray, self._colored)
        return cv2.cvtColor(result.astype(np.uint8), cv2.COLOR_Lab2BGR)

    def _neighbor_std_dev(self, img):
        luminance = cv2.split(img.copy())[0]
        r = 5
        luminance = cv2.copyMakeBorder(luminance, r, r, r, r, cv2.BORDER_CONSTANT, 0)
        return self._neighbor_std_dev_core(luminance, r)

    def _get_k_samples(self, reference_img):
        samples = []
        color_labels, color_centers = self.k_mean(reference_img)

        x = reference_img.reshape((-1, 3))
        for i in range(8):
            y = x.copy()
            y[color_labels.flatten() != i] = [0, 0, 0]
            y = y.reshape(reference_img.shape)
            sub_samples = self._find_samples(y)
            for ii in sub_samples:
                samples.append([ii[1], ii[0]])

        return samples

    @staticmethod
    @numba.jit(nopython=True, fastmath=True, cache=True)
    def _neighbor_std_dev_core(luminance, r):
        result = np.empty((luminance.shape[0], luminance.shape[1]))
        for i in range(r, luminance.shape[0] - r):
            for j in range(r, luminance.shape[1] - r):
                mean = 0
                for m in range(i - r, i + r):
                    for n in range(j - r, j + r):
                        mean += luminance[m, n]

                mean /= (2 * r + 1) ** 2

                std_dev = 0
                for m in range(i - r, i + r):
                    for n in range(j - r, j + r):
                        std_dev += (luminance[m, n] - mean) ** 2

                std_dev /= (2 * r + 1) ** 2

                std_dev = math.sqrt(std_dev)
                result[i - r, j - r] = std_dev

        return result

    @staticmethod
    @numba.jit(nopython=True, fastmath=True, cache=True)
    def _get_jitter_samples(img):
        samples_in_a_row = img.shape[0] / 2
        samples_in_a_col = img.shape[1] / 2

        block_size_y = math.floor(img.shape[0] / samples_in_a_col)
        block_size_x = math.floor(img.shape[1] / samples_in_a_row)

        jitter_samples = []

        for i in range(samples_in_a_col):
            for j in range(samples_in_a_row):
                rand_x = random.randint(0, img.shape[1] - 1)
                rand_y = random.randint(0, img.shape[0] - 1)
                jitter_samples.append([rand_x, rand_y])

        return jitter_samples

    @staticmethod
    def _find_samples(img):
        no_of_samples = int(img[np.nonzero(np.sum(img, axis=2))].size * 0.25)
        samples = list(zip(*np.nonzero(np.sum(img, axis=2))))
        return random.sample(samples, no_of_samples)
