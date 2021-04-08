import numpy as np


# http://www.zsk.iiar.pwr.edu.pl/zsk/repository/dydaktyka/ioc/laboratorium_zaoczne/tw_cwiczenie_3.pdf

def rgb2yuv(rgb):
    m = np.array([[0.299, 0.587, 0.114],
                  [-0.147, -0.289, 0.436],
                  [0.615, -0.515, -0.100]])

    return np.dot(rgb, m.T.copy())


def yuv2rgb(yiq):
    m = np.array([[1, 0, 1.14],
                  [1, -0.395, -0.581],
                  [1, 2.032, 0]])
    return np.dot(yiq, m.T.copy())
