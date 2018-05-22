import math
from scipy.spatial import distance

INFINITY = float('inf')


def euclidean_distance(p1, p2):
    return distance.euclidean(p1, p2)


def closest_pair_strip(S, mid, d, P):
    n = len(S)
    S1 = []
    for i in range(n):
        print("P:",P)
        print("S:",S)
        centroid = P[S[i]].get_centroid()
        if euclidean_distance(centroid[0] - mid[0], centroid[1] - mid[1]) < d:
            S1.append(S[i])

    (d, i, j) = (INFINITY, -1, -1)

    k = len(S1)-1

    for u in range(k-2):
        for v in range(u, min(u+3, n-1)+1):
            (d, i, j) = min((d, i, j), (euclidean_distance(S1[u], S1[v]), S1[u], S1[v]))

    return d, i, j


def slow_closest_pair(clusters):
    min_d = INFINITY
    min_c = None

    for u, c1 in enumerate(clusters):
        for v, c2 in enumerate(clusters):
            if v > u:
                d = euclidean_distance(c1.get_centroid(), c2.get_centroid())
                if d < min_d:
                    min_d = d
                    min_c = (c1, c2)
    return min_d, min_c[0], min_c[1]
    # TODO: eugen il metodo ritorna una tupla di cluster da unire


def split(S, pl, pr, P):
    n = len(S)
    sl = []
    sr = []
    print('s:', S)
    print('P:', P)
    # print('pl:', pl)

    for i in range(n):
        if P[S[i]] in pl:
            sl.append(pl.index(P[S[i]]))
        else:
            sr.append(pr.index(P[S[i]]))
    return sl, sr


def fast_closest_pair(P, S):
    print(S)
    n = len(P)
    if n <= 3:
        return slow_closest_pair(P)
    else:
        m = math.floor(n/2)
        pl = []
        pr = []
        for i, point in enumerate(P):
            if i < m:
                pl.append(point)
            else:
                pr.append(point)
        sl, sr = split(S, pl, pr, P)
        (d, i, j) = min(fast_closest_pair(pl, sl), fast_closest_pair(pr, sr))
        m = (P[m-1]+P[m])
        mid = (m[0]/2, m[1]/2)
        return min((d, i, j), closest_pair_strip(S, mid, d, P))
