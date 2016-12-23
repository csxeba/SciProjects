import numpy as np

from csxdata import roots

# header: EURODAT, FAJTA, SZIN, BORREGIO, BORVIDEK, EVJARAT, DH1, DH2, D13C
GRAPESPATH = roots["csvs"] + "grapes.csv"


def pull_data(frame=False, feature="borrégió", filterby=None, selection=None):

    from csxdata import CData
    from csxdata.utilities.parsers import parse_csv

    def feature_name_to_index(featurename):
        try:
            got = {"fajta": 1,
                   "szín": 2,
                   "borrégió": 3,
                   "borvidék": 4,
                   "évjárat": 5}[featurename]
        except IndexError:
            raise IndexError("Unknown feature: {}".format(featurename))
        return got

    def filter_data(*data):
        if selection is None:
            raise ValueError("Please supply a selection argument for filtering!")
        filterindex = feature_name_to_index(filterby)
        filterargs = argfilter(data[1][:, filterindex], selection).ravel()
        return data[0][filterargs], data[1][filterargs]

    def select_classification_feature(feature_matrix):
        nofeature = feature_name_to_index(feature)
        return feature_matrix[:, nofeature]

    X, Y, header = parse_csv(GRAPESPATH, indeps=6, headers=1, shuffle=True, lower=True)
    if filterby is not None:
        X, Y = filter_data(X, Y)

    Y = select_classification_feature(Y)

    if frame:
        return CData((X, Y))

    return X, Y


def stringeq(A, chain):
    return np.array([left == chain for left in A])


def argfilter(argarr, selection):
    if isinstance(selection, str):
        return np.argwhere(stringeq(argarr, selection))
    else:
        return np.argwhere(np.equal(argarr, selection))


def arrfilter(X, Y, argarr, selection):
    args = argfilter(argarr, selection)
    return X[args], Y[args]
