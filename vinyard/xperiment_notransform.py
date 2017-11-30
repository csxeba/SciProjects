from SciProjects.vinyard.utility import WineData

from csxdata.visual.scatter import Scatter2D
from csxdata.utilities.vectorop import drop_lowNs

FEATURE = "CULTIVAR"

dw = WineData()[[FEATURE, "DH1", "D18O"]].dropna()
Y, X = dw[FEATURE].as_matrix(), dw[["DH1", "D18O"]].as_matrix()
Y, X = drop_lowNs(10, Y, X)

scat = Scatter2D(X, Y, title="Untransformed", axlabels=["$(D/H)_I$", "$\delta ^ {18}O$"])
scat.split_scatter(legend=True, show=True)
