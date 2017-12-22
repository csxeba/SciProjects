import os

import numpy as np
import pandas as pd

from SciProjects.alcmodel import Converter


df = pd.read_excel(os.path.expanduser("~/tmp/kozma.xlsx"))
valid = df.iloc[:, 8:]
alc = df["ALK"]

conv = Converter().to_absalc(alc, valid)
pd.DataFrame(data=conv, columns=valid.columns).to_excel(os.path.expanduser("~/tmp/output.xlsx"))
