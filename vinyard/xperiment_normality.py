from matplotlib import pyplot as plt

from csxdata.visual import histogram

from SciProjects.vinyard.utility import WineData


wd = WineData()

isotope = wd[["DH1", "DH2", "D13C", "D18O"]].dropna()

# inspection.correlation(isotope, names=isotope.columns)
# normaltest.full(isotope, names=isotope.columns)

fig, axarr = plt.subplots(4, 2)

titles = {"DH1": "$(D/H)_I$", "DH2": "$(D/H)_{II}$",
          "D13C": r"$\delta^{13}C$",
          "D18O": r"$\delta^{18}O$"}

for col, (lax, rax) in zip(isotope.columns, axarr):
    x = isotope[col]
    hist = histogram.Histogram(x, ax=lax)
    hist.plot(axtitle=f"{titles[col]} Histogram")
    nprob = histogram.NormProb(x, ax=rax)
    nprob.plot(axtitle=f"{titles[col]} NormProb")

plt.show()
