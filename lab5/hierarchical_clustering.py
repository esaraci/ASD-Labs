from cluster import Cluster
from closest_pair import *


def hierarchical_clustering(P, k):
    # creo i cluster da usare successivamente
    clusters = [((point[0], point[1]), Cluster([point])) for point in P]  # tuple (centroide, clusters)
    S = clusters[:]

    distortion_clusters = []
    while len(clusters) > k:

        if 5 < len(clusters) < 21:
            distortion_clusters.append([cluster[1] for cluster in clusters])

        clusters.sort(key=lambda x: (x[0])[0])
        S.sort(key=lambda x: (x[0])[1])

        to_be_unified = fast_closest_pair(clusters, S)

        new_elements = to_be_unified[1][1].get_elements() + to_be_unified[2][1].get_elements()
        new_cluster = Cluster(new_elements)

        clusters.remove(to_be_unified[2])
        clusters.remove(to_be_unified[1])
        clusters.append((new_cluster.get_centroid(), new_cluster))

        S = clusters[:]

    return [cluster[1] for cluster in clusters], distortion_clusters
