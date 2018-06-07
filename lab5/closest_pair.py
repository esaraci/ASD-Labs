from math import floor, sqrt
import copy

INFINITY = float('inf')


def euclidean_distance(p1, p2):
    return sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    # return distance.euclidean(p1, p2)


def closest_pair_strip(S, mid, d):
    n = len(S)
    # S1 = []
    # for i in range(n):
    #     centroid = S[i][0]  # == (S[i])[0] ==> get_centroid()
    #     # if euclidean_distance(centroid, mid) < d:
    #     if abs(mid - centroid[0]) < d:
    #         S1.append(S[i])

    S1 = [S[i] for i in range(n) if abs(mid - S[i][0][0]) < d]  # <== è più lento

    d, i, j = INFINITY, -1, -1

    k = len(S1)

    for u in range(k - 1):
        for v in range(u + 1, min(u + 3, k - 1) + 1):
            # (d, i, j) = min((d, i, j), (euclidean_distance((S1[u])[1].get_centroid(), (S1[v])[1].get_centroid()), S1[u], S1[v]))
            d, i, j = min((d, i, j), (euclidean_distance((S1[u])[0], (S1[v])[0]), S1[u], S1[v]))
    return d, i, j


def slow_closest_pair(clusters):
    min_d = INFINITY
    min_c = None

    for u, c1 in enumerate(clusters):
        for v, c2 in enumerate(clusters):
            if v > u:
                # d = euclidean_distance(c1[1].get_centroid(), c2[1].get_centroid())
                d = euclidean_distance(c1[0], c2[0])
                if d < min_d:
                    min_d = d
                    min_c = (c1, c2)
    return min_d, min_c[0], min_c[1]
    # TODO: eugen il metodo ritorna una tupla di cluster da unire


def split(S, pl, pr):
    # n = len(S)
    # sl = []
    # sr = []
    sl = pl[:]
    sr = pr[:]

    sl.sort(key=lambda x: x[0][1])
    sr.sort(key=lambda x: x[0][1])
    # for i in range(n):
    #     if S[i] in pl:
    #         sl.append(S[i])
    #     else:
    #         sr.append(S[i])
    return sl, sr


def fast_closest_pair(P, S):
    # print(S)
    n = len(P)
    if n <= 3:
        return slow_closest_pair(P)
    else:
        m = floor(n / 2)
        pl = P[0:m]
        pr = P[m:]

        sl, sr = split(S, pl, pr)

        (d, c1, c2) = min(fast_closest_pair(pl, sl), fast_closest_pair(pr, sr))

        x1 = (P[m - 1])[0][0]  # prendo la x del centroide
        x2 = (P[m])[0][0]  # prendo la x del centroide
        mid = (x1 + x2)/2

        return min((d, c1, c2), closest_pair_strip(S, mid, d))
