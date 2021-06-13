import observer


class ColorizedImageObserver(observer.Observer):
    def __init__(self):
        self.x_start = None
        self.y_start = None
        self.result = None

    def update_subject(self, **kwargs):
        self.x_start = kwargs.get('x_start')
        self.y_start = kwargs.get('y_start')
        self.result = kwargs.get('result')
