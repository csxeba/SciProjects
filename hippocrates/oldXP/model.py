from csxdata import roots
from hippocrates.oldXP.generic import load_data
from keras.layers.convolutional import Convolution3D
from keras.layers.core import Dense, Flatten
from keras.layers.pooling import MaxPooling3D
from keras.models import Sequential
from keras.optimizers import RMSprop


def getnet1(inshape):
    print("Building model 1...")
    print("Input shape is", inshape)
    # inshape is (160, 448, 500) = 35 840 000
    model = Sequential()
    model.add(Convolution3D(1, 5, 9, 21, input_shape=inshape, activation="relu"))
    model.add(MaxPooling3D())
    # shape is (78, 220, 240) = 4 118 400
    model.add(Convolution3D(1, 7, 11, 21, activation="relu"))
    model.add(MaxPooling3D())
    # shape is (36, 105, 110) = 415 800
    model.add(Convolution3D(1, 7, 6, 11, activation="relu"))
    model.add(MaxPooling3D())
    # shape is (15, 50, 50) = 37 500
    model.add(Convolution3D(1, 6, 9, 9, activation="relu"))
    model.add(MaxPooling3D())
    # shape is (5, 21, 21) = 2 205
    model.add(Flatten())
    model.add(Dense(120, activation="sigmoid"))
    model.add(Dense(1, activation="sigmoid"))

    print("Compiling model...")
    model.compile(RMSprop(lr=0.01), "mse")
    return model


def getnet2(inshape):
    print("Building model 2...")
    # inshape is (160, 448, 500) = 35 840 000
    model = Sequential()
    model.add(Convolution3D(1, 61, 49, 101, input_shape=inshape, activation="relu"))
    model.add(MaxPooling3D())
    # shape is (50, 200, 200) = 2 000 000
    model.add(Convolution3D(1, 9, 21, 21, activation="relu"))
    model.add(MaxPooling3D())
    # shape is (21, 90, 90) = 170 100
    model.add(Convolution3D(1, 10, 10, 10, activation="relu"))
    model.add(MaxPooling3D((3, 3, 3)))
    # shape is (4, 27, 27) = 2 916
    model.add(Flatten())
    model.add(Dense(30, activation="sigmoid"))
    model.add(Dense(1, activation="sigmoid"))

    print("Compiling model...")
    model.compile(RMSprop(lr=0.01), "mse")
    return model


def getnet3(inshape):
    print("Building model 3...")
    print("Input shape is", inshape)
    # inshape is (80, 224, 250) = 4 480 000
    model = Sequential()
    model.add(Convolution3D(1, 11, 25, 31, input_shape=inshape, activation="relu"))
    model.add(MaxPooling3D())
    # shape is (35, 100, 110) = 385 000
    model.add(Convolution3D(1, 6, 21, 31, input_shape=inshape, activation="relu"))
    model.add(MaxPooling3D())
    # shape is (15, 40, 40) = 24 000
    model.add(Convolution3D(4, 6, 21, 21, input_shape=inshape, activation="relu"))
    model.add(MaxPooling3D())
    # shape is (5, 10, 10) = 500
    model.add(Flatten())
    model.add(Dense(30, activation="sigmoid"))
    model.add(Dense(1, activation="sigmoid"))

    print("Compiling model...")
    model.compile(RMSprop(lr=0.01), "binary_crossentropy")
    return model


def fit():
    X, y = load_data(roots["raw"] + "Project_Hippocrates/X_ds_y_labels.pkl")
    X /= 255.
    print("Loaded data of shape {}".format(X.shape[1:]))
    network = getnet3(X.shape[1:])
    network.summary()
    print("Initial cost:", network.evaluate(X, y))
    network.fit(X, y, batch_size=5, nb_epoch=3)
    print("Done fitting data!")
    return network


if __name__ == '__main__':
    fit()
