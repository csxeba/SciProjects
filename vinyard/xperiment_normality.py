from csxdata.stats import normaltest, inspection
from csxdata.visual import histogram

from SciProjects.vinyard.utility import WineData


wd = WineData()

isotope = wd[["DH1", "DH2", "D13C", "D18O"]].dropna()

normaltest.full(isotope, names=isotope.columns)
inspection.correlation(isotope, names=isotope.columns)

for col in isotope:
    histogram.fullplot(isotope[col], paramname=col)
