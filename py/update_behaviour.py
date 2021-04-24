from colorization_postprocessor import ColorizationPostprocessor
from colorization_preprocessor import ColorizationPreprocessor
from image_colorizer_multiprocess import ImageColorizerMultiprocess
from update_grid import UpdateGrid


class UpdateBehaviour:
    def __init__(self, matrix, pencil_config_subject):
        self.__GRID_SIZE_ROW = 100
        self.__GRID_SIZE_COLUMN = 100
        self.__pencil_config_subject = pencil_config_subject
        self._main_grid = self.__create_grid(matrix)
        self.cells = set()
        self.__colorization_preprocessor = ColorizationPreprocessor(pencil_config_subject)
        self.__colorization_postprocessor = ColorizationPostprocessor()

    def on_click(self, e):
        cells_to_update = self._main_grid.on_click(e)
        self.cells.add(cells_to_update)

    def on_motion(self, e):
        cells_to_update = self._main_grid.on_click(e)
        self.cells.add(cells_to_update)

    def perform_colorize(self, bw, color):
        mbb, input_matrices = self.__colorization_preprocessor.prepare_input_for_colorization(self.cells, bw, color)
        colorizer = ImageColorizerMultiprocess(input_matrices[0], input_matrices[1])
        result = colorizer.colorize()

        self.cells.clear()
        return self._main_grid.col_index_to_pixel_format(mbb[0]), \
               self._main_grid.row_index_to_pixel_format(mbb[1]), \
               result

    def __create_grid(self, matrix):
        grid = UpdateGrid(matrix, self.__GRID_SIZE_ROW, self.__GRID_SIZE_COLUMN)
        self.__pencil_config_subject.attach(grid.pencil_config_observer)
        return grid
