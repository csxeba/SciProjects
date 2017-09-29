from csxdata.stats.inspection import correlation
from rich.currency.util import pull_data

X, Y, header = pull_data()
correlation(X, Y)
