import numpy as np
import pandas as pd

from SciProjects.rich import projectroot


def pull_data(rescale=True, crossval=0.1, shuffle=False):
    df = pd.read_excel(projectroot + "Filled.xlsx")

    stocks = df.as_matrix().astype(float)
    if rescale:
        stocks /= stocks.max(axis=0)
        stocks -= stocks.mean(axis=0, keepdims=True)

        arg = np.arange(len(stocks))
        if shuffle:
            np.random.shuffle(arg)
        return stocks[arg[crossval:]], stocks[arg[crossval:]]

    return stocks, df.columns
