import pandas as pd

from csxdata.utilities.vectorop import drop_lowNs
from SciProjects.vinyard.structure import WineData


def read_datasets(ycol="WINEREGION", dropthresh=0):
    wd = WineData()
    df = wd.raw[[ycol, "DH1", "DH2", "D13C", "D18O"]].dropna()  # type: pd.DataFrame
    X, Y = df[["DH1", "DH2", "D13C", "D18O"]].as_matrix(), df[ycol].as_matrix()
    if dropthresh:
        Y, X = drop_lowNs(dropthresh, Y, X)
    return X, Y


def main():
    X, Y = read_datasets()
    print(f"X: {X.shape}, Y: {Y.shape}, categY: {len(set(Y))}")


if __name__ == "__main__":
    main()
