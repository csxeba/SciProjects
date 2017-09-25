import numpy as np
import pandas as pd

from csxdata.utilities.vectorops import split_by_categories

from SciProjects.fruits import projectroot

category = ["EURODAT", "GYUM", "EV"]
isotope = ["DH1", "DH2", "D13C"]
volatile = ["METOH", "ACALD", "ETAC", "ACETAL", "2BUT",
            "1PROP", "2M1P", "1BUT", "2M1B", "3M1B"]
volatile_inc = ["METOH", "ACALD", "ETAC", "ACETAL",
                "1PROP", "2M1P", "2M1B", "3M1B"]

data = pd.read_excel(projectroot + "Gyümölcs_adatbázis_összesített.xlsx", header=0)
valid = data[category + volatile_inc].dropna()
X = valid[volatile_inc]
X = (X - X.mean()) / X.std()
valid[volatile_inc] = X

ds = []

for categ in ("Alma", "Kajszi", "Málna"):
    x = valid[valid["GYUM"] == categ][volatile_inc].as_matrix()
    center = x.mean(axis=0)
    print(categ, "center:", center)
    ids = valid[valid["GYUM"] == categ][category].as_matrix()
    for ID, record in zip(ids, x):
        ds.append(ID.astype(str).tolist() + [str(np.linalg.norm(center - record))])

with open(projectroot + "distances.csv", "w") as handle:
    handle.write("\n".join("\t".join(line) for line in ds))
