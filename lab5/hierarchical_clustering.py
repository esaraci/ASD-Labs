from cluster import Cluster
from closest_pair import *


def hierarchical_clustering(P, k):
    n = len(P)
    P.sort()
    print("P:", P)
    clusters = [Cluster([point]) for point in P]
    S = P.copy()
    S.sort(key=lambda x: x[1])
    print("Sorted S:", S)
    S_index = [P.index(t) for t in S]

    while len(clusters) > k:

        to_be_unified = fast_closest_pair(clusters, S_index)
        to_be_unified[0].union_cluster(to_be_unified[1])

        clusters.remove(to_be_unified[1])
        S_index.remove(P.index(to_be_unified[1]))
        #print("S index:", S_index)


    return clusters
