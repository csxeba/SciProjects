import numpy as np
from matplotlib import pyplot as plt
from shapefile import Reader

from csxdata import roots
from SciProjects.riskanalyze import projectroot
from SciProjects.riskanalyze.utils import pull_data

hun = np.array(Reader(roots["gis"] + "hun/HUN_adm0.shp").shapes()[0].points)
xy, data = pull_data()
date = np.array([s.replace(".", "-") for s in data[:, 2]], dtype="datetime64[D]")

# tdelta = (date - date.min()).astype(int)
# heatmap, xedges, yedges = np.histogram2d(*xy.T, bins=100)
# extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
plt.plot(*hun.T, "w-", linewidth=1)
plt.hexbin(*xy.T, bins="log", cmap="hot", gridsize=50)
plt.savefig(projectroot + "HexBin.png")
plt.show()
