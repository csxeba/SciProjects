import numpy as np
from matplotlib import pyplot as plt

from csxdata.stats.inspection import correlation

from SciProjects.rich.stockshu.data_util import pull_data


Y, header = pull_data()

X = np.arange(1, len(Y))
correlation(Y, names=header)
for y, col in zip(Y.T, header):
    plt.plot(X, y, label=col)

plt.legend()
plt.show()
