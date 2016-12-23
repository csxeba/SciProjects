# Stdlib imports
import abc
import numpy as np
from random import randrange, uniform, random
from src.util import rectify, sigmoid


class Individual(abc.ABC):
    """
    Abstract base class of Individual Response Types

    Cannot be instanciated, only defines the interface and
    some basic data attributes of its derivatives
    """

    def __init__(self, p, typ):
        self.fitness = 0.0
        self.effort = 0.0
        self.type = typ
        self.quality = randrange(p.max_qual)
        self.n_node = 0
        self.n_input = 2
        self.delta = p.delta

        # self.qk = p.qk

    @abc.abstractmethod
    def mutate(self, prob): raise NotImplementedError

    @abc.abstractmethod
    def calc_effort(self, inputs): raise NotImplementedError

    @property
    @abc.abstractmethod
    def chromosome(self): raise NotImplementedError

    @chromosome.setter
    def chromosome(self, value): raise NotImplementedError

    @abc.abstractproperty
    def type_code(self): raise NotImplementedError


class ANNIndividual(Individual):
    """
    Abstraction of an Individual with <ANN type> response
    as in Artificial Neural Network.

    The original structure of its chromosome:
    [n_node * n_input + 2] + [self.n_node + 2]
    [the hidden weights  ] + [the output weights]

    I omit the rho and I convert the threshold to bias (1 - th), so
    the effort simplifies to sigmoid(input . weights) where . denotes
    the vector-matrix product.

    This neural network architecture is equivalent to the fully connected
    time distributed dense neural network with 2 input nodes.
    """

    def __init__(self, p, model=None):
        Individual.__init__(self, p, typ="ANN")
        self.n_input = p.n_input
        self.n_node = p.n_node
        self.w_min = p.min_ann
        self.w_max = p.max_ann
        self.cl = self.n_node * (self.n_input + 2) + self.n_node + 2
        if model is None:
            self.weights = [np.random.uniform(low=self.w_min, high=self.w_max, size=(self.n_input, self.n_node)),
                            np.random.uniform(low=self.w_min, high=self.w_max, size=(self.n_node, 1))]
            self.biases = [np.random.uniform(low=self.w_min, high=self.w_max, size=(self.n_node,)),
                           np.random.uniform(low=self.w_min, high=self.w_max, size=(1,))]
        else:
            self.fitness = self.effort = model.fitness
            self.weights = np.copy(model.weights)  # create a copy, not just a reference
            self.biases = np.copy(model.biases)

    @property
    def chromosome(self):
        w1 = self.n_input*self.n_node
        w2 = w1 + self.n_node
        b1 = w2 + self.n_node
        b2 = b1 + 1
        chrom = np.zeros((self.cl,))
        chrom[:w1] = np.ravel(self.weights[0])
        chrom[w1:w2] = np.ravel(self.weights[1])
        chrom[w2:b1] = np.ravel(self.biases[0])
        chrom[b1:b2] = np.ravel(self.biases[1])
        return chrom

    @chromosome.setter
    def chromosome(self, chrom):
        if self.cl != len(chrom):
            raise RuntimeError
        w1 = self.n_input*self.n_node
        w2 = w1 + self.n_node
        b1 = w2 + self.n_node
        b2 = b1 + 1
        self.weights = [chrom[:w1].reshape(self.n_input, self.n_node),
                        chrom[w1:w2].reshape(self.n_node, 1)]
        self.biases = [chrom[w2:b1].reshape(self.n_node,),
                       chrom[b1:b2].reshape(1,)]

    def mutate(self, prob):
        """
        Mutate the ANN's weights by a gaussian random value
        of mu = 0.0 and sigma = delta
        """

        def manipulate_parameters(params):
            """Nested function, only the local scope sees it"""
            mask = np.random.binomial(1, prob, params.shape)
            gauss = np.random.randn(*params.shape) * self.delta
            params += gauss * mask
            return rectify(params, self.w_min, self.w_max)

        self.weights[0], self.weights[1], self.biases[0], self.biases[1] = \
            tuple(map(manipulate_parameters, self.weights + self.biases))

    def calc_effort(self, inputs):
        """
        Effort is calculated by forward-propagating
        the inputs through the neural network
        """
        stimuli = np.array(inputs)
        for w, b in zip(self.weights, self.biases):
            z = stimuli.dot(w) + b
            stimuli = sigmoid(z)
        return float(stimuli)

    def __str__(self):
        return "ANN ({}-{}-{}; q: {})".format(self.n_input, self.n_node, 1, self.quality)

    @property
    def type_code(self):
        return str(self)


