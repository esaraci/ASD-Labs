from cluster import Cluster
from closest_pair import *


def hierarchical_clustering(P, k):
    n = len(P)
    # ordino i valori
    # P.sort()
    # temp = P.copy()
    # temp.sort(key=lambda x: x[1])

    # creo i cluster da usare successivamente
    clusters = [((point[0], point[1]), Cluster([point])) for point in P]  # tuple (centroide, clusters)
    # print(clusters)
    S = clusters[:]

    while len(clusters) > k:

        clusters.sort(key=lambda x: (x[0])[0])

        S.sort(key=lambda x: (x[0])[1])

        to_be_unified = fast_closest_pair(clusters, S)

        # print("to be unified", to_be_unified)
        # print("cluster prende elementi", len((to_be_unified[1])[1].get_elements()))
        # clusters[clusters.index(to_be_unified[1])].union_cluster(to_be_unified[2])

        new_elements = to_be_unified[1][1].get_elements() + to_be_unified[2][1].get_elements()
        new_cluster = Cluster(new_elements)

        # print("cluster da unire", len(to_be_unified[2].get_elements()))
        # print("cluster unito", len(to_be_unified[1].get_elements()))
        # print("cluster nell'array", len(clusters[clusters.index(to_be_unified[1])].get_elements()))

        # print("clusters", clusters)
        # print("S:", S)

        clusters.remove(to_be_unified[2])
        clusters.remove(to_be_unified[1])
        # S.remove(to_be_unified[2])
        # S.remove(to_be_unified[1])

        clusters.append((new_cluster.get_centroid(), new_cluster))
        # S.append((new_cluster.get_centroid(), new_cluster))

        S = clusters[:]

        # print("clusters_update", clusters)
        # print("S_update:", S)

        # print("lunghezza P e S", len(clusters), len(S))

        # print("lunghezza clusters", sum([len(cluster[1].get_elements()) for cluster in clusters]))

    return [cluster[1] for cluster in clusters]
