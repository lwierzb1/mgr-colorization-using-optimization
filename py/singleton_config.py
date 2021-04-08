import argparse
import os


class SingletonConfig:
    __instance = None
    __args = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if SingletonConfig.__instance is None:
            SingletonConfig()
        return SingletonConfig.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if SingletonConfig.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SingletonConfig.__instance = self
            self._parse_args()

    def get_args(self):
        return self.__args

    def _parse_args(self):
        parser = argparse.ArgumentParser(description='Colorization using optimization')
        parser.add_argument('--input', help='grayscale image')
        parser.add_argument('--marked', help='image with colour hints')
        parser.add_argument('--store', help='path to store result of algorithm')
        parser.add_argument('--jacobi', help='path to store result of algorithm')
        parser.add_argument('--lgmres', help='path to store result of algorithm')
        parser.add_argument('--processes', help='path to store result of algorithm')
        self.__args = parser.parse_args()

        if self.__args.input is None:
            print('Please give the input greyscale image name.')
            exit()

        if os.path.isfile(self.__args.input) == 0:
            print('Input file does not exist')
            exit()

        if self.__args.marked is None:
            print('Please give the hint image name.')
            exit()

        if self.__args.jacobi is not None:
            self.__args.jacobi = int(self.__args.jacobi)

        if self.__args.processes is not None:
            self.__args.processes = int(self.__args.processes)

        if os.path.isfile(self.__args.marked) == 0:
            print('Hint file does not exist')
            exit()