class RNNIndividual(Individual):
    """
    Abstraction of an Individual with <RNN type> response
    as in Recurrent Neural Network

    This neural network has a hidden layer, which receives its own previous
    output (hidden_out) as input in the next output generation phase and in theory
    it has a different weight set fot the hidden-hidden connections.
    For faster computation I concatenate the input vector (X) and the vector
    hidden_out (producing Z) and also unify the input-hidden (Wx) and hidden-hidden (Wh)
    weight matrices to W and bias vectors (bx, bh) to b.

    The theoretical output of the recurrent layer is as follows:

    hidden_out = sigmoid((X . Wx + bx) + (hidden_out . Wh + bh))
    this becomes the following:
    hidden_out = sigmoid(Z . W + b)

    The hidden_out is fed to an output layer, which is the usual densely connected neural layer
    with weight matrix Wo and bias vector bo.

    network_out = sigmoid(hidden_out . Wo + b)
    """

    def __init__(self, p, model=None):
        Individual.__init__(self, p, typ="RNN")
        self.n_input = 1
        self.n_node = p.n_node
        self.z = self.n_input + self.n_node
        self.w_min = p.min_ann
        self.w_max = p.max_ann
        self.hidden_out = np.zeros((self.n_node,))
        self.cl = self.z * self.n_node + self.n_node + self.n_node + 1

        if model is None:
            self.W = np.random.uniform(low=self.w_min, high=self.w_max, size=(self.z, self.n_node))
            self.b = np.random.uniform(low=self.w_min, high=self.w_max, size=(self.n_node,))
            self.Wo = np.random.uniform(low=self.w_min, high=self.w_max, size=(self.n_node, 1))
            self.bo = np.random.uniform(low=self.w_min, high=self.w_max, size=(1,))

        else:
            self.fitness = self.effort = model.fitness
            self.W = np.copy(model.W)
            self.b = np.copy(model.b)
            self.Wo = np.copy(model.W)
            self.bo = np.copy(model.b)
        pass

    def calc_effort(self, inputs):
        Z = np.concatenate((np.array(inputs[:self.n_input]), self.hidden_out))
        self.hidden_out = sigmoid(Z.dot(self.W) + self.b)
        output = sigmoid(self.hidden_out.dot(self.Wo) + self.bo)
        return float(output)

    def mutate(self, prob):

        def manipulate_parameters(params):
            """Nested function, only the local scope sees it"""
            mask = np.random.binomial(1, prob, params.shape)
            gauss = np.random.randn(*params.shape) * self.delta
            params += gauss * mask
            params = np.maximum(self.w_min, np.minimum(self.w_max, params))
            return params

        self.W, self.b, self.Wo, self.bo = tuple(map(manipulate_parameters,
                                                     [self.W, self.b, self.Wo, self.bo]))

    @property
    def chromosome(self):
        W = self.z * self.n_node
        b = W + self.n_node
        Wo = b + self.n_node
        bo = Wo + 1
        chrom = np.zeros((self.cl,))
        chrom[:W] = np.ravel(self.W)
        chrom[W:b] = np.ravel(self.b)
        chrom[b:Wo] = np.ravel(self.Wo)
        chrom[Wo:bo] = np.ravel(self.bo)
        return chrom

    @chromosome.setter
    def chromosome(self, chrom):
        if self.cl != len(chrom):
            raise RuntimeError
        W = self.z * self.n_node
        b = W + self.n_node
        Wo = b + self.n_node
        bo = Wo + 1
        self.W = chrom[:W].reshape(self.z, self.n_node)
        self.b = chrom[W:b]
        self.Wo = chrom[b:Wo].reshape(self.n_node, 1)
        self.bo = chrom[Wo:bo]

    @property
    def type_code(self):
        return str(self)

    def __str__(self):
        return "RNN ({}-{}-{}; q: {})".format(self.n_input, self.n_node, 1, self.quality)


