from matplotlib import pyplot as plt

from csxdata.visual import histogram
from csxdata.stats import normaltest, inspection

from SciProjects.fruitwinestat.merge_data import pull_merged_data, PARAM


def main():
    df = pull_merged_data("MEGYE")
    print()
    inspection.category_frequencies(df["MEGYE"])
    normaltest.full(df[PARAM], names=PARAM)
    # inspection.correlation(df[PARAM], names=PARAM)
    print()

    fig, axarr = plt.subplots(3, 2, figsize=(5, 10))

    for param, (histax, probax) in zip(PARAM, axarr):
        x = df[param]
        print(f"SKEW of {param}: {x.skew()}")
        histogram.Histogram(x, ax=histax).plot(axtitle=f"{param} histogram")
        histogram.NormProb(x, ax=probax).plot(axtitle=f"{param} Norm. prob. plot")
    plt.suptitle("Normality test on the merged fruit-wine datasets")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
