import numpy as np
import pandas as pd

from csxdata.stats import pairwise_T2
from csxdata.utilities.vectorop import drop_lowNs

from SciProjects.vinyard import projectroot
from SciProjects.vinyard.utility import WineData

labels = ["WINEREGION", "CULTIVAR", "YEAR"]
params = ["DH1", "DH2", "D13C", "D18O"]

wd = WineData()

for ycol in labels:
    df = wd.raw[[ycol] + params].dropna()
    X, Y = df[params].as_matrix(), df[ycol].as_matrix()
    Y, X = drop_lowNs(10, Y, X)
    pairwise_T2(X, Y, verbose=False, dumproot=projectroot, xpid=ycol)
