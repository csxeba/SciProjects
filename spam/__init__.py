import os

import numpy as np

projectroot = os.path.expanduser("~/SciProjects/Project_Spam/")


def pull_data():
    edim = 300
    ydim = 50
    samples = 64

    mat = np.zeros((samples, edim, ydim, 1))
    Y = np.zeros((samples,))

    s = 0
    y = 0
    for line in open(projectroot+"spamdata.txt"):
        if line[0:6] == "label=":
            s += 1
            Y[s - 1] = int(line[6])
            y = 0
        else:
            c = 0
            for x in line.strip().split(" ", edim):
                mat[s - 1][c][y][0] = float(x)
                c += 1
            y += 1
    return mat, Y[:, None]
