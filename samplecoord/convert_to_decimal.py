import numpy as np
import pandas as pd

from SciProjects.samplecoord import projectroot


def do1(ar):
    for i, crd in enumerate(ar):
        if ";" not in crd:
            continue
        sepd = crd.split(";")

        ar[i] = float(sepd[0]) + float(sepd[1]) / 60.
        if len(sepd) == 3:
            ar[i] += float(sepd[-1]) / 3600
        elif len(sepd) > 3:
            raise RuntimeError(f"Unexpected coordinate in X: {crd}")
    return ar


df = pd.read_excel(projectroot + "coords.xlsx")
X, Y = df["GPSX"].tolist(), df["GPSY"].tolist()
X, Y = map(do1, (X, Y))
pd.DataFrame(data=np.stack((X, Y), axis=1), columns=["GPSX", "GPSY"]).to_excel(projectroot + "output.xlsx")
