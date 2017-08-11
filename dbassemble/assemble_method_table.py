import os
import pickle

from SciProjects.dbassemble import projectroot

outchain = []

for methodobj in (pickle.load(path) for path in (os.listdir(projectroot + "methodpklz"))):
    outchain.append(methodobj.)
