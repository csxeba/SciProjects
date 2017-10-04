import numpy as np
import pandas as pd
from scipy.spatial.distance import mahalanobis

from SciProjects.riskanalyze import projectroot

allhead = []
param = ["MA", "DATUM", "HELY", "HIVATAL", "MEGJ", "TIPUS", "SŰR", "VISZK", "LOBP", "D350", "FAME"]

df = pd.read_excel(projectroot + "OlajMinden.xlsx")
frame = df[param]
data = frame.loc[:, "SŰR":"FAME"].dropna().as_matrix()

center = data.mean(axis=0)
cov = np.cov(data.T)
icov = np.linalg.inv(cov)
D = np.zeros(len(data))

for i, record in enumerate(data):
    D[i] = mahalanobis(record, center, icov)

frame["D"] = D
frame.to_excel(projectroot + "MahalD.xlsx")
