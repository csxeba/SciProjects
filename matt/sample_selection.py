import numpy as np
import pandas as pd

from SciProjects.matt import projectroot

category = ["EURODAT", "GYUM", "EV"]
params_inc = ["D13C", "log_ACALD", "log_ETAC", "log_ACETAL",
              "log_1PROP", "log_2M1B", "log_3M1B"]

data = pd.read_excel(projectroot + "Param_szurt.xlsx", header=0)
valid = data[category + params_inc].dropna()
X = valid[params_inc]
X = (X - X.mean()) / X.std()
valid[params_inc] = X

ds = []

for categ in ("Alma", "Kajszi", "Málna"):
    x = valid[valid["GYUM"] == categ][params_inc].as_matrix()
    center = x.mean(axis=0)
    print(categ, "center:", center)
    ids = valid[valid["GYUM"] == categ][category].as_matrix()
    for ID, record in zip(ids, x):
        d = np.linalg.norm(center - record)
        ds.append(ID.tolist() + [d])

outchain = "\t".join(category + ["D"]) + "\n"
outchain += "\n".join("\t".join(map(str, line)) for line in ds)

with open(projectroot + "distances.csv", "w") as handle:
    handle.write(outchain.replace(".", ","))
