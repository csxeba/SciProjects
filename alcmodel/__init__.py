import os

import numpy as np
import pandas as pd

projectroot = os.path.expanduser("~/SciProjects/Project_alcmodel/")


def get_reference():
    return pd.read_excel(projectroot + "points.xlsx")


def get_model(deg=2, data=None):
    data = get_reference() if data is None else data
    X, Y = data["VV"], data["DENSE20"]
    curve = np.poly1d(np.polyfit(X, Y, deg=deg))
    R = np.corrcoef(X, curve(X))[0][1]
    print(f"Fitted {deg} degree LS curve with R2 = {R**2}")
    return curve


def convert(vv, model=None):
    if model is None:
        model = get_model(2)
    return model(vv)
