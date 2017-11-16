import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

from SciProjects.learntf import projectroot


mnist = input_data.read_data_sets(projectroot + "train/", one_hot=False, reshape=True, validation_size=10000)
model = tf.estimator.DNNClassifier(
    hidden_units=[60],
    feature_columns=[tf.feature_column.numeric_column("x", shape=[784])],
    activation_fn=tf.nn.tanh,
    n_classes=10
)
train_infn = tf.estimator.inputs.numpy_input_fn({"x": mnist.train.images}, mnist.train.labels.astype(int),
                                                batch_size=32, num_epochs=10, shuffle=True, num_threads=1)
test_infn = tf.estimator.inputs.numpy_input_fn({"x": mnist.validation.images}, mnist.validation.labels.astype(int),
                                               shuffle=False)

tf.logging.set_verbosity(tf.logging.INFO)
model.train(train_infn)
print("Final evaluation")
model.evaluate(test_infn)
