import numpy as np

from matplotlib import pyplot as plt

from csxdata import roots

with open(roots["csvs"] + "szuki_suly.csv") as handle:
    data = [line.split("\t") for line in handle.read().split("\n")[1:] if line]

dates, days, ddays, grams = [[] for _ in range(4)]
for dt, dy, ddy, gr in data:
    dates.append(dt)
    days.append(dy)
    ddays.append(ddy)
    grams.append(gr)

dates, days, ddays, grams = list(map(np.array, (dates, days, ddays, grams)))
days, grams = days.astype(int), grams.astype(int)
ddays = np.diff(days.astype(float))
dgrams = np.diff(grams.astype(float))

fig, axar = plt.subplots(2, sharex=True)

axar[0].set_title("A Doktorandusz hízása")
axar[0].plot(days, grams.ravel(), color="blue")
axar[0].scatter(days, grams.ravel(), marker="o", color="red")

axar[1].set_title("d{A Doktorandusz hízása}/dx")
axar[1].plot(days[1:], dgrams / ddays, color="blue")
axar[1].scatter(days[1:], dgrams / ddays, marker="o", color="red")

plt.show()
