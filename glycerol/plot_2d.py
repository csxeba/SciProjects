import numpy as np

from matplotlib import pyplot as plt

from SciProjects.glycerol import pull_data

cdata, xdata = pull_data()
X = np.concatenate((cdata, xdata)).T
cdata = cdata.T
xdata = xdata.T

poly = np.poly1d(np.polyfit(X[0], X[1], 1))
r = np.corrcoef(X[1], poly(X[0])).min()

plt.scatter(*cdata, s=2, c="blue", label="Cabanero et al.")
plt.scatter(*xdata, s=2, c="red", label="Xuemin et al.")
plt.plot(X[0], poly(X[0]), "r-", label=f"$R^2 = {r**2:.4f}$")
plt.title(f"Bor etanol/glicerin $\delta^13C$ értékek")
plt.legend()
plt.show()
