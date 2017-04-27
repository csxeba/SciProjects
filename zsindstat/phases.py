from sklearn.feature_selection import f_oneway

from csxdata.stats import inspection
from csxdata.utilities.highlevel import plot, transform

from SciProjects.zsindstat.util import pull_data, axlab_latex


frame = pull_data("YEAR", filterby="FRUIT", selection="meggy")

inspection.category_frequencies(frame.indeps)
X = frame.learning
plot(X, frame.indeps, axlabels=axlab_latex, ellipse_sigma=2)
tX = transform(X, factors=1, get_model=False, method="lda", y=frame.indeps)

print("F: {}, pval: {}".format(*f_classif(tX, frame.indeps)))
