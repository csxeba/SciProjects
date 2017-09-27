import numpy as np
import pandas as pd

from SciProjects.fruits import projectroot

categ = ["EURODAT"]
etoh = ["ALK"]
volatile = ["METOH", "ACALD", "ETAC", "ACETAL", "2BUT",
            "1PROP", "2M1P", "1BUT", "2M1B", "3M1B"]


def get_model(deg=2):
    data = np.load(projectroot + "density_points.npa")
    X = np.linspace(0., 1., len(data))
    curve = np.poly1d(np.polyfit(X, data, deg=deg))
    R = np.corrcoef(data, curve(X))[0][1]
    print(f"Fitted {deg} degree LS curve with R2 = {R**2}")
    return curve


def convert(p, vv):
    """Param * rho_solution
    -------------------------- = Param_abs_ethanol
    volume_ratio * rho_ethanol
    """
    rho = density_curve(vv)
    return (p * rho) / (vv * RHO_ETOH)


df = pd.read_excel(projectroot + "Gyümölcs_adatbázis_összesített.xlsx", header=0)
valid = df[categ + etoh + volatile].dropna()  # type: pd.DataFrame
density_curve = get_model(2)

RHO_ETOH = density_curve(1.)

output = []
for i, row in valid.iterrows():
    vv = row["ALK"] * 0.01
    conv = [convert(p, vv) for p in row[volatile]]
    output.append([row["EURODAT"]] + conv)
output = np.array(output)

chain = "\t".join(categ + volatile) + "\n"
chain += "\n".join("\t".join(line) for line in output.astype(str))

with open(projectroot + "Converted_volatiles.csv", "w") as handle:
    handle.write(chain)
