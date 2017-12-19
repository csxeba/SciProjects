"""
Finding most probable mixture ratio of a sample
"""

import numpy as np

from SciProjects.fruits.fruitframe import EtOH


class FruitProblem:

    def __init__(self, fruit_reference: EtOH, sugar_reference: EtOH):
        self.fruit = fruit_reference
        self.sugar = sugar_reference

    @classmethod
    def from_names(cls, fruit_name, sugar_name):
        return cls(EtOH.fruit(fruit_name), EtOH.sugar(sugar_name))

    def _calculate(self, calcfn, calcapproach, verbose, *samples):
        alphas = np.array([calcfn(sample, self.fruit, self.sugar) for sample in samples])
        if verbose:
            print(f"Most probable mixture by {calcapproach}:")
            for sample, ratio in zip(samples, alphas):
                print(f"Sample: {sample.ID} sugar content: {ratio:.2%}")
        return alphas

    def ratio_based(self, *samples, metric="euclidean", verbose=1):
        calcfn = {"euc": _euclidean_ratio, "mah": _mahalanobis_ratio}[metric[:3].lower()]
        return self._calculate(calcfn, f"{metric} distance ratio", verbose, *samples)

    def optimization_based(self, *samples, metric="mahalanobis", verbose=1):
        calcfn = {"euc": _optimization_euclidean, "mah": _optimization_mahalanobis}[metric[:3].lower()]
        return self._calculate(calcfn, f"optimizing on {metric} distance", verbose, *samples)

    def projection_based(self, *samples, metric=None, verbose=1):
        return self._calculate(_project_on_line, "projection", verbose, *samples)


def _euclidean_ratio(sample, fruit, sugar, verbose=0):
    dbase = np.linalg.norm(sample["mean"] - fruit["mean"])
    dtop = np.linalg.norm(sample["mean"] - sugar["mean"])
    if verbose:
        print(f"R_EUCL: sample from fruit: {dbase}")
        print(f"R_EUCL: sample from sugar: {dtop}")
    return dtop / (dtop + dbase)


def _mahalanobis_ratio(sample, fruit, sugar, verbose=0):

    def md(x, mu, sigma):
        z = x - mu
        return z @ np.linalg.inv(sigma) @ z

    dtop = md(sample["mean"], sugar["mean"], sugar["cov"])
    dbase = md(sample["mean"], fruit["mean"], sugar["cov"])
    if verbose:
        print(f"R_EUCL: sample from fruit: {dbase}")
        print(f"R_EUCL: sample from sugar: {dtop}")
    return dtop / (dtop + dbase)


def _optimization_euclidean(sample, fruit, sugar, verbose=0):
    x = sample["mean"] - fruit["mean"]
    mu = sugar["mean"] - fruit["mean"]
    return (x @ mu) / (mu @ mu)


def _optimization_mahalanobis(sample, fruit, sugar, verbose=0):
    M = np.linalg.inv(sugar["cov"])
    x, m0, m1 = sample["mean"], fruit["mean"], sugar["mean"]
    return np.sqrt((x@M@x - 2*x@M@m0) + m0@M@m0) / (m1@M@m1)


def _project_on_line(sample, fruit, sugar, verbose=0):
    x = sample["mean"] - fruit["mean"]
    mu = sugar["mean"] - fruit["mean"]
    enum = x @ mu
    denom = np.linalg.norm(mu)
    if verbose:
        print(f"project enum: {enum}, denom: {denom}")
    return enum / denom


def main():
    from SciProjects.mixtures.visualize import FruitDisplayer
    prob = FruitProblem.from_names(fruit_name="kajszi", sugar_name="répa")
    sample = EtOH.sample(95.73, -25.89, "kajszi", "17090055")
    prob.ratio_based(sample, metric="euclidean")
    prob.ratio_based(sample, metric="mahalanobis")
    prob.optimization_based(sample, metric="euclidean")
    prob.optimization_based(sample, metric="mahalanobis")
    prob.projection_based(sample)
    fd = FruitDisplayer.from_fuitproblem(fruitproblem_obj=prob)
    fd.draw_as_point(sample)
    fd.show()


if __name__ == '__main__':
    main()
