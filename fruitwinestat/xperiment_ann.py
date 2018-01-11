from keras.models import Model, Sequential
from keras.layers import Dense, BatchNormalization, Input, Concatenate
from keras.utils import plot_model

from csxdata.visual import learningcurve
from homyd.features import embedding_factory
from SciProjects.fruitwinestat.merge_data import pull_merged_data, as_learningtable, projectroot


def build_shallow_ann(inshape, outshape):
    print("Building shallow ANN...")
    model = Sequential([
        Dense(128, activation="tanh", input_shape=inshape),
        Dense(outshape[0], activation="tanh")
    ])
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["acc"])
    plot_model(model, to_file=projectroot + "Shallow_ANN.png")
    return model


def build_deep_ann(inshape, outshape):

    print("Building deep ANN...")

    def densesegment(tensor, units, length=4):
        tensor1 = BatchNormalization()(Dense(units, activation="relu")(tensor))
        for layer in [Dense(units, activation="relu") for _ in range(length-2)]:
            tensor1 = BatchNormalization()(layer(tensor1))
        cc = BatchNormalization()(Concatenate()([tensor, tensor1]))
        return BatchNormalization()(Dense(units, activation="relu")(cc))

    inpt = Input(inshape)
    densed = Dense(128, activation="relu")(inpt)
    for _ in range(1):
        densed = densesegment(densed, 64, length=4)
    output = Dense(outshape[0], activation="softmax")(densed)
    model = Model(inputs=inpt, outputs=output)
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["acc"])
    plot_model(model, to_file=projectroot + "Deep_ANN.png")
    return model


def get_data(feature):
    lX, lY, tX, tY = as_learningtable(pull_merged_data(feature), feature, split=0.1)
    embedding = embedding_factory(0)
    embedding.fit(lY)
    lY, tY = map(embedding.apply, (lY, tY))
    return lX, lY, tX, tY


def xperiment():
    for nettype, netbuilder in zip(["Shallow", "Deep"], [build_shallow_ann, build_deep_ann]):
        for feature in ["MEGYE", "EV"]:
            print("Fitting on feature:", feature)
            lX, lY, tX, tY = get_data(feature)
            ann = netbuilder(lX.shape[1:], lY.shape[1:])
            history = ann.fit(lX, lY, batch_size=64, epochs=100, validation_data=(tX, tY), verbose=0)
            learningcurve.plot_learning_dynamics(
                history, show=False, dumppath=f"{projectroot}{nettype}_ANN_vs_{feature}.png"
            )


if __name__ == '__main__':
    xperiment()
