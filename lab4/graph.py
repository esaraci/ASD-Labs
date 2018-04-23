# una bella classe per eugen da spostare in un file a parte
import numpy as np
from math import cos, acos


# global
PI = 3.141592
RRR = 6378.388
INFINITY = float('inf')
# x[0][lat][long]


class Graph:
    def __init__(self, dataset):
        self.n = len(dataset)  # inizializzo già qua la matrice delle adiacenze
        self.adj_matrix = np.zeros((self.n, self.n), dtype=int)
        self.create_adj_matrix(dataset)
        self.distances = {}  # chiave del dizionario tupla (v, S)
        self.parents = {}

    def create_adj_matrix(self, dataset):  # format, passare il formato geo o euc
        for i in dataset:
            for j in dataset:
                if i[0] != j[0]:
                    self.adj_matrix[int(i[0])-1][int(j[0])-1] = compute_distance(i, j)  # None if i == j

    # la chiave è una tupla
    def get_distances(self, key):
        try:
            return self.distances[key]
        except KeyError as e:
            return None

    def set_distances(self, key, value):
        self.distances[key] = value

    # anche per i parents la chiave è una tupla
    def get_parents(self, key):
        return self.parents[key]

    def set_parents(self, key, value):
        self.parents[key] = value

    def get_adj_matrix(self, u=None, v=None):
        if u is None or v is None:
            return self.adj_matrix
        else:
            return self.adj_matrix[u, v]

    def get_len(self):
        return self.n


def convert_to_rads(val):
    deg = int(val)
    min_ = val - deg
    rad = PI * (deg + 5.0 * min_/ 3.0) / 180.0

    return rad


def compute_distance(i, j):
    if i[0] == j[0]:
        return -1

    lat_i = convert_to_rads(i[1]) # u[1] = latitudine del nodo u ==> riga u
    long_i = convert_to_rads(i[2])

    lat_j = convert_to_rads(j[1])
    long_j = convert_to_rads(j[2])

    q1 = cos(long_i - long_j)
    q2 = cos(lat_i - lat_j)
    q3 = cos(lat_i + lat_j)
    dij = int(RRR * acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)

    return dij


if __name__ == '__main__':
    print("you should not be executing me")