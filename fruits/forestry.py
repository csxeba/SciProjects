from sklearn.ensemble import RandomForestClassifier as RF

from csxdata import CData

from project_fruits.util import pull_data, pull_validation_data

LABEL = "familia"
PARAMSET = "all"


rf = RF(n_estimators=100, n_jobs=1)

data = CData(pull_data(label=LABEL, paramset=PARAMSET))
data.transformation = ("lda", 5)

valid = pull_validation_data(label=LABEL, paramset=PARAMSET)
valid = data.transform(valid[0]), valid[1]
rf.fit(data.learning, data.lindeps)

tpredict = rf.predict(data.testing)
vpredict = rf.predict(valid[0])
tacc = [right == left for right, left in zip(tpredict, data.tindeps)]
vacc = [right == left for right, left in zip(vpredict, valid[1])]
print("TPredictions ({}%):\n{}".format(int(100*sum(tacc)/len(tacc)), tpredict))
print("TestingY:\n", data.tindeps)
print("VPredictions ({}%):\n{}".format(int(100*sum(vacc)/len(vacc)), vpredict))
print("ValidY:\n", valid[1])
