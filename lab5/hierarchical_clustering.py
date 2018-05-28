from cluster import Cluster
from closest_pair import *


def hierarchical_clustering(P, k):
    n = len(P)
    # ordino i valori
    P.sort()
    temp = P.copy()
    temp.sort(key=lambda x: x[1])

    # creo i cluster da usare successivamente
    clusters = [Cluster([point]) for point in P]
    S = [Cluster([point]) for point in temp]

    while len(clusters) > k:

        to_be_unified = fast_closest_pair(clusters, S)

        # print("to be unified", to_be_unified)
        to_be_unified[1].union_cluster(to_be_unified[2])

        # print("clusters", clusters)
        # print("S:", S)

        clusters.remove(to_be_unified[2])
        S.remove(to_be_unified[2])

        # print("clusters_update", clusters)
        # print("S_update:", S)

    return clusters
