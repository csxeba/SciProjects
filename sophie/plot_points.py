from sklearn.feature_selection import f_classif

from csxdata.utilities.parsers import parse_csv
from csxdata.utilities.highlevel import plot, transform

from SciProjects.sophie import projectroot


X, Y, head = parse_csv(projectroot + "01GEO.csv",
                       indeps=4, headers=1, decimal=True,
                       discard_nans=True, discard_class_treshold=5,
                       feature="COUNTRY")
tX = transform(X, factors=1, get_model=False, method="lda", y=Y)

print("F: {}, pval: {}".format(*f_classif(tX, Y)))
plot(X, Y, axlabels=["$(D/H)_I$", r"$\delta^{13}C$"], ellipse_sigma=2)
