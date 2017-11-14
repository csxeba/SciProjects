from csxdata.visual import spiderplot
from csxdata.utilities.vectorop import standardize

from SciProjects.fruits.fruitframe import FruitData


df = FruitData(transform=False)
X, Y = df.volatile, df["FAMILIA"]

# bycat = split_by_categories(Y, X)

spiderplot.split_gridlike(standardize(X), Y, X.columns, ncols=3)
