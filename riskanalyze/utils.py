import numpy as np

from SciProjects.riskanalyze import projectroot


def pull_data():
    with open(projectroot + "olajok.csv") as handle:
        chain = handle.read()
    lines = np.array([line.split("\t") for line in chain.split("\n")[:-1]])
    data = lines[1:, 1:]
    coords = data[:, -2:]
    data = data[:, :-2]
    return coords, data
