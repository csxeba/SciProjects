from matplotlib import pyplot as plt

from csxdata import CData
from csxdata.visual import Plotter2D

from SciProjects.matt import projectroot

data = CData(projectroot + "Spitzke.data.xlsx", indeps=4, feature="ORIGIN", cross_val=0, headers=1, dropna=True)
data.set_transformation("pls", 2)

plot = Plotter2D(X=data.learning, y=data.lindeps, fig=plt.gcf(),
                 title="Spitzke PCA", axlabels=("PC01", "PC02"))
plot.split_scatter(center=True, label=True)
plt.show()
