from SciProjects.sophie import projectroot

from csxdata.utilities.parsers import parse_csv
from csxdata.utilities.vectorops import discard_NaN_rows
from csxdata.stats.inspection import category_frequencies, correlation
from csxdata.stats.normality import full

X, Y, head = parse_csv(projectroot + "01GEO.csv",
                       indeps=2, headers=1, decimal=True)

category_frequencies(Y)
X, Y = discard_NaN_rows(X, Y)
correlation(X, ["X", "Y", "DH1", "DH2"])
full(X)
