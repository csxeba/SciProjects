import numpy as np

from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse


class FruitDisplayer:

    def __init__(self, fruit, sugar, sigma_level=2., ax=None):
        self.fruit = fruit
        self.sugar = sugar
        self.ellipse = dict(fruit=None, sugar=None)
        self.sigma = sigma_level
        self.ax = plt.subplot(111) if ax is None else ax
        self._draw_reference_ellipses()
        self._set_up_axes()

    @classmethod
    def from_fuitproblem(cls, fruitproblem_obj, sigma_level=2.):
        obj = cls(fruit=fruitproblem_obj.fruit, sugar=fruitproblem_obj.sugar, sigma_level=sigma_level)
        obj.draw_as_point(fruitproblem_obj.sample)
        return obj

    def _draw_reference_ellipses(self):
        self.ellipse["fuit"] = self.draw_as_ellipse(self.fruit)
        self.ellipse["sugar"] = self.draw_as_ellipse(self.sugar)
        self.draw_as_point(self.fruit)
        self.draw_as_point(self.sugar)

    def _calculate_ellipse_params_from_wrapper(self, wrapper):
        vals, vecs = np.linalg.eig(wrapper["cov"])

        a = np.sqrt(vals[0]) * self.sigma * 2.
        b = np.sqrt(vals[1]) * self.sigma * 2.
        theta = np.arctan(vecs[0, 1])

        xy = wrapper["mean"]
        e = Ellipse(xy, a*2, b*2, theta)
        e.set_edgecolor("black")
        e.set_facecolor("none")
        return e

    def _set_up_axes(self):
        fell = self.ellipse["fuit"]
        sell = self.ellipse["sugar"]
        self.ax.set_xlim([
            min(fell.center[0] - fell.width, sell.center[0] - sell.width),
            max(fell.center[0] + fell.width, sell.center[0] + sell.width)
        ])
        self.ax.set_ylim([
            min(fell.center[1] - fell.height, sell.center[1] - sell.height),
            max(fell.center[1] + fell.height, sell.center[1] + sell.height)
        ])
        self.ax.set_xlabel("$D/H_I$")
        self.ax.set_ylabel(r"$\delta^{13}C$")

    def draw_as_ellipse(self, wrapper):
        if wrapper["cov"] is None:
            print(f"Can't add {wrapper.ID} as an ellipse, it has no covariance matrix!")
        ell1 = self._calculate_ellipse_params_from_wrapper(wrapper)
        self.ax.add_artist(ell1)
        return ell1

    def draw_as_point(self, wrapper):
        self.ax.plot(*wrapper["mean"], "ro")
        self.ax.annotate(wrapper.ID, xy=wrapper.mean)

    def link_centroids(self, wrapper, other,):
        mu1, mu2 = wrapper["mean"], other["mean"]
        self.ax.plot([mu1[0], mu2[0]], [mu1[1], mu2[1]], "r--")

    @staticmethod
    def show():
        plt.show()
        plt.close()

    @staticmethod
    def dump(path):
        plt.savefig(path)
