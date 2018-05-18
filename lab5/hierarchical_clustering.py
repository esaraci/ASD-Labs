from cluster import Cluster
from scipy.spatial import distance

INFINITY = float('inf')


def euclidean_distance(p1, p2):
    return distance.euclidean(p1, p2)


def min_distance(clusters):
    min_d = INFINITY
    min_c = None

    for u, c1 in enumerate(clusters):
        for v, c2 in enumerate(clusters):
            if v > u:
                d = euclidean_distance(c1.get_centroid(), c2.get_centroid())
                if d < min_d:
                    min_d = d
                    min_c = (c1, c2)
    return min_c
    # TODO: eugen il metodo ritorna una tupla di cluster da unire


def hierarchical_clustering(P, k):
    n = len(P)

    clusters = []
    for point in P:
        cluster = Cluster([point])
        clusters.append(cluster)
    while len(clusters) > k:

        to_be_unified = min_distance(clusters)
        to_be_unified[0].union_cluster(to_be_unified[1])

        clusters.remove(to_be_unified[1])

    return clusters
