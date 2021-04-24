import cv2
import numpy as np

from pencil_config_observer import PencilConfigObserver
from update_grid_cell import UpdateGridCell


class UpdateGrid:
    def __init__(self, matrix, number_of_cells_x, number_of_cells_y):
        self.shape = (number_of_cells_y, number_of_cells_x)
        self._grid = np.empty(shape=self.shape, dtype=np.object)
        self.__init_pencil_config_observer()
        self.__init_matrix(matrix)
        self.__split_matrix()

    def on_click(self, e):
        flood_width = self.__get_pencil_width() + int(self._grid[0][0].width() / 2)
        flood_height = self.__get_pencil_width() + int(self._grid[0][0].height() / 2)
        # flood_width = 0
        # flood_height = 0

        y_start, x_start, = self.__resolve_nearest_cells(e, - flood_width,
                                                         - flood_height)

        y_stop, x_stop, = self.__resolve_nearest_cells(e, flood_width,
                                                       flood_height)

        # ret = self.__merge_array_rows(x_start, y_start, x_stop, y_stop)
        return x_start, y_start, x_stop, y_stop

    def __resolve_nearest_cells(self, e, offset_x=0, offset_y=0):
        x = e.x
        y = e.y
        if e.x + offset_x >= 0:
            x = e.x + offset_x
        if e.y + offset_y >= 0:
            y = e.y + offset_y

        row_index = self.__get_row_index_to_update(y)
        column_index = self.__get_column_index_to_update(x)
        return row_index, column_index

    def get_sub_array(self, x_start, y_start, x_stop, y_stop):
        merged_rows = None
        for r in range(y_start, y_stop + 1):
            merged_columns = self.__merge_columns_in_row(r, x_start, x_stop)
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

    def __merge_columns_in_row(self, r_idx, c_start, c_stop):
        merged_columns = None
        for c in range(c_start, c_stop + 1):
            if merged_columns is None:
                merged_columns = self._grid[r_idx][c].matrix
            else:
                merged_columns = np.hstack([merged_columns, self._grid[r_idx][c].matrix])
        return merged_columns

    def __get_column_index_to_update(self, x):
        gained_width = 0
        for c in range(self.shape[1]):
            gained_width += self._grid[0][c].width()
            if gained_width >= x:
                return c

    def __get_row_index_to_update(self, y):
        gained_height = 0
        for r in range(self.shape[0]):
            gained_height += self._grid[r][0].height()
            if gained_height >= y:
                return r

    def __init_matrix(self, matrix):
        self.__matrix = matrix

    def __split_matrix(self):
        x_cells = self.shape[0]
        y_cells = self.shape[1]

        x_arrays = np.array_split(self.__matrix, x_cells)
        for x_index in range(x_cells):
            xy_arrays = np.array_split(x_arrays[x_index], y_cells, axis=1)
            for y_index in range(y_cells):
                self._grid[x_index][y_index] = UpdateGridCell(xy_arrays[y_index])

    def __init_pencil_config_observer(self):
        self.pencil_config_observer = PencilConfigObserver()

    def __get_pencil_width(self):
        return int(self.pencil_config_observer.width)
