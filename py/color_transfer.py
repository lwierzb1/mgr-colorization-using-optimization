import math
import random

import cv2
import numpy as np
from numba import jit


class ColorTransfer:
    def __init__(self):
        self._colored = None
        self._gray = None

    def transfer(self, colored, gray):
        self._colored = colored
        factor_row = 5
        factor_col = 5
        self._colored = cv2.resize(self._colored,
                                   (factor_row * self._colored.shape[0], factor_col * self._colored.shape[1]))
        self._colored = cv2.cvtColor(self._colored, cv2.COLOR_BGR2Lab)
        self._gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

        result = self._colorize()
        cv2.imshow('', result)
        cv2.waitKey(0)
        return result

    def _colorize(self):
        jitter_samples = self._get_jitter_samples(self._colored)
        ref_std_dev = self._neighbor_std_dev(self._colored)
        gray_std_dev = self._neighbor_std_dev(self._gray)

        result = self._colorize_core(np.array(jitter_samples), ref_std_dev, gray_std_dev, self._gray, self._colored)
        return cv2.cvtColor(result.astype(np.uint8), cv2.COLOR_Lab2BGR)

    def _neighbor_std_dev(self, img):
        luminance = cv2.split(img.copy())[0]
        r = 2
        luminance = cv2.copyMakeBorder(luminance, r, r, r, r, cv2.BORDER_CONSTANT, 0)
        return self._neighbor_std_dev_core(luminance, r)

    @staticmethod
    @jit(nopython=True, fastmath=True, cache=True)
    def _colorize_core(jitter_samples, ref_std_dev, gray_std_dev, gray, colored):
        result = np.empty((gray.shape[0], gray.shape[1], 3))
        sample_values = []
        for i in range(len(jitter_samples)):
            x = jitter_samples[i][0]
            y = jitter_samples[i][1]
            sample_values.append(colored[y, x, 0] + ref_std_dev[y, x])

        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                val = gray[i, j] + gray_std_dev[i, j]

                nearest_sample = sample_values[0]
                min_idx = 0
                for k in range(len(sample_values)):
                    if abs(val - sample_values[k]) < abs(val - nearest_sample):
                        nearest_sample = sample_values[k]
                        min_idx = k

                x = jitter_samples[min_idx][0]
                y = jitter_samples[min_idx][1]

                a = colored[y, x, 1]
                b = colored[y, x, 2]

                result[i, j] = [gray[i, j], a, b]
        return result

    @staticmethod
    @jit(nopython=True, fastmath=True, cache=True)
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
    @jit(nopython=True, fastmath=True, cache=True)
    def _get_jitter_samples(img):
        samples_in_a_row = 16
        samples_in_a_col = 16

        block_size_y = math.floor(img.shape[0] / samples_in_a_col)
        block_size_x = math.floor(img.shape[1] / samples_in_a_row)

        jitter_samples = []
        for i in range(samples_in_a_col):
            for j in range(samples_in_a_row):
                rand_x = (j * block_size_x) + (random.randint(0, block_size_x))
                rand_y = (i * block_size_y) + (random.randint(0, block_size_y))
                jitter_samples.append([rand_x, rand_y])

        return jitter_samples
