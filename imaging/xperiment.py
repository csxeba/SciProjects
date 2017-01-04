from time import sleep

import numpy as np

from matplotlib import pyplot as plt
from skimage.filters import sobel
from scipy.ndimage import binary_fill_holes

from SciProjects.imaging import pull_data

pics = pull_data()

# R-G-B
THRESHOLDS = [1.75, 0.6, 0.6]


def binarize(ar):
    channel_averages = ar.mean(axis=(0, 1)) * THRESHOLDS
    tmp = np.greater_equal(ar, channel_averages[None, None, :]).sum(axis=2)
    # tmp = np.sum(tmp, axis=2)
    return np.greater_equal(tmp, 3)


bins = (binarize(pic) for pic in pics)
filled = (binary_fill_holes(bind) for bind in bins)
edged = (sobel(fl) for fl in filled)

plt.ion()
obj = None
for i, pic in enumerate(filled, start=1):
    print("Doing pic", i)
    if obj is None:
        obj = plt.matshow(np.zeros_like(pic))
        plt.show()
    obj.set_data(pic)
    sleep(10)
