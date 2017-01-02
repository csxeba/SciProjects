import time

from csxdata import CData

from SciProjects.generic import paths


# FEATURE = "szin"
FEATURE = "evjarat"
RUNS = 10
EPOCHS = 100
BSIZE = 20
TREATMENTS = None, "std", "pca", "lda", "ica"
TRPARAMS = 0, 0, 3, 2, 2


def get_frame(transf, params):
    path, indepsn = paths["grapes"]
    grapes = CData(path, indepsn, headers=1, feature=FEATURE, lower=True)
    grapes.transformation = (transf, params)
    return grapes


def forge_network(data: CData):
    from csxnet import Network
    from csxnet.brainforge.layers import DenseLayer

    inshape, outshape = data.neurons_required
    model = Network(input_shape=inshape, name="GrapeNinja")
    model.add(DenseLayer(60, activation="tanh"))
    model.add(DenseLayer(30, activation="tanh"))
    model.add(DenseLayer(outshape, activation="sigmoid"))
    model.finalize(cost="xent", optimizer="adam")
    return model


def build_keras_net(data: CData):
    from keras.models import Sequential
    from keras.layers import Dense

    inshape, outshape = data.neurons_required
    model = Sequential([
        Dense(input_dim=inshape[0], output_dim=60, activation="tanh"),
        Dense(output_dim=30, activation="tanh"),
        Dense(output_dim=outshape[0], activation="sigmoid")
    ])
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["acc"])
    return model


def run_forged(grapes):
    start = time.time()
    accs = []
    net = forge_network(grapes)
    for run in range(1, RUNS+1):
        print("\rBrainforge run {0:>{2}}/{1}".format(run, RUNS, len(str(RUNS))), end="")
        net.shuffle()
        grapes.reset_data(shuff=True, transform=True)
        net.fit_csxdata(grapes, batch_size=BSIZE, epochs=EPOCHS, monitor=["acc"], verbose=0)
        accs.append(net.evaluate(*grapes.table("testing"), classify=True)[-1])
    # net.describe(1)
    acc = sum(accs) / len(accs)
    print("\r", end="")
    print("Brainforged Network accuracy: {0:.2%} time: {1} s"
          .format(acc, int(time.time()-start)))
    return acc


def run_keras(grapes):
    start = time.time()
    accs = []
    net = build_keras_net(grapes)
    for run in range(1, RUNS+1):
        print("\rKeras run {0:>{2}}/{1}".format(run, RUNS, len(str(RUNS))), end="")
        net.reset_states()
        grapes.reset_data(shuff=True, transform=True)
        X, Y = grapes.table("learning")
        valid = grapes.table("testing")
        net.fit(X, Y, batch_size=BSIZE, nb_epoch=EPOCHS, validation_data=valid, verbose=0)
        accs.append(net.evaluate(*valid, verbose=0)[-1])

    print("\r", end="")
    print("Keras Network accuracy: {0:.2%} time: {1} s"
          .format(sum(accs) / len(accs), int(time.time()-start)))


def test_pretreatments():
    for treat, arg in zip(TREATMENTS, TRPARAMS):
        print("*"*50)
        print("Data pretreatment is {} ({})".format(treat, arg))
        grapes = get_frame(treat, arg)
        run_forged(grapes)
        run_keras(grapes)


if __name__ == '__main__':
    print("FROM {} RUNS".format(RUNS))
    test_pretreatments()
