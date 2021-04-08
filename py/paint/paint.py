from tkinter import *

import cv2
import numpy as np
from Example import Example
from display_canvas import DisplayCanvas
from py.paint.drawing_canvas import DrawingCanvas

if __name__ == '__main__':
    root = Tk()
    img = cv2.imread('../../test_hd/1_bw.bmp')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    y, _, _ = cv2.split(img)
    # y = cv2.resize(y, (100, 100))

    arrays = np.array_split(y, 2, axis=1)
    for i in range(len(arrays)):
        arrays[i] = np.array_split(arrays[i], 4, axis=0)

    sd = DisplayCanvas(root, arrays)
    sd.pack(side=RIGHT, padx=4, pady=4)

    d = DrawingCanvas(root, y, sd)
    d.pack(side=LEFT, padx=4, pady=4)
    #

    root.mainloop()
