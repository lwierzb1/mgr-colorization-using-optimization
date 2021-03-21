import numpy as np
import cv2


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def load_image(path):
    return cv2.imread(path)


original_path = '8_bw.bmp'
#template_path = '9_bw_sp_gauss'
print(mse(load_image(original_path), load_image('8_bw_overexposed.bmp')))
print(mse(load_image(original_path), load_image('8_bw_underexposed.bmp')))
print(mse(load_image(original_path), load_image('8_bw_overexposed_normalized.bmp')))
print(mse(load_image(original_path), load_image('8_bw_underexposed_normalized.bmp')))

#for j in range(1, 8,2):
#    jacobi = template_path + str(j) + '.bmp'
#    mse_result = mse(load_image(original_path), load_image(jacobi))
#    print(mse_result)

