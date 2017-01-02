from csxdata import CData
from csxnet.ann import Network
from csxnet.brainforge.layers import DenseLayer

from SciProjects.grapes import path, indepsn
from SciProjects.grapes.classical import full_run


def autoencoder(grapes):
    ae = Network(input_shape=grapes.neurons_required[0], name="TestAutoEncoder")
    ae.add(DenseLayer(60, activation="tanh"))
    ae.add(DenseLayer(30, activation="tanh"))
    ae.add(DenseLayer(30, activation="tanh"))
    ae.add(DenseLayer(60, activation="tanh"))
    ae.add(DenseLayer(grapes.neurons_required[0], activation="linear"))
    ae.finalize(cost="mse", optimizer="adam")
    ae.describe(1)

    ae.fit(grapes.testing, grapes.testing, epochs=300, verbose=0)
    ae.prediction(grapes.learning)
    eX = ae.layers[2].output

    trGrapes = CData((eX, grapes.lindeps), headers=None)

    full_run(trGrapes)


def neural_switcharoo(grapes):
    model = Network(input_shape=grapes.neurons_required[0], name="GrapesNet")
    model.add(DenseLayer(60, activation="tanh"))
    model.add(DenseLayer(grapes.neurons_required[1], activation="sigmoid"))
    model.finalize(cost="xent", optimizer="adam")
    model.describe(1)

    model.fit(*grapes.table("testing"), epochs=300, monitor=["acc"], verbose=0)

    model.prediction(grapes.learning)
    trX = model.layers[-2].output

    trGrapes = CData((trX, grapes.lindeps), headers=None)

    full_run(trGrapes)

if __name__ == '__main__':
    dframe = CData(path, indepsn, headers=1, feature="borregio", lower=True)
    dframe.transformation = "std"
    autoencoder(dframe)
