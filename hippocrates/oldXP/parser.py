import os

import numpy as np

from csxdata import roots
from csxdata.utilities.vectorop import standardize
from csxdata.utilities.highlevel import image_sequence_to_array as pull_data
from csxdata.utilities.highlevel import autoencode

floatX = "float32"


def parse_one(pics_root, std=False, autoenc=0):
    X = np.array(pull_data(pics_root)).astype(floatX)
    if X.shape[0] > 160:
        print("Adjusted to 160")
    X = X[-160:]
    if std or autoenc:
        X = standardize(X)
        if autoenc:
            X = autoencode(X, autoenc)
    # print("{} ARRAY SHAPE: {}".format(pics_root, X.shape))
    return X.reshape([1] + list(X.shape))


def parse_all(hipporoot, sequence="postCM", dump=None):
    posroot = hipporoot + "00Pos/"
    negroot = hipporoot + "00Neg/"
    pX = np.array(
        [parse_one(posroot + casename + "/" + sequence + "/", std=True)
         for casename in sorted(os.listdir(posroot))])
    nX = np.array(
        [parse_one(negroot + casename + "/" + sequence + "/", std=True)
         for casename in sorted(os.listdir(negroot))])
    X = np.concatenate((pX, nX)).astype(floatX)
    # X = X[..., :160, :440, :480]
    y = np.concatenate((np.ones(pX.shape[0]), np.zeros(nX.shape[0])))
    labl = []
    for i, name in enumerate(os.listdir(posroot) + os.listdir(negroot)):
        istr = str(i + 1)
        labl.append("S{}".format("0"*(2-len(istr)) + istr))
        print("{}: {}".format(labl[-1], name))

    if dump is None:
        return X, y, labl
    else:
        print("Dumping to {}".format(dump))
        import pickle
        with open(dump, "wb") as outfl:
            pickle.dump((X, y, labl), outfl)
            outfl.close()

if __name__ == '__main__':
    parse_all(roots["raw"] + "Project_Hippocrates/", dump=roots["raw"] + "Project_Hippocrates/X_y_headers.pkl")
    print("Finite Incantatum...")
