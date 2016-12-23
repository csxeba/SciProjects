# Std lib imports
import abc

# 3rd party imports
import numpy as np


def sigmoid(z):
    """The vectorized sigmoid (logistic) function"""
    return 1. / (1. + np.exp(-z))


def rectify(val, mini=0., maxi=1.):
    return np.maximum(mini, np.minimum(maxi, val))


def log(chain):
    from datetime import datetime as dt
    with open("log/runlog.txt", "a") as logfl:
        logfl.write("\n\n{}: {}".format(dt.now().strftime("%Y.%m.%d %H:%M:%S"), chain))
        logfl.close()


class _FitnessFunction(abc.ABC):

    @abc.abstractmethod
    def _calculate(self, x1, x2, q, maxqual):
        raise NotImplementedError

    def __call__(self, x1, x2, q, maxqual):
        return self._calculate(x1, x2, q, maxqual)


class _Taylor04f(_FitnessFunction):

    def _calculate(self, x1, x2, q, maxqual):
        z = x1 + x2
        if maxqual == 1:
            return (z / (z + 1.)) - (x1 * x2)
        else:
            return (z / (z + 1.)) - (1. - q) * x1 - (x1 * x2)


class _Taylor04s(_FitnessFunction):

    def _calculate(self, x1, x2, q, maxqual):
        del q, maxqual
        z = x1 + x2
        return 2. * z - (x1 * x2)


class _Case_B(_FitnessFunction):

    def _calculate(self, x1, x2, q, maxqual):
        z = x1 + x2
        if maxqual == 1:
            return 2. * z - z ** 2 - 0.5 * x1 * x2
        else:
            return 2. * z - z ** 2 - x1 * x2 - (1. - q) * x1


class _Fitness:
    """
    This is a convenience class. By indexing <fitness> so:
    fitness[name_of_fitness_function] one can get the reference
    to the desired fitness function.
    """

    def __init__(self):
        self.functions = {
            "taylor04f": taylor04f,
            "taylor04s": taylor04s,
            "case b": case_b,
            "case_b": case_b
        }

    def __getitem__(self, item):
        if item not in self.functions:
            raise IndexError("Requested fitness function is not defined!")
        return self.functions[item]


taylor04f = _Taylor04f()
taylor04s = _Taylor04s()
case_b = _Case_B()

# Instance of the _Fintess convenience class
# fitness functions can be retrieved with the
# getitem operator ["fitness function name"]
fitness = _Fitness()
