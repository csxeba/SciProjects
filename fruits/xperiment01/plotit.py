import numpy as np

from csxdata.utilities.parser import parse_csv
from csxdata.utilities.highlevel import plot, transform

from SciProjects.fruits import gyumpath, gyumindeps

ELLIPSE = True
ELLIPSE_SIGMA = 2

axlb = {
    "raw": ("DH1", "DH2", "D13C"),
    "log": ("logDH1", "logDH2", "D13C"),
    "sqrt": ("sqrtDH1", "sqrtDH2", "D13C"),
    "sigm": ("sigmDH1", "D13C"),
    "pca": ("PC01", "PC02", "PC03"),
    "ica": ("IC01", "IC02", "IC03"),
    "lda": ("LD01", "LD02", "LD03"),
    "sinu": ("sinDH1", "sinDH2", "D13C"),
    "fft": ("fftDH1", "fftDH2", "D13C"),
    "ae": ("AE1", "AE2", "AE3")
}


def fruits_xperiment(transformation, param):
    X, y, header = parse_csv(gyumpath, gyumindeps, feature="Species", absval=True)
    lX = transform(X, factors=param, get_model=False, method=transformation, y=y)
    plot(lX, np.vectorize(lambda x: x[:4])(y),
         axlabels=axlb[transformation],
         ellipse_sigma=ELLIPSE_SIGMA)


if __name__ == '__main__':
    fruits_xperiment("raw", None)
