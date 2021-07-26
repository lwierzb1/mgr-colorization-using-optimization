# !/usr/bin/env python
__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from colorization_program.src.main_window import MainWindow


def main():
    main_window = MainWindow()
    main_window.main_loop()


if __name__ == '__main__':
    main()
