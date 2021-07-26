__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SingletonConfig(metaclass=SingletonMeta):
    def __init__(self):
        self.mode = None
        self.jacobi_approximation = None
        self.linear_algorithm = None
        self.processes = None
        self.colorization_algorithm = None
        self.max_video_frames_per_section = None
        self.k_means = None
        self.edge_detection = None

    def save_state(self):
        state_value = dict()
        state_value['mode'] = self.mode
        state_value['processes'] = self.processes
        state_value['colorization_algorithm'] = self.colorization_algorithm
        state_value['max_video_frames_per_section'] = self.max_video_frames_per_section
        state_value['linear_algorithm'] = self.linear_algorithm
        state_value['k_means'] = self.k_means
        state_value['edge_detection'] = self.edge_detection
        return state_value

    def restore_state(self, data):
        self.mode = data['mode']
        self.processes = data['processes']
        self.colorization_algorithm = data['colorization_algorithm']
        self.linear_algorithm = data['linear_algorithm']
        self.max_video_frames_per_section = data['max_video_frames_per_section']
        self.k_means = data['k_means']
        self.edge_detection = data['edge_detection']
