from generic import *


def get_net(fanin, outshape):
    from keras.models import Sequential
    from keras.layers.core import Dense, Activation
    from keras.optimizers import SGD

    if isinstance(fanin, tuple):
        if len(fanin) == 1:
            fanin = fanin[0]

    network = Sequential()
    network.add(Dense(input_dim=fanin, output_dim=30))
    network.add(Activation("tanh"))
    network.add(Dense(output_dim=outshape, activation="softmax"))
    network.compile(SGD(lr=0.06), "categorical_crossentropy", metrics=["accuracy"])

    return network


def experiment(crossval, epochs=100):
    ntab = pull_data(crossval)
    kerberos = get_net(*ntab.neurons_required)
    X, y = ntab.table("learning")
    bsize = X.shape[0] // 2
    if not crossval:
        kerberos.fit(X, y, batch_size=bsize, nb_epoch=epochs)
    if crossval:
        ttable = ntab.table("testing")
        kerberos.fit(X, y, batch_size=bsize, nb_epoch=epochs, validation_data=ttable)

    samples, sample_labels = pull_samples()
    samples_t = ntab.standardize(samples)

    cls = kerberos.predict_classes(samples_t)

    lbs, prds = [], []
    for lab, prd in zip(sample_labels, cls):
        print("Kerberos prediction for {}:\t{}".format(lab[0], "Foreign" if prd else "HUN"))
        lbs.append(lab)
        prds.append(prd)
    return lbs, prds


if __name__ == '__main__':
    experiment(0.2, epochs=120)
