import pandas as pd

from matplotlib import pyplot as plt

from csxdata import CData
from csxdata.visual import Plotter2D
from SciProjects.matt import projectroot

param = ["D13C", "log_ACALD", "log_ETAC", "log_ACETAL", "log_1PROP", "log_2M1B", "log_3M1B"]

df = pd.read_excel(projectroot + "Param_szurt.xlsx", header=0)

data = CData((df[param].as_matrix(), df[["GYUM"]].as_matrix()), cross_val=0)
data.set_transformation("lda", 2)

print(*data.transformation._model.explained_variance_ratio_, sep="\t")
print(*data.transformation._model.intercept_, sep="\t")
with open(projectroot + "LDA_loadings.csv", "w") as handle:
    handle.write(
        "\n".join("\t".join(line) for line in data.transformation._model.coef_.astype(str))
    )

plot = Plotter2D(plt.gcf(), data.learning, data.lindeps, axlabels=["Factor01", "Factor02"])
plot.split_scatter(center=False, label=False)
plot.add_legend(plt)

plt.show()
