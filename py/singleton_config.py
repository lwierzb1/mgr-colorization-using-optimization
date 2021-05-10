import configparser


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
            self._parse_config()

    def _parse_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.mode = config.get('colorizer', 'mode')
        self.linear_algorithm = config.get('colorizer', 'linear_algorithm')
        self.processes = config.getint('colorizer', 'process_no')

        if 'jacobi_approximation' in config:
            self.jacobi_approximation = config.getint('colorizer', 'jacobi_approximation')
        else:
            self.jacobi_approximation = None

        if self.mode is None:
            print("Please set 'mode' in .ini file ('video'|'image')")
            exit()

        if self.linear_algorithm is None:
            print("Please set 'linear_algorithm' in .ini file ('lgmres'|'linalg'|'jacobi')")
            exit()

        if self.linear_algorithm == 'jacobi' and self.jacobi_approximation is None:
            print("Please set 'jacobi_approximation' in .ini file")
            exit()

        if self.processes is None:
            self.processes = 1
