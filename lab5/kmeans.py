from cluster import Cluster
from math import sqrt


INFINITY = float('inf')


def euclidean_distance(p1, p2):
    return sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def kmeans(P, k, pop, q=1):
    """
    :param P: points, (x, y)
    :param k: number of clusters
    :param pop: population of the cities, need for choosing the centers of the k clusters
    :param q: iterations
    :return:
    """

    n = len(P)

    # Ordering by population and creating k centers
    l = [(P[i], pop[i]) for i in range(n)]
    l.sort(key=lambda x: x[1], reverse=True)
    centers = [l[i][0] for i in range(k)]

    clusters = []
    for i in range(q):
        # for each iteration
        clusters = [Cluster([]) for _ in range(k)]
        for j in range(n):
            # for each point
            min_dist = INFINITY
            min_c = None
            for c in range(k):
                # searching for closest center to current point
                dist = euclidean_distance(centers[c], P[j])
                if dist < min_dist:
                    min_dist = dist
                    min_c = c

            clusters[min_c].add_element(P[j])

        # recomputing centroids for next iteration
        for idx in range(k):
            if clusters[idx].get_centroid() is not None:
                centers[idx] = clusters[idx].get_centroid()

    return clusters
