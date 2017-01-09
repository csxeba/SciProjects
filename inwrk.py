import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import binary_fill_holes
from skimage.feature import canny

from csxdata import roots

from SciProjects.imaging import pull_data


def inspect_histogram(pic):
    for data, channel in zip(pic.T, ("red", "green", "blue")):
        print("Channel:", channel)
        yield np.histogram(data, bins=20), channel


def segment_by_edge_detection(pic):
    edges = canny(pic.T[0] / 255.)
    return edges

if __name__ == '__main__':
    for pic in pull_data():
        plt.imshow(segment_by_edge_detection(pic))
        plt.show()
