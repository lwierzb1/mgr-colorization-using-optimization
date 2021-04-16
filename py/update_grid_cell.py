class UpdateGridCell:
    def __init__(self, matrix):
        self.matrix = matrix

    def check_if_needs_update(self):
        return abs(self.matrix).sum(2) > 0.01

    def width(self):
        return self.matrix.shape[1]

    def height(self):
        return self.matrix.shape[0]
