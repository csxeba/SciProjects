import numpy as np

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.naive_bayes import GaussianNB as GNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from csxdata.utilities.vectorop import separate_validation

from SciProjects.fruits.fruitframe import FruitData


class ClassifierMock:

    def __init__(self):
        self.X, self.Y = None, None

    def fit(self, X, Y):
        self.X, self.Y = X, Y

    def predict(self, X, Y=None):
        del Y
        return np.random.choice(self.Y, len(X))


def load_dataset(feature, dset=None):
    df = FruitData(transform=True)
    X = {"volatile": df.volatile.as_matrix(),
         "isotope": df.isotope.as_matrix(),
         None: df.X.as_matrix()}[dset]
    X = (X - X.mean(axis=0)) / X.std(axis=0)
    y = df[feature].as_matrix()
    return X, y


def get_model(name):
    return {
        "mock": ClassifierMock(), "lda": LDA(), "qda": QDA(), "gnb": GNB(), "knn": KNN(),
        "forest": RandomForestClassifier(), "logistic": LogisticRegression(class_weight="balanced"),
        "svm": SVC(kernel="linear", class_weight="balanced"),
    }[name]


def xperiment(modelname, X, Y, repeat=100):
    acc = []
    for rep in range(repeat):
        lX, lY, tX, tY = separate_validation(0.1, X, Y, balanced=True, nowarning=True)
        model = get_model(modelname)
        model.fit(lX, lY)
        acc.append(np.mean(model.predict(tX) == tY))
    return np.mean(acc)


def main():
    X, y = load_dataset(feature="GYUM", dset=None)
    for mn in ("mock", "lda", "qda", "gnb", "knn", "forest", "svm", "logistic"):
        acc = xperiment(mn, X, y, repeat=100)
        print(f"{mn.upper()} accuracy: {acc:.2%}")


if __name__ == '__main__':
    main()
