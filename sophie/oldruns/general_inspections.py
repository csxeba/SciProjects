from SciProjects.sophie import projectroot

from csxdata.utilities.parser import parse_csv
from csxdata.utilities.vectorop import dropna
from csxdata.stats.inspection import category_frequencies, correlation
from csxdata.stats.normality import full

X, Y, head = parse_csv(projectroot + "01GEO.csv",
                       indeps=2, headers=1, decimal=True)

category_frequencies(Y)
X, Y = dropna(X, Y)
correlation(X, ["X", "Y", "DH1", "DH2"])
full(X)
