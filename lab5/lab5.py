import numpy as np
from hierarchical_clustering import *

if __name__ == '__main__':
    f_name = "unifiedCancerData/unifiedCancerData_111.csv"
    dataset = np.loadtxt(f_name, dtype=float, delimiter=',')

    n = len(dataset)

    x = dataset[:, 1]  # coordinate x
    y = dataset[:, 2]  # coordinate y

    coordinates = [(x[i], y[i]) for i in range(n)]

    print(hierarchical_clustering(coordinates, 15))

