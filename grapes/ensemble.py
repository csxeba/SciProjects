# from sklearn.ensemble import AdaBoostClassifier as Boost
from sklearn.ensemble.bagging import BaggingClassifier as Boost
from sklearn.naive_bayes import GaussianNB

from csxdata import CData

from SciProjects.grapes import path, indepsn


if __name__ == '__main__':

    data = CData(path, indepsn, feature="evjarat", headers=1, cross_val=0.2, lower=True)
    data.transformation = "std"
    model = Boost(GaussianNB(), n_estimators=100)

    model.fit(data._learning, data.lindeps)
    preds = model.predict(data._testing)
    eq = [left == right for left, right in zip(preds, data.tindeps)]
    print("Acc:", sum(eq) / len(eq))
