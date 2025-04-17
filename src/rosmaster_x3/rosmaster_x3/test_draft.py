import numpy as np
import cv2

image_dir = '/home/ica/auto_parking/image.npy'
image = np.load(image_dir)
cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
