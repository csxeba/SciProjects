"""
Python reimplementation of

/* An implementation of the simulation model by
 *
 * Taylor PD, Day T Stability in negotiation games and the emergence of
 * cooperation PROCEEDINGS OF THE ROYAL SOCIETY OF LONDON SERIES B-BIOLOGICAL
 * SCIENCES 271 (1540): 669-674 APR 7 2004
 */

All rights go to the respected owners.
"""

try:
    import numpy
except ImportError:
    raise ImportError("NumPy is not available, please install it!")

from bz.src.ga import Population
from bz.src.util import log


class Param:

    def __init__(self):
        # The individual types used. Can be "Linear", "ANN", "RNN", "LSTM"
        self.indiv_type1 = ""
        self.indiv_type2 = ""

        self.max_gen = 0  # max number of generations
        self.nth_out = 0  # every nth generation is written out
        self.n_node = 0  # the number of hidden nodes
        self.n_input = 0  # >= 2
        self.n_indiv = 0  # the number of individuals
        self.max_neg = 0  # max number of rounds in a negotiation
        self.tol_neg = 0.0  # tolerance for negotiation
        self.p_ann = 0.0  # initial proportion of type ANN individual
        self.max_qual = 0  # maximum number of qualities

        self.fitness_fun = None  # reference to the actual fitness function used
        self.fit_type = 0  # type of fitness function
        self.pairing = 0  # type of pairing: "one_to_one" vs.
        self.qk = 0.0  # parameter expressing the effect of quality
        self.min_rho = 0.0  # min rho value allowed
        self.max_rho = 0.0  # max rho value allowed
        self.min_lambda = 0.0  # min lambda value allowed
        self.max_lambda = 0.0  # max lambda value allowed
        self.max_ann = 0.0  # max value allowed for weights and function pars
        self.min_ann = 0.0  # min value allowed for weights and function pars

        self.mut_prob = 0.0  # probability that an allele mutates
        self.delta = 0.0  # mutation changes an allele in range +- delta
        self.prob_recomb = 0.0  # probability of recombination

    def __getitem__(self, item):
        return self.__dict__[item]


class CsxParams(Param):

    def __init__(self):
        Param.__init__(self)
        # The of individual types used. Can be "Linear", "ANN", "RNN", "LSTM"
        self.indiv_type1 = "Linear"
        self.indiv_type2 = "ANN"
        self.p_type1 = 0.5  # initial proportion of type1 individual

        self.max_gen = 100  # max number of generations
        self.nth_out = 10  # every nth generation is written out
        self.n_node = 3  # the number of hidden nodes
        self.n_input = 4  # >= 2
        self.n_indiv = 10  # the number of individuals
        self.max_neg = 5  # max number of rounds in a negotiation
        self.tol_neg = 2.6  # tolerance for negotiation
        self.max_qual = 5  # maximum number of qualities

        self.fitness_fun = "case b"  # reference to the actual fitness function used
        self.pairing = "one to one"  # type of pairing
        self.min_rho = 0.0  # min rho value allowed
        self.max_rho = 3.0  # max rho value allowed
        self.min_lambda = 0.0  # min lambda value allowed
        self.max_lambda = 3.0  # max lambda value allowed
        self.min_ann = 0.0  # min value allowed for weights and function pars
        self.max_ann = 3.0  # max value allowed for weights and function pars

        self.mut_prob = 0.1  # probability that an allele mutates
        self.delta = 2.0  # mutation changes an allele in range +- delta
        self.prob_recomb = 0.1  # probability of recombination

        self.qk = [0.1, 0.3, 0.6, 1.5, 3.0]  # parameter expressing the effect of quality


def sanity_check():
    import os
    if not os.path.exists("./log"):
        print("Log directory is unavailable. Creating it!")
        os.mkdir("./log")
    if not os.path.exists("./log/runlog.txt"):
        with open("log/runlog.txt", "w") as logfl:
            logfl.write("")
            logfl.close()
            print("Creating logs/runlog.txt")


def main():
    params = CsxParams()
    pop = Population(initialize=True, p=params)

    print("\n-------------\nINITIAL:")
    log("XPERIMENT START!")
    pop.describe(write_to_log=True)

    print("\n-------------\nRUN:")
    pop.run(write_to_log=True)

    print("\n-------------\nFINAL:")
    pop.describe(write_to_log=True)
    log("XPERIMENT END!")


if __name__ == '__main__':
    sanity_check()
    main()
