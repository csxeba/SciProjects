import numpy as np
from csxdata import CData

from SciProjects.generic import paths


RUNS = 100


def get_frame(pretreat="std", param=0):
    path, indps = paths["grapes"]
    frame = CData(path, indps, headers=1, feature="borregio", lower=True)
    frame.transformation = (pretreat, param)
    return frame


def naive_bayes_run(frame):
    from sklearn.naive_bayes import GaussianNB

    model = GaussianNB()
    acc = run(model, frame.learning, frame.lindeps,
              frame.testing, frame.tindeps, RUNS)
    print("Naive Bayes accuracy:", acc)


def svc_run(frame):
    from sklearn.svm import SVC

    model = SVC()
    acc = run(model, frame.learning, frame.lindeps,
              frame.testing, frame.tindeps, RUNS)
    print("SVC accuracy:", acc)


def qda_run(frame):
    from sklearn.discriminant_analysis import (
        QuadraticDiscriminantAnalysis as QDA)

    model = QDA()
    acc = run(model, frame.learning, frame.lindeps,
              frame.testing, frame.tindeps, RUNS)
    print("QDA accuracy:", acc)


def forest_run(frame):
    from sklearn.ensemble.forest import RandomForestClassifier as RFC

    model = RFC(n_estimators=10)
    acc = run(model, frame.learning, frame.lindeps,
              frame.testing, frame.tindeps, RUNS)
    print("Random Forest accuracy:", acc)


def random_mockery(frame):

    class RandomMocker:
        def fit(self, *args, **kwargs):
            pass

        def predict(self, Y):
            return np.random.choice(frame.categories, Y.shape[:1])

    model = RandomMocker()
    acc = run(model, frame.learning, frame.lindeps,
              frame.testing, frame.tindeps, RUNS)
    print("Random Mocker accuracy:", acc)


def run(model, X, Y, vX, vY, runs):
    accs = []
    for r in range(1, runs+1):
        model.fit(X, Y)

        preds = model.predict(vX)
        eq = [left == right for left, right in zip(preds, vY)]
        accuracy = sum(eq) / len(eq)
        accs.append(accuracy)
    return sum(accs) / len(accs)


def full_run(frame):
    random_mockery(frame)
    naive_bayes_run(frame)
    qda_run(frame)
    svc_run(frame)
    forest_run(frame)


def test_pretreatments():
    for treat, arg in zip((None, "std", "pca", "lda", "ica"),
                          (0, 0, 2, 2, 2)):
        print("Data pretreatment is {} ({})".format(treat, arg))
        grapes = get_frame(treat, arg)
        full_run(grapes)


if __name__ == '__main__':
    test_pretreatments()
