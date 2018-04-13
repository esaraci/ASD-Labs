import numpy as np
from math import cos, sin, acos


# global
PI = 3.141592
RRR = 6378.388
INFINITY = float('inf')
# x[0][lat][long]


def held_karp(adj_matrix, v, S):
    """

    :param adj_matrix: weights
    :param v: target node
    :param S: nodi poer cui dobbiamo passare
    :return:
    """
    distances = {}
    parents = {}


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
    q3 = cos(lat_i + lat_j);
    dij = int(RRR * acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)

    return dij


def create_adj_matrix(dataset): # format, passare il formato geo o euc
    n = len(dataset)
    matrix = np.zeros((n, n), dtype=int)
    for i in dataset:
        for j in dataset:
            if i[0] != j[0]:
                matrix[int(i[0])-1][int(j[0])-1] = compute_distance(i, j)  # None if i == j
    return matrix


if __name__ == "__main__":
    # print("min(len(lul))")

    dataset = np.loadtxt("datasets/burma14.tsp", skiprows=8, comments="EOF")
    # create_adj_matrix(n)
    adj_matrix = create_adj_matrix(dataset)
    held_karp(adj_matrix)