import numpy as np
import pandas as pd

from sklearn.discriminant_analysis import (
    LinearDiscriminantAnalysis as LDA,
    QuadraticDiscriminantAnalysis as QDA
)
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from csxdata.utilities.highlevel import RandomClassifierMock
from csxdata.utilities.vectorop import standardize

from SciProjects.vinyard import projectroot
from SciProjects.vinyard.utility import read_datasets


models = ("mock", "lda", "qda", "gnb", "knn", "forest", "svm", "rbf-svm", "poly3-svm")
categs = ("WINEREGION", "CULTIVAR", "YEAR")


def split(X, Y, ratio=0.1):
    N = len(Y)
    arg = np.arange(N)
    np.random.shuffle(arg)
    m = int(N*ratio)
    targ, larg = arg[:m], arg[m:]
    lX, lY, tX, tY = X[larg], Y[larg], X[targ], Y[targ]
    lX, (mu, sigma) = standardize(lX, return_factors=True)
    tX = standardize(tX, mean=mu, std=sigma)
    return lX, lY, tX, tY


def get_model(modelname):
    return {
        "mock": lambda: RandomClassifierMock(),
        "lda": lambda: LDA(), "qda": lambda: QDA(),
        "logistic": lambda: LogisticRegression(),
        "gnb": lambda: GaussianNB(),
        "knn": lambda: KNeighborsClassifier(),
        "forest": lambda: RandomForestClassifier(),
        "svm": lambda: SVC(kernel="linear"),
        "rbf-svm": lambda: SVC(kernel="rbf"),
        "poly3-svm": lambda: SVC(kernel="linear", degree=3)
    }[modelname]()


def run_experiment(modelname, ycol, repeats=100):
    X, Y = read_datasets(ycol, dropthresh=10)
    accs = []
    for r in range(repeats):
        lX, lY, tX, tY = split(X, Y, 0.1)
        model = get_model(modelname)
        model.fit(lX, lY)
        # noinspection PyTypeChecker
        accs.append(np.mean(model.predict(tX) == tY))
    macc = np.mean(accs)
    print(f"{modelname.upper()} on {ycol}: {macc:.2%}")
    return macc


def main():
    pd.DataFrame(data=np.array([[run_experiment(mname, ycol) for mname in models] for ycol in categs]).T,
                 index=models, columns=categs).to_excel(projectroot + "statmodels.xlsx")


if __name__ == '__main__':
    main()
