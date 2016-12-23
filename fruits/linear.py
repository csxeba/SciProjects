from sklearn.svm import SVC

from csxdata import CData

from project_fruits.util import pull_data, pull_validation_data

TAXLEVEL = "familia"
RUNS = 100
PRETREATMENT = "raw"
AFTER_TREATMENT = "std"
TRANSFORM_PARAM = 0
CROSSVAL = .3


def svm():

    def evaluate(X, y):
        preds = model.predict(X)
        eq = [preds[i] == y[i] for i in range(len(preds))]
        return sum(eq) / len(eq)

    def get_data():
        data = CData(pull_data(label=TAXLEVEL, transformation=None, param=TRANSFORM_PARAM),
                     cross_val=CROSSVAL)
        data.transformation = AFTER_TREATMENT
        lX, lY = data.learning, data.lindeps
        tX, tY = data.testing, data.tindeps
        vX, vY = pull_validation_data(TAXLEVEL)
        vX = data.transform(vX)
        return lX, lY, tX, tY, vX, vY

    Xs, Ys, testX, testY, valX, valY = get_data()

    model = SVC(C=1.0, kernel="rbf")
    model.fit(Xs, Ys)

    tacc = evaluate(testX, testY)
    vacc = evaluate(valX, valY)

    print("T: {}\tV: {}".format(tacc, vacc))

    return tacc, vacc, model


if __name__ == '__main__':
    taccs, vaccs = [], []
    for run in range(RUNS):
        tc, vc, _ = svm()
        taccs.append(tc)
        vaccs.append(vc)

    print("Final result:")
    print("Accuracy on testing:", sum(taccs) / len(taccs))
    print("Accuracy on validation:", sum(vaccs) / len(vaccs))
