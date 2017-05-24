import numpy as np

from matplotlib import pyplot as plt
from matplotlib import mlab

project_root = "/home/csa/Rizs/"


def pull_data(path=None):
    if path is None:
        path = project_root + "biometria.csv"

    with open(path) as handle:
        chain = handle.read()

    data = np.array([line.split("\t") for line in chain.split("\n")[1:-1] if line])
    return np.vectorize(str.replace)(data[:, -1], ",", ".").astype(float)


R = pull_data()
mu, sigma = R.mean(), R.std()

n, bins, patches = plt.hist(R, bins=10, normed=1, facecolor="green", alpha=0.75)
y = mlab.normpdf(bins, mu, sigma)

plt.plot(bins, y, "r--", linewidth=1)
plt.xlabel("R")
plt.ylabel("p")
plt.title("PDF of R of S1-1")
plt.grid(True)
plt.show()
