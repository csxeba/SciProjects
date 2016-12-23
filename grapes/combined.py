from csxdata import CData
from csxnet.ann import Autoencoder, Network
from csxnet.brainforge.layers import DenseLayer, HighwayLayer

from project_grapes.misc import pull_data
from project_grapes.classical import full_run

grapes = pull_data(frame=True, feature="borrégió")
grapes.transformation = "std"


def autoencoder():
    ae = Network(input_shape=grapes.neurons_required[0], name="TestAutoEncoder")
    ae.add(DenseLayer(60, activation="tanh"))
    ae.add(DenseLayer(30, activation="tanh"))
    ae.add(DenseLayer(30, activation="tanh"))
    ae.add(DenseLayer(60, activation="tanh"))
    ae.add(DenseLayer(grapes.neurons_required[0]))
    ae.finalize(cost="mse", optimizer="adam")
    ae.describe(1)

    ae.fit(grapes.testing, grapes.testing, epochs=300, verbose=0)
    ae.prediction(grapes.learning)
    eX = ae.layers[2].output

    trGrapes = CData((eX, grapes.lindeps))

    full_run(trGrapes)


def neural_switcharoo():
    model = Network(input_shape=grapes.neurons_required[0], name="GrapesNet")
    model.add(DenseLayer(60, activation="tanh"))
    model.add(DenseLayer(grapes.neurons_required[1], activation="sigmoid"))
    model.finalize(cost="xent", optimizer="adam")
    model.describe(1)

    model.fit(*grapes.table("testing"), epochs=300, monitor=["acc"], verbose=0)

    model.prediction(grapes.learning)
    trX = model.layers[-2].output

    trGrapes = CData((trX, grapes.lindeps))

    full_run(trGrapes)

if __name__ == '__main__':
    neural_switcharoo()
