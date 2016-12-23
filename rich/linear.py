import numpy as np

from project_rich.util import pull_data


def print_correlation(delay=0):
    X, y, headers = pull_data()
    dX = np.gradient(X, axis=0)
    ddX = np.gradient(dX, axis=0)

    correlation = np.corrcoef(X.T)
    print("Correlation:")
    print("\t"+"\t\t\t  ".join(headers[0][1:]))
    for i, row in enumerate(correlation):
        print(headers[0][i+1], row, sep="\t")

if __name__ == '__main__':
    print_correlation()
