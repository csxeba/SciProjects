import numpy as np
import pandas as pd
from keras.optimizers import SGD

from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

import keras
from keras.models import Sequential
from keras.layers import Dense, BatchNormalization, Dropout, Activation

from csxdata.utilities.vectorop import shuffle

from SciProjects.matt import projectroot


def get_data(dummycode=False):
    df = pd.read_excel(projectroot + "adat.xlsx", header=0)
    X, Y = df.iloc[:, 1:].as_matrix(), df["GYUM"].as_matrix()
    if dummycode:
        categ = dict(enumerate(np.unique(Y)))
        categ.update({v: k for k, v in categ.items()})
        Y = np.array([categ[y] for y in Y])
    return X, Y


def run_model(model, name, X, Y):
    acc = []
    print("-"*50)
    for rep in range(1, 1001):
        print(f"\r{name} repeat {rep:>3}/1000", end="")
        X, Y = shuffle(X, Y)
        tX, tY = X[:5], Y[:5]
        lX, lY = X[5:], Y[5:]
        model.fit(lX, lY)
        pred = model.predict(tX)
        acc.append((pred == tY).sum() / len(tX))
    print()
    print(f"{name} acc of 1000 runs:")
    print("MEAN:", sum(acc)/len(acc))
    print("MIN: ", min(acc))
    print()


def run_ann():
    X, y = get_data(dummycode=True)
    X = keras.utils.normalize(X)
    Y = keras.utils.to_categorical(y)
    acc = [0]
    for rep in range(100):
        print(f"\rRepeat {rep}/100, last: {acc[-1]}", end="")
        X, Y = shuffle(X, Y)
        ann = Sequential([
            Dense(units=15, input_dim=X.shape[-1]), Activation("tanh"),
            Dense(units=Y.shape[-1]), Activation("softmax")
        ])
        ann.compile(optimizer=SGD(momentum=0.9), loss="categorical_crossentropy", metrics=["acc"])
        hist = ann.fit(X, Y, batch_size=len(X), epochs=50, verbose=0, validation_split=0.3)
        acc.append(hist.history["val_acc"][-1])
    print()
    print(sum(acc[1:]) / len(acc)-1)


def main():
    models = [QDA(), GaussianNB(), SVC(), RandomForestClassifier()]
    X, Y = get_data()
    for model in models:
        run_model(model, model.__class__.__name__, X, Y)


if __name__ == '__main__':
    run_ann()
