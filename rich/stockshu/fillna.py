import numpy as np
import pandas as pd

from SciProjects.rich import projectroot


df = pd.read_excel(projectroot + "SparseInput.xlsx")  # type: pd.DataFrame

M, N = df.shape

lastnum = 0.
for c in range(1, N):
    for r in range(M):
        val = df.iloc[r, c]
        if np.isnan(val):
            df.iloc[r, c] = lastnum
        else:
            lastnum = val

df.to_excel(projectroot + "Filled.xlsx")
