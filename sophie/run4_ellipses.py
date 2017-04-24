import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse


from SciProjects.sophie import projectroot

SIGMA = 2.
colors = {
    "Alma": "red",
    "Kört": "red",
    "Cser": "purple",
    "CRép": "black",
    "CNád": "black",
    "Kuko": "black",
    "Megg": "purple",
    "Kajs": "orange",
    "Szil": "navy",
    "Szől": "green",
    "Burg": "black"
}


class EllipseDrawer:

    def __init__(self, name, *args):
        mean1, mean2, var1, var2, covar = list(map(float, args))
        self.name = name
        self.means = np.array([float(mean1), float(mean2)])
        self.covariance = np.zeros((2, 2))
        self.covariance[0, 0] = float(var1)
        self.covariance[0, 1] = covar
        self.covariance[1, 0] = covar
        self.covariance[1, 1] = var2

    @property
    def ellipse_params(self):
        eigval, eigvec = np.linalg.eig(self.covariance)
        a = np.sqrt(abs(eigval[0])) * 2
        b = np.sqrt(abs(eigval[1])) * 2
        theta = np.arctan(eigvec[0, 1])
        return a, b, theta

    @classmethod
    def fromline(cls, dline):
        return cls(*dline.split(";"))

    def draw(self, sigma, ax):
        color = colors[self.name[:4]]
        a, b, theta = self.ellipse_params
        ellipse_object = Ellipse(self.means, a*sigma, b*sigma, theta)
        ellipse_object.set_facecolor("none")
        ellipse_object.set_edgecolor(color)
        ax.add_artist(ellipse_object)
        ax.scatter(self.means[0], self.means[1], color=color, marker="X")
        ax.annotate(self.name, xy=self.means, xycoords="data",
                    horizontalalignment="right",
                    verticalalignment="top")


chain = open(projectroot + "ellipses.txt").read()
data = chain.split("\n")
ellipses = (EllipseDrawer.fromline(line) for line in data)

axes = plt.gca()
for ell in ellipses:
    ell.draw(SIGMA, axes)

axes.set_xlabel("$(D/H)_I$")
axes.set_ylabel(r"$\delta^{13}C$")
plt.suptitle("Biológiai eredet, {}x szórású konfidencia ellipszisekkel"
             .format(int(SIGMA)))
plt.show()
