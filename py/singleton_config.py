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
        self.mode = None
        self.jacobi_approximation = None
        self.linear_algorithm = None
        self.processes = None
        self.colorization_algorithm = None
        self.max_video_frames_per_section = None

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
        self.colorization_algorithm = config.get('colorizer', 'colorization_algorithm')

        if config.has_option('colorizer', 'jacobi_approximation'):
            self.jacobi_approximation = config.getfloat('colorizer', 'jacobi_approximation')

        if config.has_option('colorizer', 'max_video_frames_per_section'):
            self.max_video_frames_per_section = config.getint('colorizer', 'max_video_frames_per_section')
        else:
            self.max_video_frames_per_section = 10

        if self.mode is None:
            print("Please set 'mode' in .ini file ('video'|'image')")
            exit()

        if self.colorization_algorithm is None:
            print("Please set 'colorization_algorithm' in .ini file ('CUO'|'CT')")
            exit()

        if self.linear_algorithm is None:
            print("Please set 'linear_algorithm' in .ini file ('lgmres'|'spsolve'|'jacobi')")
            exit()

        if self.linear_algorithm == 'jacobi' and self.jacobi_approximation is None:
            print("Please set 'jacobi_approximation' in .ini file")
            exit()

        if self.processes is None:
            self.processes = 1

    def save_state(self):
        state_value = dict()
        state_value['mode'] = self.mode
        state_value['processes'] = self.processes
        state_value['colorization_algorithm'] = self.colorization_algorithm
        state_value['max_video_frames_per_section'] = self.max_video_frames_per_section
        state_value['linear_algorithm'] = self.linear_algorithm
        return state_value

    def restore_state(self, data):
        self.mode = data['mode']
        self.processes = data['processes']
        self.colorization_algorithm = data['colorization_algorithm']
        self.linear_algorithm = data['linear_algorithm']
        self.max_video_frames_per_section = data['max_video_frames_per_section']
