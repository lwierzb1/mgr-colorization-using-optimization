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

from image_colorizer import ImageColorizer
import time
import sys
from statistics import mean

__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"


def parse_args():
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Colorization using optimization')
    parser.add_argument('--input', help='grayscale image')
    parser.add_argument('--marked', help='image with colour hints')
    parser.add_argument('--store', help='path to store result of algorithm')
    parser.add_argument('--jacobi', help='path to store result of algorithm')
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


def main():
    args = parse_args()
    start = time.time()
    image_colorizer = ImageColorizer(args.input, args.marked, args.store)
    image_colorizer.colorize()
    end = time.time()
    print(end - start)


if __name__ == "__main__":
    main()
