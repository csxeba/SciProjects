import os

import numpy as np
import pandas as pd

from SciProjects.vinyard import projectroot
from SciProjects.vinyard.structure import WineData


def main():
    df = WineData().raw
    print(df.dtypes)


if __name__ == "__main__":
    main()
