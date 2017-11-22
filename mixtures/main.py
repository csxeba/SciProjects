"""
Finding most probable mixture ratio of a sample by optimization
"""

import numpy as np

from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse


def _ellipse_params(cov, ellipse_sigma=2.):
    vals, vecs = np.linalg.eig(cov)

    a = np.sqrt(vals[0]) * ellipse_sigma * 2
    b = np.sqrt(vals[1]) * ellipse_sigma * 2
    theta = np.arctan(vecs[0, 1])

    return a, b, theta


def _toellipse(wrapper, sigma=2.):
    a, b, theta = _ellipse_params(wrapper["cov"], ellipse_sigma=sigma)
    xy = wrapper["mean"]
    e = Ellipse(xy, a*2, b*2, theta)
    e.set_edgecolor("black")
    e.set_facecolor("none")
    return e


def display(fruit, sugar, sample, ellipse_sigma=2):
    ax = plt.gca()

    ell1, ell2 = _toellipse(fruit, ellipse_sigma), _toellipse(sugar, ellipse_sigma)
    ax.add_artist(ell1)
    ax.add_artist(ell2)
    ax.plot([fruit["mean"][0], sugar["mean"][0]], [fruit["mean"][1], sugar["mean"][1]], "b-")
    ax.plot(*sample["mean"], marker="o", color="red")
    eps = 0
    ax.set_xlim([min(ell1.center[0]-ell1.width-eps, ell2.center[0]-ell2.width-eps),
                max(ell1.center[0]+ell1.width+eps, ell2.center[0]+ell2.width+eps)])
    ax.set_ylim([min(ell1.center[1]-ell1.height-eps, ell2.center[1]-ell2.height-eps),
                max(ell1.center[1]+ell1.height+eps, ell2.center[1]+ell2.height+eps)])
    ax.set_xlabel("$D/H_I$")
    ax.set_ylabel(r"$\delta^{13}C$")

    plt.title(f"{sample.ID} ({fruit.ID}) vs. {sugar.ID}", y=1.05)
    plt.show()
    plt.close()


def _euclidean(ar1, ar2):
    return np.linalg.norm(ar1 - ar2)


def calc_mahal_approach(fruit, sugar, sample):

    def dm(x, mu, cov):
        d = x - mu
        return np.sqrt(d.T @ np.linalg.inv(cov) @ d)

    dbase = dm(sample["mean"], fruit["mean"], fruit["cov"])
    dtop = dm(sample["mean"], sugar["mean"], sugar["cov"])
    return dtop / (dtop + dbase)


def calc_eucl_approach(sample_mean, base_mean, top_mean):
    dbase = _euclidean(sample_mean, base_mean)
    dtop = _euclidean(sample_mean, top_mean)
    return dtop / (dtop + dbase)


def _calc_translation(mu_0, mu_1):
    return mu_1 - mu_0


def _calc_alpha(x, mu_0, mu_1):
    return (mu_1.T @ (mu_0 - x)) / (np.linalg.norm(mu_0) ** 2.)


def calculate_optimization_approach(sample_mean: np.ndarray,
                                    base_mean: np.ndarray,
                                    top_mean: np.ndarray,
                                    base_covariance: np.ndarray,
                                    top_covariance: np.ndarray,
                                    get_transform=False):
    """
    Calculates the linear combination of two multivariate normal distributions
    which minimizes the Euclidean/Mahalanobis distance to a sample mean.
    """
    alpha = _calc_alpha(sample_mean, base_mean, top_mean)
    b = _calc_translation(base_mean, top_mean)
    W = np.linalg.inv(base_covariance) @ top_covariance
    return (alpha, b * alpha, W * alpha) if get_transform else alpha


def xperiment():
    from SciProjects.fruits.fruitframe import EtOH

    beet = EtOH.sugar("Beet")
    fruit = EtOH.fruit("Kajszi")
    # sample = EtOH(ID="5377", fruit="Körte", mean=np.array([95.4, -28.2]))
    sample = EtOH(ID="5376", fruit="Alma", mean=np.array([95.5, -27.7]))

    alpha = calculate_optimization_approach(sample["mean"], fruit["mean"], beet["mean"],
                                            fruit["cov"], beet["cov"], get_transform=False)
    print("Mixture ratio optimizerd:", alpha)
    print("Mixture ratio euclidean:", calc_eucl_approach(sample["mean"], fruit["mean"], beet["mean"]))
    print("Mixture ratio mahalanobis:", calc_mahal_approach(fruit, beet, sample))
    display(fruit, beet, sample)


if __name__ == '__main__':
    xperiment()
