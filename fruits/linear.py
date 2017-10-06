from sklearn.svm import SVC

from csxdata import CData

from SciProjects.fruits import gyumpath, gyumindeps, zsindpath, zsindeps

TAXLEVEL = "Familia"
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
        fruits = CData(gyumpath, gyumindeps, feature=TAXLEVEL, cross_val=CROSSVAL)
        fruits.transformation = (AFTER_TREATMENT, TRANSFORM_PARAM)
        zsind = CData(zsindpath, zsindeps, feature=TAXLEVEL, cross_val=0,
                      transformation=None, param=None)
        lX, lY = fruits._learning, fruits.lindeps
        tX, tY = fruits._testing, fruits.tindeps
        vX, vY = zsind._learning, zsind.lindeps
        vX = fruits.transform(vX)
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
