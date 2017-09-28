from numpy.linalg.linalg import LinAlgError as LErr

from csxdata.utilities.parser import parse_csv
from csxdata.utilities.highlevel import plot, transform
from csxdata.stats.inspection import category_frequencies

from SciProjects.fruits import gyumpath

selection = "Kajszi"

X, Y, head = parse_csv(gyumpath, 4, feature="Year")
print("SELECTION IS", "nincs")
category_frequencies(Y)

nolda = False

try:
    lX = transform(X[:, :3], 2, False, "lda", Y)
except LErr:
    nolda = True
    lX = None

rawlbl = "DH1", "D13C"
ldalbl = "LD1", "LD2"

plot(X[:, (0, 2)], Y, axlabels=rawlbl, ellipse_sigma=1)
if not nolda:
    plot(lX, Y, axlabels=ldalbl, ellipse_sigma=1)
