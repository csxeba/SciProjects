from keras.models import Sequential
from keras.layers import Dense, Dropout, Highway
from keras.optimizers import *

from csxdata import CData
from keras.regularizers import WeightRegularizer
from project_fruits.util import pull_data, pull_validation_data

TAXLEVEL = "species"
PARAMSET = "all"
RUNS = 10

PRETREATMENT = "raw"
PRETREATMENT_PARAM = 0

TRANSFORMATION = "std"
TRANSFORMATION_PARAM = 0

CROSSVAL = .2


def build_net(fanin, outshape):
    network = Sequential([
        Dense(input_dim=fanin, output_dim=120, activation="tanh",
              W_regularizer=WeightRegularizer(l2=0.0)),
        Highway(activation="tanh"),
        Highway(activation="tanh"),

        Dense(output_dim=outshape, activation="softmax")
    ])
    network.compile(SGD(lr=0.01, momentum=0.9), loss="categorical_crossentropy",
                    metrics=["acc"])
    return network


def full_training(validate=True, dump_weights=False):
    fruits = CData(pull_data(label=TAXLEVEL, transformation=PRETREATMENT, param=PRETREATMENT_PARAM),
                   cross_val=0.0)
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
        vx, vy = pull_validation_data(TAXLEVEL, PARAMSET)
        vx = fruits.transform(vx)
        vy = fruits._embedding(vy)
        vacc = network.evaluate(vx, vy, batch_size=len(vy), verbose=0)[-1]
        probs = network.predict_proba(vx, verbose=0)
        preds = network.predict_classes(vx, verbose=0)
        print("ANN validation accuracy:", vacc)
        return probs, preds, vy, fruits


def run():
    fruits = CData(pull_data(label=TAXLEVEL, transformation=PRETREATMENT, param=PRETREATMENT_PARAM,
                             paramset=PARAMSET),
                   cross_val=CROSSVAL)
    fruits.transformation = "std"

    network = build_net(*fruits.neurons_required)

    testing = fruits.table("testing")
    vx, vy = pull_validation_data(TAXLEVEL, paramset=PARAMSET)
    vx = fruits.transform(vx)
    vy = fruits._embedding(vy)

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
