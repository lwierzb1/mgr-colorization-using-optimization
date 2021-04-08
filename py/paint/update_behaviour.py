class UpdateBehaviour:
    def __init__(self, width, height):
        self.__PARTS_X = 2
        self.__PARTS_Y = 4
        self.__WIDTH = width
        self.__HEIGHT = height
        self.__X_STEP = self.__WIDTH / self.__PARTS_X
        self.__Y_STEP = self.__HEIGHT / self.__PARTS_Y
        self.canvas_coordinates_to_update = set()

    def analyze(self, e):
        event_x = e.x
        event_y = e.y

        if 0 <= event_x <= self.__WIDTH and 0 <= event_y <= self.__HEIGHT:
            x_id = self.__get_x_id(event_x)
            y_id = self.__get_y_id(event_y)
            self.canvas_coordinates_to_update.add((x_id, y_id))

    def __get_x_id(self, event_x):
        for i in range(self.__PARTS_X):
            if event_x < self.__X_STEP * (i + 1):
                return i

    def __get_y_id(self, event_y):
        for i in range(self.__PARTS_Y):
            if event_y < self.__Y_STEP * (i + 1):
                return i

    def clear(self):
        self.canvas_coordinates_to_update.clear()
