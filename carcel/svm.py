from generic import *


def experiment():
    from sklearn.svm import SVC

    svm = SVC()
    data = pull_data(0.0)
    X, y = data.table("learning")

    svm.fit(X, data.lindeps)

    samples = pull_samples()
    preds = svm.predict(samples[0])

    for prd, lbl in zip(preds, samples[1]):
        print("SVM prediction for {}: {}".format(lbl[0], "Foreign" if prd else "HUN"))

if __name__ == '__main__':
    experiment()

