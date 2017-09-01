import os

import numpy as np

projectroot = os.path.expanduser("~/SciProjects/Project_Glycerol/")


def pull_data(concat=False):
    xdata = np.array([line.split(";") for line in open(projectroot + "xuemin.csv").read().split("\n") if len(line) > 1])
    assert xdata.ndim == 2
    X = xdata[1:, 1:]
    cdata = np.array([line.split(";") for line in open(projectroot + "cabanero.csv").read().split("\n") if len(line) > 1])
    assert cdata.ndim == 2
    csplit = cdata[1:, (2, 4)]
    if concat:
        out = np.concatenate((csplit, X))
        return out.astype(float)
    return csplit.astype(float), X.astype(float)
