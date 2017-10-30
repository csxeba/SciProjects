import pandas as pd

from SciProjects.alcmodel import Converter
from SciProjects.fruits import projectroot


df = pd.read_excel(projectroot + "adat.xlsx")
print(df.dtypes)
converter = Converter(deg=3)
volcol = df.columns[11:]
aa = converter.to_absalc(df["ALK"].as_matrix(), df.loc[:, "METOH":].as_matrix())
for name, data in zip(volcol, aa.T):
    df["aa" + name] = data
df.to_excel(projectroot + "convert.xlsx")
