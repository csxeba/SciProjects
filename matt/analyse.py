import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from csxdata import stats

from SciProjects.matt import projectroot

df = pd.read_excel(projectroot + "Kozma.Izotóp.eredmény.zrg.xlsx")

X = df.loc[:, "ETOH":"AMYL"]  # type: pd.DataFrame
Y = df["GYUM"]  # type: pd.Series

stats.correlation(X.dropna().as_matrix(), X.columns)

