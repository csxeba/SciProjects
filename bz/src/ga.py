# Stdlib imports
from random import randrange, random, uniform, choice

# 3rd party imports
import numpy as np

# Project imports
from .indiv import indivtypes
from .util import fitness, log


class Population:
    """
    Wraps a list of Individual objects

    and defines operations on them.
    """

    def __init__(self, initialize, p):
        self.indivtype1 = indivtypes[p.indiv_type1]
        self.indivtype2 = indivtypes[p.indiv_type2]
        self.p_type1 = p.p_type1

        self.params = p
        self.n_indiv = p.n_indiv
        self.pairing_type = p.pairing
        self.negotiation_tol = p.tol_neg
        self.negotiation_max = p.max_neg
        self.prob_recomb = p.prob_recomb
        self.qk = p.qk
        self.fitness_fun = fitness[p.fitness_fun]
        self.max_qual = p.max_qual
        self.mut_prob = p.mut_prob
        self.individuals = []
        self.nth_outh = p.nth_out
        self.uptodate = False
        self.generation = 0
        self.max_gen = p.max_gen

        if initialize:
            for _ in range(p.n_indiv):
                ind = self.indivtype1 if random() < self.p_type1 else self.indivtype2
                self.individuals.append(ind(p=self.params))
        else:
            self.individuals = []

    def run(self, epochs=None, write_to_log=False):
        """Coordinates the simulation"""
        if epochs is None:
            epochs = self.max_gen
        if not self.uptodate:
            self.pairing()
        for ep in range(1, epochs+1):
            self.reproduction()
            self.pairing()
            if ep % self.nth_outh == 0:
                chain = "Generation {}: AVG Fitness: {}".format(ep, self.grade)
                print(chain)
                if write_to_log:
                    log(chain)

            self.generation += 1

    def reproduction(self):
        """
        Generates a new set of individuals (a new generation).
        The contribution of the previous individuals to the next
        generation is determined by their scaled fitness values.
        """

        def calculate_contributions_to_next_generation_from_fitnesses():
            # I changed the logic here!
            # In the original code, min and sum get calculated first, then they
            # are applied. I calculate the sum after subtracting the min, so the
            # final fitness values will sum up to 1.0.
            # I hope I didn't mess up the logic somehow, I'm not the greatest
            # ecologist, but this seemed to be the original intent.
            fnesses = np.array([ind.fitness for ind in self.individuals])
            # Since fnesses is an array, most of the mathematical operations in
            # this function are applied elementwise!
            fnesses -= fnesses.min()
            fnesses /= fnesses.sum()
            contribution = fnesses * self.n_indiv

            remainder = contribution - np.trunc(contribution)
            contribution = np.trunc(contribution).astype(int)

            # <rest> is a function with one array argument! It works elementwise
            # and returns a bool array!
            rest = np.vectorize(lambda prob: uniform(0.0, prob) < 0.5)
            contribution += rest(remainder)  # bool gets casted to int implicitly

            return contribution

        def generate_candidate_individuals_for_next_generation(contributions):
            candidates = []
            for i, (individual, contrib) in enumerate(zip(self.individuals, contributions)):
                for _ in range(contrib):
                    # This hack with the type() function is a but ugly, but basically
                    # 'type(obj)(*args)' returns a new object of type 'type(obj)'
                    candidates.append(type(individual)(p=self.params))
            diff = len(self.individuals) - len(candidates)

            for _ in range(diff):
                typ = self.indivtype1 if random() < self.params.p_ann else self.indivtype2
                candidates.append(typ(p=self.params))
            return candidates

        def pick_new_gen_individuals_from_the_pool_of_candidates(candidates):
            new_generation = []
            while len(new_generation) != self.n_indiv:
                ind = choice(candid)
                candidates.remove(ind)
                new_generation.append(ind)
            return new_generation

        contrb = calculate_contributions_to_next_generation_from_fitnesses()
        candid = generate_candidate_individuals_for_next_generation(contrb)
        self.individuals = pick_new_gen_individuals_from_the_pool_of_candidates(candid)

        self.uptodate = False

    def pairing(self):
        pt = self.pairing_type[:6]
        if pt == "one to":
            for indiv in self.individuals:
                indiv.fitness = random()
                indiv.mutate(self.mut_prob)
            self.individuals.sort(key=lambda ind: ind.fitness)
            for one, other in zip(self.individuals[::2], self.individuals[1::2]):
                self.update_fitness(one, other)
        elif pt == "random":
            # Why is there no mutation when pairing is set to random?
            for i in range(self.n_indiv):
                self.update_fitness(self.individuals[i], self.individuals[randrange(self.n_indiv)])
        self.uptodate = True

    def negotiate(self, p1, p2):
        """
        Elaine's negotiate function's replicate

        I barely touched this, I tried to reimplement it using recursion,
        but I didn't manage to pull it off.
        """
        inputs1 = [0.0 for _ in range(p1.n_input)]
        inputs2 = [0.0 for _ in range(p2.n_input)]
        # This is not right in my opinion
        # We either should pass the quality as an input constantly
        # or we shouldn't pass it at all, because a weight gets assigned
        # to the corresponding input node and if we pass the quality as
        # inputs one time and an effort the next time, that weight loses
        # its meaning.
        # Also the Linear type individual only calculates with the 0th element
        # of this array, so it won't receive the quality information!
        inputs1[-1] = p1.quality
        inputs2[-1] = p2.quality

        px1 = p1.calc_effort(inputs1)
        inputs1[0] = inputs2[0] = px1
        px2 = p2.calc_effort(inputs2)
        inputs1 = [0.0] + inputs1[:-1]
        inputs2 = [0.0] + inputs2[:-1]

        cx1, cx2 = 0.0, 0.0

        for i in range(self.negotiation_max):
            cx1 = p1.calc_effort(inputs1)
            inputs1[0] = cx1
            inputs2[0] = cx1
            cx2 = p2.calc_effort(inputs2)
            inputs1 = [0.0] + inputs1[:-1]
            inputs2 = [0.0] + inputs2[:-1]
            inputs1[0] = cx2
            inputs2[0] = cx2

            if abs(cx1 - px1) + abs(cx2 - px2) < self.negotiation_tol:
                break

        return cx1, cx2

    def update_fitness(self, p1, p2):
        if p1.type_code == p2.type_code and random() < self.prob_recomb:
            self.recombination(p1, p2)
        x1, x2 = self.negotiate(p1, p2)
        p1.effort = x1
        p2.effort = x2
        # What in the heavens is qk??? And this quality thing?
        q1 = self.qk[p1.quality]
        q2 = self.qk[p2.quality]
        p1.fitness = self.fitness_fun(x1, x2, q1, self.max_qual)
        p2.fitness = self.fitness_fun(x2, x1, q2, self.max_qual)
        pass

    @staticmethod
    def recombination(p1, p2):
        chrom = p1.chromosome
        p1.chromosome = p2.chromosome
        p2.chromosome = chrom

    @property
    def grade(self):
        if not self.uptodate:
            self.pairing()
        return sum((ind.fitness for ind in self.individuals)) / self.n_indiv

    def describe(self, write_to_log=False):
        if not self.uptodate:
            self.pairing()
        chain = "        TYPECODE\tI\tQ\tEFFORT\tFITNESS\n"
        chain += "-" * len(chain) * 2
        chain += "\n"
        for i in range(self.n_indiv):
            pi = self.individuals[i]
            chain += "{}\t{}\t{}\t{}\t{}\n".format(pi.type_code, i, pi.quality,
                                                   round(pi.effort, 5), round(pi.fitness, 5))
        print(chain)
        if write_to_log:
            log("\n" + chain)
