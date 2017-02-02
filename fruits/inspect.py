from SciProjects.fruits import gyumindeps, gyumpath

from csxdata.utilities.parsers import parse_csv
from csxdata.stats.inspection import category_frequencies

X, y, head = parse_csv(gyumpath, gyumindeps, feature="Species", absval=True)

category_frequencies(y)
