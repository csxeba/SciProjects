from csxdata import CData, roots
from csxdata.stats.inspection import correlation, category_frequencies
from csxdata.stats.normality import full,

winesource = roots["csvs"] + "sophiewine.csv"
frame = CData(winesource, indeps=4, headers=1, cross_val=0., feature="COUNTRY", decimal=True)
category_frequencies(frame.indeps)
correlation(frame.data, ("DH1", "DH2", "D13C"))
full(frame.data)
