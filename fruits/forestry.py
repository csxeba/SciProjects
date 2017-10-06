from sklearn.ensemble import RandomForestClassifier as RF

from csxdata import CData

from SciProjects.fruits import *


LABEL = "Familia"
rf = RF(n_estimators=100, n_jobs=1)

fruits = CData(gyumpath, gyumindeps, cross_val=0.2, feature=LABEL)
fruits.transformation = ("lda", 5)

zsind = CData(zsindpath, zsindeps, cross_val=0.0)
valid = fruits.transform(zsind._learning, zsind.lindeps)
rf.fit(fruits._learning, fruits.lindeps)

tpredict = rf.predict(fruits._testing)
vpredict = rf.predict(valid[0])
tacc = [right == left for right, left in zip(tpredict, fruits.tindeps)]
vacc = [right == left for right, left in zip(vpredict, valid[1])]
print("TPredictions ({}%):\n{}".format(int(100*sum(tacc)/len(tacc)), tpredict))
print("TestingY:\n", fruits.tindeps)
print("VPredictions ({}%):\n{}".format(int(100*sum(vacc)/len(vacc)), vpredict))
print("ValidY:\n", valid[1])
