from matplotlib import pyplot as plt

from SciProjects.alcmodel import get_model, get_reference


df = get_reference()
curve = get_model(2, df)

X = df["VV"]

plt.plot(X, df["DENSE20"], "b-", alpha=0.5)
plt.plot(X, curve(X), "r-")
plt.show()
