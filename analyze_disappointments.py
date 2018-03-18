"""
Analyze disappointment rates in order to find good thresholds for votes.
"""

# STD
import codecs
import sys
from collections import defaultdict

# EXT
import matplotlib.pyplot as plt
import numpy as np


def read_in_data(inpath):
    data = defaultdict(int)

    with codecs.open(inpath, "rb", "utf-8") as infile:
        for line in infile:
            line = float(line.strip())
            data[line] += 1

    return data


if __name__ == "__main__":
    inpath = sys.argv[1]
    data = read_in_data(inpath)
    measurements = np.array(list(data.values()))

    x = np.arange(0, round(max(data.keys())) + 1, 1)
    y = [0] * len(x)

    for key, value in data.items():
        if key == 0:
            continue
        y[int(round(key))] += value

    mu = np.mean(np.array(measurements))
    sigma = np.std(np.array(measurements))
    best_fit = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
         np.exp(-0.5 * (1 / sigma * (x - mu)) ** 2))

    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.plot(x, best_fit, '--')
    print(mu)
    print(sigma)
    plt.show()

# Fitting with wolfram-alpha
# sigmas
# quadratic fit {45, 10.72} {25, 13.76} {10, 15.07} {5, 22.921} {15, 16.095} {30, 9.74} {35, 8.518}
# 0.0110448 x^2 - 0.829527 x + 25.2988

# mus
# linear fit {45, 2.08} {25, 2.47} {10, 2.69} {5, 4.327} {15, 2.86076} {30, 1.96} {35, 1.7936}
# 0.00219177 x^2 - 0.155699 x + 4.66269