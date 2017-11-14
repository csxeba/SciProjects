import numpy as np

"""
Finding most probable mixture ratio of a sample by optimization
"""


def _calc_translation(mu_0, mu_1):
    return mu_1 - mu_0


def _calc_alpha(x, mu_0, mu_1):
    return (mu_1.T @ (x - mu_0)) / (np.linalg.norm(mu_0) ** 2.)


def calculate(sample_mean: np.ndarray,
              base_mean: np.ndarray,
              top_mean: np.ndarray,
              base_covariance: np.ndarray,
              top_covariance: np.ndarray):
    """
    Calculates the linear combination of two multivariate normal distributions
    which minimizes the Euclidean/Mahalanobis distance to a sample mean.
    """
    alpha = _calc_alpha(sample_mean, base_mean, top_mean)
    b = _calc_translation(base_mean, top_mean)
    W = np.linalg.inv(base_covariance) @ top_covariance
    return alpha, b * alpha, W * alpha
