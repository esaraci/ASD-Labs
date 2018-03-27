import numpy as np
import matplotlib.pyplot as plt
from heapq import heappop, heappush

sources = [3718987342, 915248218, 65286004]
destinations = [261510687, 3522821903, 65319958, 65325408, 65295403, 258913493]


if __name__ == '__main__':
    data = np.loadtxt("./SFroad.txt")
    tail = data[:, 0]
    head = data[:, 1]
    meters = data[:, 2]
    road_type = data[:, 3]
    x = set(tail)
    y = set(head)
    z = x.union(y)
    n = len(z)
    print(n)
