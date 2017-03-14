from SciProjects.xlcrawl import project_root

import os
import shutil

xlflz = []
for root, dirz, flz in os.walk(project_root):
    xlflz += [(root + "/", flnm) for flnm in flz if flnm[-4:] in ("xlsx", ".xls")]

for drnm, flnm in xlflz:
    shutil.copy(drnm + flnm, project_root + "ALLXLFLZ/" + flnm)
