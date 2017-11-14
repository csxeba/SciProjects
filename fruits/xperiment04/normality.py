from csxdata.stats import correlation
from csxdata.stats import normaltest
from csxdata.visual.histogram import fullplot

from SciProjects.fruits.fruitframe import FruitData


frame = FruitData(transform=True)
X = frame.volatile
correlation(X, names=X.columns)
normaltest.full(X, names=X.columns)
for col in X:
    fullplot(X[col], paramname=col)
