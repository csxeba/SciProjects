"""
Finding most probable mixture ratio of a sample by optimization
"""

import numpy as np


def _calc_translation(mu_0, mu_1):
    return mu_1 - mu_0


def _calc_alpha(x, mu_0, mu_1):
    return (mu_1.T @ (x - mu_0)) / (np.linalg.norm(mu_0) ** 2.)


def calculate(sample_mean: np.ndarray,
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
    sample = EtOH(name="17090055", fruit="Kajszi", mean=np.array([95.73, -25.89]))

    alpha = calculate(sample["mean"], fruit["mean"], beet["mean"],
                      fruit["cov"], beet["cov"], get_transform=False)
    print("Most probable mixture ratio:", alpha)


if __name__ == '__main__':
    xperiment()
