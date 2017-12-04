import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from SciProjects.alice_weight import projectroot

df = pd.read_excel(projectroot + "/alice_weight.xlsx")
print(df.dtypes)

df["tdelta"] = (df.date - df.date[0]).as_matrix().astype(int)
# df["grams"] -= df["grams"].min()

X = df.tdelta.as_matrix()
Y = (df.grams - df.grams.min()).as_matrix()
Y /= Y.max()
# e^Y = Ax + B
# Y = log(Ax) + log(B)

# X = np.log(X / X.max())
# Y = np.exp(Y / Y.max())
# Y = Y / Y.max()


plt.plot(X, Y)
plt.scatter(X, Y)
plt.grid(True)
plt.show()
