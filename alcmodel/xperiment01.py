import pandas as pd

from SciProjects.alcmodel import projectroot, convert


df = pd.read_excel(projectroot + "Convertme01.xlsx")
df["RHO"] = convert(df["VV"].as_matrix())

df.to_excel(projectroot + "Output01.xlsx")
