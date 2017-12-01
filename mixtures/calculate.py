"""
Finding most probable mixture ratio of a sample
"""

import numpy as np

from SciProjects.fruits.fruitframe import EtOH


_approaches = ("euclidean", "mahalanobis", "optimization")


class FruitProblem:

    def __init__(self, fruit_reference: EtOH, sugar_reference: EtOH):
        self._fruit = fruit_reference
        self._sugar = sugar_reference

    @classmethod
    def from_names(cls, fruit_name, sugar_name):
        return cls(EtOH.fruit(fruit_name), EtOH.sugar(sugar_name))

    def mixture_ratio(self, *samples, approach="euclidean", verbose=1):
        calc_fn = {"euc": _euclidean_ratio, "mah": _mahal_approach, "opt": _optimization_approach
                   }[approach[:3].lower()]
        alphas = np.array([calc_fn(sample, self._fruit, self._sugar) for sample in samples])
        if verbose:
            print(f"Most probable mixture ratios calculated by approach: {approach}")
            for sample, ratio in zip(samples, alphas):
                print(f"Sample: {sample.ID} sugar content: {ratio:.2%}")
        return alphas


def _euclidean_ratio(sample, fruit, sugar):
    dbase = np.linalg.norm(sample["mean"] - fruit["mean"])
    dtop = np.linalg.norm(sample["mean"] - sugar["mean"])
    return dtop / (dtop + dbase)


def _mahalanobis_ratio(sample, fruit, sugar):

    def md(x, mu, sigma):
        return


def _optimization_euclidean(sample, fruit, sugar):
    x, m0, m1 = sample["mean"], fruit["mean"], sugar["mean"]
    return (x @ m1 - m0 @ m1) / (m1 @ m1)


def _optimization_mahalanobis(sample, fruit, sugar):

    def trp(y, z=None):
        return np.sum(M * np.outer(y, y if z is None else z))

    M = np.linalg.inv(sugar["cov"]) @ fruit["cov"]
    x, m0, m1 = sample["mean"], fruit["mean"], sugar["mean"]
    return np.sqrt((trp(x) - 2.*trp(x, m0) + trp(m0)) / (trp(m1)))


if __name__ == '__main__':
    print(_optimization_approach(EtOH.sample(95.5, -27.7, "Alma", "5376"), EtOH.fruit("Alma"), EtOH.sugar("Beet")))
