import numpy as np

from csxdata.utilities.highlevel import plot
from csxdata.stats.inspection import category_frequencies

from SciProjects.zsindstat.util import pull_data, axlab_latex


def filter_out(X, Y, unwanted):
    arg = np.argwhere(Y != unwanted).ravel()
    return X[arg], Y[arg]


frame = pull_data("FRUIT", filterby="FAM", selection="Pru")

category_frequencies(frame.indeps)

plot(frame.data, frame.indeps, ellipse_sigma=2, axlabels=axlab_latex)
