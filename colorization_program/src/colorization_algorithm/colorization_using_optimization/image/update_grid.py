__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import numpy as np

from colorization_program.src.colorization_algorithm.colorization_using_optimization.image.update_grid_cell import \
    UpdateGridCell
from colorization_program.src.observer.pencil_config_observer import PencilConfigObserver


class UpdateGrid:
    def __init__(self, matrix, number_of_cells_x, number_of_cells_y):
        self.shape = (number_of_cells_y, number_of_cells_x)
        self._grid = np.empty(shape=self.shape, dtype=np.object)
        self._init_pencil_config_observer()
        self._init_matrix(matrix)
        self._split_matrix()

    def on_click(self, e):
        flood_width = self._get_pencil_width() + int(self._grid[0][0].width() / 2)
        flood_height = self._get_pencil_width() + int(self._grid[0][0].height() / 2)

        y_start, x_start, = self._resolve_nearest_cells(e, - flood_width,
                                                        - flood_height)

        y_stop, x_stop, = self._resolve_nearest_cells(e, flood_width,
                                                      flood_height)

        return x_start, y_start, x_stop, y_stop

    def get_sub_array(self, x_start, y_start, x_stop, y_stop):
        merged_rows = None
        for r in range(y_start, y_stop + 1):
            merged_columns = self._merge_columns_in_row(r, x_start, x_stop)
            if merged_rows is None:
                merged_rows = merged_columns
            else:
                merged_rows = np.concatenate([merged_rows, merged_columns])
        return merged_rows

    def row_index_to_pixel_format(self, r_idx):
        pixel_row = 0
        for i in range(r_idx):
            pixel_row += self._grid[i][0].height()
        return pixel_row

    def col_index_to_pixel_format(self, c_idx):
        pixel_col = 0
        for i in range(c_idx):
            pixel_col += self._grid[0][i].width()
        return pixel_col

    def _resolve_nearest_cells(self, e, offset_x=0, offset_y=0):
        x = e.x
        y = e.y
        if e.x + offset_x >= 0:
            x = e.x + offset_x
        if e.y + offset_y >= 0:
            y = e.y + offset_y

        row_index = self._get_row_index_to_update(y)
        column_index = self._get_column_index_to_update(x)
        return row_index, column_index

    def _merge_columns_in_row(self, r_idx, c_start, c_stop):
        merged_columns = None
        for c in range(c_start, c_stop + 1):
            if merged_columns is None:
                merged_columns = self._grid[r_idx][c].matrix
            else:
                merged_columns = np.hstack([merged_columns, self._grid[r_idx][c].matrix])
        return merged_columns

    def _get_column_index_to_update(self, x):
        gained_width = 0
        for c in range(self.shape[1]):
            gained_width += self._grid[0][c].width()
            if gained_width >= x:
                return c

    def _get_row_index_to_update(self, y):
        gained_height = 0
        for r in range(self.shape[0]):
            gained_height += self._grid[r][0].height()
            if gained_height >= y:
                return r

    def _init_matrix(self, matrix):
        self._matrix = matrix.copy()

    def _split_matrix(self):
        x_cells = self.shape[0]
        y_cells = self.shape[1]

        x_arrays = np.array_split(self._matrix, x_cells)
        for x_index in range(x_cells):
            xy_arrays = np.array_split(x_arrays[x_index], y_cells, axis=1)
            for y_index in range(y_cells):
                self._grid[x_index][y_index] = UpdateGridCell(xy_arrays[y_index])

    def _init_pencil_config_observer(self):
        self.pencil_config_observer = PencilConfigObserver()

    def _get_pencil_width(self):
        return int(float(self.pencil_config_observer.width))