class LSTMIndividual(Individual):
    """
    Abstraction of an Individual with <LSTM type> response
    as in Long/Short Term Memory (Recurrent Neural Network subtype)
    A recurrent neural network architecture with a memory cell (C)

    LSTM Layer works as follows:
    ----------------------------
    it accepts an input (X) and concatenates it with
    its previus output (self.hidden_out), producing Z.
    A "forget" gate (f) gets computed so: simgoid(Z . Wf + bf)
    An "input" gate (i) gets computed so: sigmoid(Z . Wi + bi)
    A "candidate" memory (cand) gets computed: sigmoid(Z . Wc + bc)
    An "output" gate (o) gets computed so: sigmoid(Z . Wo + bo)
    [For the sake of speed, the gate activations are computed in parallel
    by cocatenating the gate weights (W) and gate biases (b) together and
    computing gates = sigmoid(Z . W + b)]

    A portion of the memory cell's contets are forgotten: C *= f
    The candidate memory is added in after the application
    of the input gate on it: C += cand * i
    The output is generated by appliing the output gate to the
    memory cell so: h_out = o * sigmoid(C)

    The LSTM layer's output is finally fed into a densely connected
    output layer which produces the network output (the effort)

    Structure of the chromosome:
    [4 * (n_input + n_node)] + [4 * n_node]    + [n_node * 1]  + 1
    W of gates and Wc        + b of gates + bc + [W of output] +  bias of output
    """

    def __init__(self, p, model=None):
        Individual.__init__(self, p, typ="RNN")
        self.n_node = p.n_node
        self.n_input = 1
        self.z = self.n_node + self.n_input
        self.w_min = p.min_ann
        self.w_max = p.max_ann
        self.cl = (self.z * 4 * self.n_node) + 4 * self.n_node + self.n_node + 1
        self.hidden_out = np.zeros((self.n_node,))
        self.memory = np.zeros((self.n_node,))
        if model is None:
            self.W = np.random.uniform(low=self.w_min, high=self.w_max, size=(self.z, 4*self.n_node))
            self.b = np.random.uniform(low=self.w_min, high=self.w_max, size=(4*self.n_node,))
            self.Wo = np.random.uniform(low=self.w_min, high=self.w_max, size=(self.n_node,))
            self.bo = np.random.uniform(low=self.w_min, high=self.w_max, size=(1,))
        else:
            self.fitness = self.effort = model.fitness
            self.W = np.copy(model.weights)
            self.b = np.copy(model.biases)
            self.Wo = np.copy(model.rweights)
            self.bo = np.copy(model.rbiases)
        pass

    def calc_effort(self, inputs):
        Z = np.concatenate((np.array(inputs[:self.n_input]), self.hidden_out))
        preact = Z.dot(self.W) + self.b
        f, i, o, candidate = np.split(sigmoid(preact), 4)
        self.memory *= f
        self.memory += i * candidate
        self.hidden_out = o * sigmoid(self.memory)

        output = sigmoid(self.hidden_out.dot(self.Wo) + self.bo)

        return float(output)

    def mutate(self, prob):
        def manipulate_parameters(params):
            """Nested function, only the local scope sees it"""
            mask = np.random.binomial(1, prob, params.shape)
            gauss = np.random.randn(*params.shape) * self.delta
            params += gauss * mask
            params = np.maximum(self.w_min, np.minimum(self.w_max, params))
            return params

        self.W, self.b, self.Wo, self.bo = tuple(map(manipulate_parameters,
                                                     [self.W, self.b, self.Wo, self.bo]))

    @property
    def chromosome(self):
        W = self.z * 4 * self.n_node
        b = W + 4 * self.n_node
        Wo = b + self.n_node
        bo = Wo + 1
        chrom = np.zeros((self.cl,))
        chrom[:W] = np.ravel(self.W)
        chrom[W:b] = np.ravel(self.b)
        chrom[b:Wo] = np.ravel(self.Wo)
        chrom[Wo:bo] = np.ravel(self.bo)
        return chrom

    @chromosome.setter
    def chromosome(self, chrom):
        if self.cl != len(chrom):
            raise RuntimeError
        W = self.z * 4 * self.n_node
        b = W + 4 * self.n_node
        Wo = b + self.n_node
        bo = Wo + 1
        self.W = chrom[:W].reshape(self.z, 4*self.n_node)
        self.b = chrom[W:b]
        self.Wo = chrom[b:Wo].reshape(self.n_node, 1)
        self.bo = chrom[Wo:bo]

    @property
    def type_code(self):
        return str(self)

    def __str__(self):
        return "LSTM ({}-{}-{}; q: {})".format(self.n_input, self.n_node, 1, self.quality)


