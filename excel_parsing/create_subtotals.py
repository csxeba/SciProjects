import numpy as np
import pandas as pd

from SciProjects.excel_parsing import projectroot

data = pd.read_excel(projectroot + "BEERK.xlsx").as_matrix()

categ = np.unique(data[:, 0])
chain = ""

