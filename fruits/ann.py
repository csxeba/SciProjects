from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import *

from csxdata import CData
from keras.regularizers import WeightRegularizer
from SciProjects.fruits import gyumpath, gyumindeps, zsindpath, zsindeps

TAXLEVEL = "Species"
RUNS = 10

PRETREATMENT = "raw"
PRETREATMENT_PARAM = 0

TRANSFORMATION = "std"
TRANSFORMATION_PARAM = 0

CROSSVAL = .2


def build_net(inshape, outshape):
    network = Sequential([
        Dense(input_dim=inshape[0], output_dim=120, activation="tanh",
              W_regularizer=WeightRegularizer(l2=0.0)),
        Dense(output_dim=outshape[0], activation="softmax")
    ])
    network.compile(SGD(lr=0.01, momentum=0.9), loss="categorical_crossentropy",
                    metrics=["acc"])
    return network


def full_training(validate=True, dump_weights=False):
    fruits = CData(gyumpath, gyumindeps, feature=TAXLEVEL, cross_val=0.0)
    fruits.transformation = (TRANSFORMATION, TRANSFORMATION_PARAM)

    network = build_net(*fruits.neurons_required)

    X, y = fruits.table("learning")
    network.fit(X, y, batch_size=30, nb_epoch=500, verbose=0)

    if dump_weights:
        weights = network.layers[0].get_weights()

        wghts = open("weights.csv", "w")
        wghts.write("\n".join(["\t".join([str(float(cell)) for cell in line]) for line in weights[0].T])
                    .replace(".", ","))
        wghts.close()

    if validate:
        vx, vy = CData(zsindpath, zsindeps, cross_val=0.0, feature=TAXLEVEL)
        vx = fruits.transform(vx)
        vy = fruits.embed(vy)
        vacc = network.evaluate(vx, vy, batch_size=len(vy), verbose=0)[-1]
        probs = network.predict_proba(vx, verbose=0)
        preds = network.predict_classes(vx, verbose=0)
        print("ANN validation accuracy:", vacc)
        return probs, preds, vy, fruits


def run():
    fruits = CData(gyumpath, gyumindeps, feature=TAXLEVEL, cross_val=CROSSVAL)
    fruits.transformation = (TRANSFORMATION, TRANSFORMATION_PARAM)

    network = build_net(*fruits.neurons_required)

    testing = fruits.table("testing")
    zsind = CData(zsindpath, zsindeps, cross_val=0.0, feature=TAXLEVEL)
    vx, vy = zsind._learning, zsind.lindeps
    vx = fruits.transform(vx)
    vy = fruits.embed(vy)

    initc, initacc = network.evaluate(*testing, verbose=0)
    initc, initacc = round(initc, 5), round(initacc, 5)
    print("Initial cost: {}\tacc: {}".format(initc, initacc))

    X, y = fruits.table("learning")
    network.fit(X, y, batch_size=20, nb_epoch=400, validation_data=testing, verbose=0)
    tacc = network.evaluate(*testing, batch_size=fruits.n_testing, verbose=0)[-1]
    vacc = network.evaluate(vx, vy, verbose=0)[-1]
    # batchgen = fruits.batchgen(100, infinite=True)
    # log = network.fit_generator(batchgen, fruits.N, nb_epoch=15, validation_data=valid, verbose=verbose)
    print("T: {}\tV: {}".format(tacc, vacc))
    return tacc, vacc


if __name__ == '__main__':
    taccs, vaccs = [], []
    for runnum in range(1, RUNS+1):
        print("\nANN run", runnum, end="\t")
        tc, vc = run()
        taccs.append(tc)
        vaccs.append(vc)

    print("-"*50 + "\nFinal ANN result:")
    print("Testing data:", sum(taccs) / len(taccs), sep="\t")
    print("Validation data:", sum(vaccs) / len(vaccs), sep="\t")

    # proba, preds, y, frame = full_training(dump_weights=True)
    # labels = frame.translate(y)
    # chain = "TRUE" + "\t" + "\t".join(frame._embedding._categories) + "\t" + "PRED" + "\n"
    # for label, prob, pred in zip(labels, proba, preds):
    #     chain += label + "\t" + "\t".join(prob.astype(str)) + "\t" + str(pred) + "\n"
    # print(chain)
