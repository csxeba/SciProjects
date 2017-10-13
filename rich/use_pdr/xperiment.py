import time
import matplotlib.pyplot as plt

import pandas_datareader as pdr


start = time.time()
times = []
try:
    for i in range(10):
        print(i+1)
        pdr.get_data_yahoo("AAPL")
        times.append(time.time() - start)
except Exception as E:
    print("Loop raised", str(E))
finally:
    print(f"TIMEREQ: {(time.time() - start)/len(times):.2f} s")
    plt.plot(range(len(times)), times)
    plt.show()
