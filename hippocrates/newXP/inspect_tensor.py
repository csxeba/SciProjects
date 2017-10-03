import numpy as np
from matplotlib import pyplot as plt

from SciProjects.hippocrates import projectroot, dataroot


def pull_and_preprocess_data(path):
    return np.load(path).transpose((0, 1, 4, 3, 2))[:, 0]


def animate():
    data = pull_and_preprocess_data(dataroot + "/Tumor_T2pos.npa")
    plt.ion()
    obj = plt.imshow(data[0, 0, :, :], vmin=0, vmax=255, cmap="hot")
    for tensor in data:
        for pic in tensor:
            obj.set_data(pic)
            plt.pause(0.01)


def create_frames():
    outpath = projectroot + "output/frames/"
    data = pull_and_preprocess_data(dataroot + "/Tumor_T2pos.npa")
    i = 0
    imax = data.shape[0] * data.shape[1]
    for tensor in data:
        for pic in tensor:
            plt.imshow(pic, vmin=0, vmax=255, cmap="magma")
            plt.title("PROJECT HIPPOCRATES: TUMOR +")
            plt.savefig(outpath + f"frame.{i:0>3}.png")
            i += 1
            print(f"{i:>3}/{imax}")


if __name__ == '__main__':
    animate()
