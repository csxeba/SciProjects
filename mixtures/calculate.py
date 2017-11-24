"""
Finding most probable mixture ratio of a sample
"""

import numpy as np

from SciProjects.fruits.fruitframe import EtOH


_approaches = ("euclidean", "mahalanobis", "optimization")


class FruitProblem:

    def __init__(self, fruit_reference: EtOH, sugar_reference: EtOH, sample: EtOH):
        self.fruit = fruit_reference
        self.sugar = sugar_reference
        self.sample = sample

    @classmethod
    def from_data(cls, fruit_name, sugar_name, sample_mean, sample_cov, sample_ID):
        return cls(EtOH.fruit(fruit_name), EtOH.sugar(sugar_name),
                   EtOH(mean=sample_mean, cov=sample_cov, ID=sample_ID))

    def mixture_ratio(self, approach="euclidean"):
        alpha = {"euc": _euclidean_approach, "mah": _mahal_approach, "opt": _optimization_approach
                 }[approach[:3].lower()](self.sample, self.fruit, self.sugar)
        print(f"Most probable mixture ratio calculated by approach: {approach}: {alpha:.4f}")
        return alpha


def _mahal_approach(sample, fruit, sugar):

    def dm(x, mu, cov):
        d = x - mu
        return np.sqrt(d.T @ np.linalg.inv(cov) @ d)

    dbase = dm(sample["mean"], fruit["mean"], fruit["cov"])
    dtop = dm(sample["mean"], sugar["mean"], sugar["cov"])
    return dtop / (dtop + dbase)


def _euclidean_approach(sample, fruit, sugar):
    dbase = np.linalg.norm(sample["mean"] - fruit["mean"])
    dtop = np.linalg.norm(sample["mean"] - sugar["mean"])
    return dtop / (dtop + dbase)


def _optimization_approach(sample, fruit, sugar):
    return (sugar["mean"].T @ (fruit["mean"] - sample["mean"])) / (np.linalg.norm(fruit["mean"]) ** 2.)

