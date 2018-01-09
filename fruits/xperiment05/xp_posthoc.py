import numpy as np
import pandas as pd

from SciProjects.fruits.xperiment05.util import pull_data, projectroot

from csxdata.stats import pairwise_T2
from csxdata.utilities.vectorop import drop_lowNs


df = pull_data("FAMILIA")
X, Y = df.as_matrix(["DH1", "DH2", "D13C"]), df["FAMILIA"].as_matrix()
Y, X = drop_lowNs(10, Y, X)

pairwise_T2(X, Y, dumproot=projectroot, xpid="Fruit_GEO")
