import numpy as np

from SciProjects.riskanalyze import projectroot


def pull_data(filename):
    with open(projectroot + filename) as handle:
        chain = handle.read()
    lines = np.array([line.split("\t") for line in chain.split("\n")[:-1]])
    data = lines[1:, 1:]
    coords = data[:, -2:].astype(float)
    data = data[:, :-2]
    return coords, data


def rescale(xy, sxy=None):
    xymin = xy.min(axis=0) if sxy is None else sxy.min(axis=0)
    xymax = xy.max(axis=0) if sxy is None else sxy.max(axis=0)
    return xy - xymin / xymax - xymin