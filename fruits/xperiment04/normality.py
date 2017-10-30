import pandas as pd

from csxdata.stats import correlation
from csxdata.stats import normaltest
from csxdata.visual.histogram import fullplot

from SciProjects.fruits import projectroot


df = pd.read_excel(projectroot + "convert.xlsx")
print(df.dtypes)

normaltest.full(df.iloc[:, 19:].as_matrix(), names=df.columns[7:])

for param in df.columns[19:]:
    fullplot(df[param].as_matrix(), param)
correlation(df.iloc[:, 19:].as_matrix(), df.columns[19:])
