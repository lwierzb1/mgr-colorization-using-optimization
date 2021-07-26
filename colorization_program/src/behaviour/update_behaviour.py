__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from colorization_program.src.colorization_algorithm.colorization_using_optimization.image.colorization_postprocessor import \
    ColorizationPostprocessor
from colorization_program.src.colorization_algorithm.colorization_using_optimization.image.colorization_preprocessor import \
    ColorizationPreprocessor
from colorization_program.src.colorization_algorithm.colorization_using_optimization.image.cuo_async_task import \
    CUOAsyncTask
from colorization_program.src.colorization_algorithm.colorization_using_optimization.image.update_grid import UpdateGrid


class UpdateBehaviour:
    def __init__(self, matrix, pencil_config_subject):
        self._GRID_SIZE_ROW = 100
        self._GRID_SIZE_COLUMN = 100
        self._pencil_config_subject = pencil_config_subject
        self._main_grid = self._create_grid(matrix)
        self.cells = set()
        self._colorization_preprocessor = ColorizationPreprocessor(pencil_config_subject)
        self._colorization_postprocessor = ColorizationPostprocessor()
        self._cuo_task = CUOAsyncTask()
        self._mbb = None

    def on_click(self, e):
        cells_to_update = self._main_grid.on_click(e)
        self.cells.add(cells_to_update)

    def on_motion(self, e):
        cells_to_update = self._main_grid.on_click(e)
        self.cells.add(cells_to_update)

    def perform_colorize(self, bw, color):
        self._mbb, input_matrices = self._colorization_preprocessor.prepare_input_for_colorization(self.cells, bw,
                                                                                                   color)
        self._cuo_task.run(input_matrices)

    def check_for_result(self):
        result_candidate = self._cuo_task.result()
        if result_candidate is not None:
            self.cells.clear()
            return self._main_grid.col_index_to_pixel_format(self._mbb[0]), \
                   self._main_grid.row_index_to_pixel_format(self._mbb[1]), \
                   result_candidate
        else:
            return None

    def _create_grid(self, matrix):
        grid = UpdateGrid(matrix, self._GRID_SIZE_ROW, self._GRID_SIZE_COLUMN)
        self._pencil_config_subject.attach(grid.pencil_config_observer)
        return grid
