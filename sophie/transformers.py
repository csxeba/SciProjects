from csxdata.utilities.highlevel import transform, plot
from SciProjects.sophie import wineframe

_axlabels = {"pca": ("PC1", "PC2", "PC3"),
             "lda": ("LD1", "LD2", "LD3"),
             "ica": ("IC1", "IC2", "IC3")}

plot(wineframe.learning[:, (0, 2)], wineframe.indeps,
     ("DH1", "D13C"), ellipse_sigma=1)

for transformation in ("pca", "lda", "ica"):
    trX = transform(wineframe.learning, 2, False,
                    transformation, wineframe.indeps)
    plot(trX, wineframe.indeps, _axlabels[transformation],
         ellipse_sigma=1)
