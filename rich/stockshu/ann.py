import numpy as np

from keras.models import Sequential
from keras.layers import LSTM, Dense, Conv1D, Activation, BatchNormalization, Flatten


def data_stream(raw, timestep=7, batch_size=32):
    N = len(raw)
    randix = np.arange(N-timestep-1)
    while 1:
        np.random.shuffle(randix)
        for start in range(0, len(randix), batch_size):
            X, Y = [], []
            for ix in randix[start:start+batch_size]:
                X.append(raw[ix:ix+timestep])
                Y.append(raw[ix+timestep+1])
            yield np.stack(X), np.stack(Y)


def validation_data(raw, timestep=7, m=100):
    return next(data_stream(raw, timestep, m))


def build_LSTM(inputs, outputs):
    model = Sequential(layers=[
        LSTM(120, activation="relu", input_shape=inputs), BatchNormalization(),
        Dense(30, activation="relu"), BatchNormalization(),
        Dense(outputs[0], activation="linear")
    ])
    model.compile(optimizer="adam", loss="mse")
    return model


def build_CNN(inputs, outputs):
    model = Sequential(layers=[
        BatchNormalization(input_shape=inputs),
        Conv1D(30, kernel_size=3), Activation("relu"), BatchNormalization(),
        Conv1D(30, kernel_size=3), Activation("relu"), BatchNormalization(),
        Conv1D(outputs[0], kernel_size=3),
        Activation("linear"),
        Flatten(),
    ])
    model.compile(optimizer="adam", loss="mse")
    return model


def xperiment():
    learnX, validX = pull_data()
    N, D = learnX.shape
    Xstream = data_stream(learnX, timestep=7, batch_size=32)
    valid = validation_data(validX)
    net = build_CNN([7, D], [D])
    net.fit_generator(Xstream, steps_per_epoch=(N*100)//32, epochs=10., validation_data=valid)


if __name__ == '__main__':
    xperiment()
