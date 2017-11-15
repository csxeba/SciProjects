import numpy as np

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA, QuadraticDiscriminantAnalysis as QDA
from sklearn.naive_bayes import GaussianNB as GNB
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.svm import SVC

from SciProjects.fruits.fruitframe import FruitData

df = FruitData(transform=True)
X = df.volatile.as_matrix()
X -= X.mean(axis=0)
X /= X.std(axis=0)
y = df["FAMILIA"].as_matrix()


def get_data(split=0.1):
    arg = np.arange(len(X))
    np.random.shuffle(arg)
    m = int(len(X) * split)
    targ = arg[:m]
    larg = arg[m:]
    return X[targ], y[targ], X[larg], y[larg]


def get_model(name):
    return {
        "lda": LDA(), "qda": QDA(), "gnb": GNB(), "knn": KNN(),
        "svm": SVC(kernel="linear"), "rbf svm": SVC(kernel="rbf"),
        "poly svm": SVC(kernel="poly", degree=3)
    }[name]


def xperiment(modelname, repeat=100):
    accs = []
    for r in range(repeat):
        lX, lY, tX, tY = get_data()
        model = get_model(modelname)
        model.fit(lX, lY)
        # noinspection PyTypeChecker
        accs.append(np.mean(model.predict(tX) == tY))
    print(f"{modelname} mean accuracy: {np.mean(accs):.2%}")


if __name__ == '__main__':
    for mn in ("lda", "qda", "gnb", "knn", "svm", "rbf svm", "poly svm"):
        print("RUNNING", mn.upper())
        xperiment(mn, repeat=100)
