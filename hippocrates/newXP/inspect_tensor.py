import os

import numpy as np

from matplotlib import pyplot as plt


data = np.load(os.path.expanduser("~/Prog/data/mr/SM_T2pos.npa"))
data = data.transpose((0, 3, 2, 1, 4))
data = data[:, ::2, ::2, :, 0]

plt.ion()
obj = plt.imshow(data[0, :, :, 0], vmin=0, vmax=155, cmap="hot")

fix, fadder = 0, 1
six, sadder = 0, 1
for six in range(len(data)):
    for fix in range(data.shape[-1]):
        obj.set_data(data[six, :, :, fix])
        fix += fadder
        if fix == data.shape[-2] or fix == -1:
            fadder *= -1
            fix += fadder
        plt.pause(0.01)
