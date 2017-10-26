import numpy as np
import pandas as pd

from csxdata.visual.histogram import fullplot
from csxdata.stats import correlation

from SciProjects.isovol import projectroot


df = pd.read_excel(projectroot + "AllData.zrg.xlsx")
print(df.dtypes)

X, Y = df.loc[:, "qETOH":"iAMYL"].as_matrix(), df["GYUM"].as_matrix()

X[:, :5] = np.log(X[:, :5])

correlation(X, names=df.columns[4:])

for col in df.columns[4:]:
    fullplot(df[col], col, 7)
