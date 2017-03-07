from SciProjects.rich.util import pull_data

from csxdata.stats.inspection import correlation

X, Y, header = pull_data()
correlation(X, Y)
