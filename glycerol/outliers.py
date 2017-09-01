from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from matplotlib import pyplot as plt

from SciProjects.glycerol import pull_data


X = pull_data(concat=True)
model = IsolationForest()
model.fit(X)

pred = model.predict(X)

plt.scatter(*X[pred == 1].T, s=3, c="blue", label="Inliers")
plt.scatter(*X[pred == -1].T, s=3, c="red", label="Outliers")
plt.title("Outlier detection")
plt.show()
