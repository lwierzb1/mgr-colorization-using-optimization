#!/usr/bin/env python
"""A Python implementation of Colorization Using Optimization
This code is based on
  Levin, Anat, Dani Lischinski, and Yair Weiss.
  "Colorization using optimization."
  http://www.cs.huji.ac.il/~yweiss/Colorization/
Example usage:
  $ python main.py --input bw.bmp --marked marked.bmp
"""

import argparse
import os

import cv2

from colorization_solver import ColorizationSolver
from image_processing_toolkit import read_as_float_matrix, rgb_matrix_to_image

__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"


def parse_args():
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Colorization using optimization')
    parser.add_argument('--input', help='grayscale image')
    parser.add_argument('--marked', help='image with colour hints')
    parser.add_argument('--store', help='image with colour hints')
    args = parser.parse_args()

    if args.input is None:
        print('Please give the input greyscale image name.')
        exit()

    if os.path.isfile(args.input) == 0:
        print('Input file does not exist')
        exit()

    if args.marked is None:
        print('Please give the hint image name.')
        exit()

    if os.path.isfile(args.marked) == 0:
        print('Hint file does not exist')
        exit()

    return args


def show_result(result):
    while True:
        cv2.imshow("result", result)
        k = cv2.waitKey(33)
        if k == 27:  # Esc key to stop
            break


def store_result(result, path):
    image = rgb_matrix_to_image(result)
    cv2.imwrite(path, image)


def main():
    args = parse_args()

    # read images
    grayscale_matrix = read_as_float_matrix(args.input)
    marked_matrix = read_as_float_matrix(args.marked)

    # perform colorization
    solver = ColorizationSolver(grayscale_matrix, marked_matrix)
    result = solver.solve()
    show_result(result)
    if args.store is not None:
        store_result(result, args.store)


if __name__ == "__main__":
    main()
