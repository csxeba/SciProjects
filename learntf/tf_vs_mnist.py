import numpy as np
import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data

from SciProjects.learntf import projectroot


def _shuffle(X, Y):
    assert len(X) == len(Y)
    arg = np.arange(len(X))
    np.random.shuffle(arg)
    return X[arg], Y[arg]


class TFPerceptron:

    def __init__(self, indim, hiddens, outdim):
        self.X = tf.placeholder(tf.float32, [None, indim], name="inputs")
        self.Y = tf.placeholder(tf.float32, [None, outdim], name="labels")
        Wh = tf.Variable(tf.random_normal([indim, hiddens]), name="Wh")
        Wo = tf.Variable(tf.random_normal([hiddens, outdim]), name="Wo")
        bh = tf.Variable(tf.zeros([hiddens]), name="bh")
        bo = tf.Variable(tf.zeros([outdim]), name="bo")

        H = tf.nn.tanh(self.X @ Wh + bh, name="H")
        Z = H @ Wo + bo
        self.output = tf.nn.softmax(Z, name="output")
        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=Z, labels=self.Y, name="xent"))
        eq = tf.equal(tf.argmax(Z, 1), tf.argmax(self.Y, 1))
        self.acc = tf.reduce_mean(tf.cast(eq, tf.float32), name="acc")

        self._train_step = tf.train.AdamOptimizer().minimize(self.cost, name="trainstep")
        self.session = tf.InteractiveSession()
        tf.global_variables_initializer().run()

    def fit(self, X, Y, batch_size=32, epochs=10, validation=()):
        for epoch in range(epochs):
            print("-"*50)
            print(f"Epoch {epoch}")
            X, Y = _shuffle(X, Y)
            self._epoch(X, Y, batch_size, validation)

    def _epoch(self, X, Y, batch_size=32, validation=()):
        N = len(X)
        strln = len(str(N))
        stream = ((X[start:start+batch_size], Y[start:start+batch_size])
                  for start in range(0, len(X), batch_size))
        done = 0
        for x, y in stream:
            cost = self._fit_batch(x, y)
            done += len(x)
            print(f"\rTraining... {done:>{strln}}/{N} Cost: {cost:.4f}", end="")
        print()
        if validation:
            vcost, vacc = self.evaluate(*validation)
            print(f"Validation cost: {vcost}, acc: {vacc}")

    def _fit_batch(self, X, Y):
        cost, _ = self.session.run([self.cost, self._train_step], feed_dict={self.X: X, self.Y: Y})
        return cost

    def predict(self, X):
        return self.session.run(self.output, feed_dict={self.X: X})

    def evaluate(self, X, Y):
        cost = self.session.run(self.cost, feed_dict={self.X: X, self.Y: Y}).mean()
        acc = self.session.run(self.acc, feed_dict={self.X: X, self.Y: Y})
        return cost, acc


def load_data():
    mnist = input_data.read_data_sets(projectroot + "train/", one_hot=True, reshape=True, validation_size=10000)
    return mnist


def xperiment():
    mnist = load_data()
    model = TFPerceptron(784, 60, 10)
    model.fit(mnist.train.images, mnist.train.labels, validation=(mnist.test.images, mnist.test.labels))


if __name__ == "__main__":
    xperiment()