class LinearIndividual(Individual):
    """
    Abstraction of an Individual with <Linear type> response

    The original structure of the chromosome:
    [rho, lambda, rho, lambda, ... ] len = 2 * chrom_len

    After observing the logic, I omitted the original construct of
    rhos and thetas indexed by the quality of the individual
    and only defined a single rho (converted to bias)
    and a single theta (renamed to weight)
    """

    def __init__(self, p, model=None):
        Individual.__init__(self, p, typ="Lin")
        self.n_input = 2
        self.n_node = 0
        self.bias_min = p.min_rho
        self.bias_max = p.max_rho
        self.weight_min = p.min_lambda
        self.weight_max = p.max_lambda
        self.max_qual = p.max_qual
        self.cl = 2

        if model is None:
            self.bias = uniform(self.bias_min, self.bias_max)
            self.weight = uniform(self.weight_min, self.weight_max)
        else:
            self.fitness = self.effort = model.fitness
            self.bias = model.bias
            self.weight = model.weights

    @property
    def chromosome(self):
        chrom = np.zeros((2,))
        chrom[0] += self.bias
        chrom[1] += self.weight
        return chrom

    @chromosome.setter
    def chromosome(self, chrom):
        self.bias = chrom[0]
        self.weight = chrom[1]

    def mutate(self, prob):

        self.bias += uniform(self.bias_min, self.bias_max) if random() < prob else 0.0
        self.weight += uniform(self.weight_min, self.weight_max) if random() < prob else 0.0
        self.bias = rectify(self.bias, self.bias_min, self.bias_max)
        self.weight = rectify(self.weight, self.weight_min, self.weight_max)

    def calc_effort(self, inputs):
        e = inputs[0] * self.weight + self.bias
        return max(0.0, e)

    def __str__(self):
        return "Lin (2-0-1; q: {})".format(self.quality)

    @property
    def type_code(self):
        return str(self)


class _Indiv:
    """
    Convenience class, which helps to retrieve the above declared
    classes given the proper keyword as string.
    """
    def __init__(self):
        self.dictionary = dict(zip(
            ["linear", "ann", "rnn", "lstm"],
            [LinearIndividual, ANNIndividual,
             RNNIndividual, LSTMIndividual]))

    def __getitem__(self, item):
        item = item.lower()
        if item not in self.dictionary:
            raise IndexError("{} is not a valid Individual response type!".format(item))
        return self.dictionary[item]

# Instance of the convenience class
# a class can be retrieved so: indivtypes["typename"]
indivtypes = _Indiv()
