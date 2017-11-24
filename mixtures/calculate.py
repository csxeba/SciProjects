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
        calc_fn = {"euc": _euclidean_approach, "mah": _mahal_approach, "opt": _optimization_approach
                   }[approach[:3].lower()]
        alphas = np.array([calc_fn(sample, self._fruit, self._sugar) for sample in samples])
        if verbose:
            print(f"Most probable mixture ratios calculated by approach: {approach}")
            for sample, ratio in zip(samples, alphas):
                print(f"Sample: {sample.ID} sugar content: {ratio:.2%}")
        return alphas


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
    return (sugar["mean"] @ (fruit["mean"] - sample["mean"])) / (np.linalg.norm(fruit["mean"])**2.)


def _optimization_approach2(sample, fruit, sugar):
    return (np.linalg.norm(sample["mean"]) - np.linalg.norm(fruit["mean"])) / np.linalg.norm(sugar["mean"])


if __name__ == '__main__':
    print(_optimization_approach(EtOH.sample(95.5, -27.7, "Alma", "5376"), EtOH.fruit("Alma"), EtOH.sugar("Beet")))
