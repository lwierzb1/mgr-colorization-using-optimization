#!/usr/bin/env python
"""A Python implementation of Colorization Using Optimization
This code is based on
  Levin, Anat, Dani Lischinski, and Yair Weiss.
  "Colorization using optimization."
  http://www.cs.huji.ac.il/~yweiss/Colorization/
Example usage:
  $ python main.py --input bw.bmp --marked marked.bmp
"""

import time
from image_colorizer import ImageColorizer
from image_colorizer_multiprocess import ImageColorizerMultiprocess
from image_processing_toolkit import write_image
from singleton_config import SingletonConfig

__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"


def main():
    config = SingletonConfig.get_instance()
    start = time.time()
    image_colorizer = ImageColorizerMultiprocess(config.get_args().input, config.get_args().marked)
    result = image_colorizer.colorize()
    write_image(result, config.get_args().store)
    end = time.time()
    print(end - start)


if __name__ == "__main__":
    main()
