from cluster import Cluster
from scipy.spatial import distance


INFINITY = float('inf')


def euclidean_distance(p1, p2):
    return distance.euclidean(p1, p2)


def kmeans(P, k, pop, q=1):
    """

    :param P: points, (x, y)
    :param k: number of clusters
    :param q: iterations
    :param pop: population of the cities, need for choosing the centers of the k clusters
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
        clusters = [Cluster([], i) for i in range(k)]
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

        # print("##### ITERATION {} #####".format(i))
        # print("CENTERS:", centers)
        # lens = [len(clusters[i].get_elements()) for i in range(k)]
        # print("CARDINALITY:", lens)
        # print("SUM: {}/{}".format(sum(lens), n))

    return clusters
