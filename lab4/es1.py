import numpy as np
from graph import *
import random

# global
PI = 3.141592
RRR = 6378.388
INFINITY = float('inf')
# x[0][lat][long]


def random_insertion(G):

    # INITIALIZATION
    C = [0]
    adj_matrix = G.get_adj_matrix()
    not_extracted = set((np.arange(len(adj_matrix))))
    not_extracted.remove(0)

    min_ = INFINITY
    node_idx = None
    for i, val in enumerate(adj_matrix[0, 1:]):
        if val < min_:
            min_ = val
            node_idx = i

    C.append(node_idx)
    not_extracted.remove(node_idx)

    #  Estraggo terzo nodo a caso, esistono solo 2 possibili archi che lo integrano nel circuito
    extracted = random.sample(not_extracted, 1)[0]  # random.sample ritorna una lista, prendo il primo ed unico elemento
    C.append(extracted)
    print(type(int(extracted)))
    not_extracted.remove(extracted)

    # END INITIALIZATION

    while len(not_extracted) is not 0:
        extracted = random.sample(not_extracted, 1)[0]
        not_extracted.remove(extracted)

        min_ = INFINITY
        edges = None
        for i, node in enumerate(C):
            j = i + 1
            if j == len(C):
                # se sono out of bound con j, torno a 0 e chiudo il ciclo
                j = 0

            if adj_matrix[j][extracted] + adj_matrix[i][extracted] - adj_matrix[i][j] < min_:
                min_ = adj_matrix[j][extracted] + adj_matrix[i][extracted] - adj_matrix[i][j]
                edges = (i, j)

        # collego l'ultimo nodo al primo
        if edges[1] == 0:
            C.append(extracted)
        else:
            C.insert(edges[1],  extracted)


def held_karp(graph, v, S):
    """

    :param graph: Graph
    :param v: target node
    :param S: nodi poer cui dobbiamo passare
    :return:
    """
    # Caso base
    if len(S) == 1:
        # print("Caso base:", v)
        return graph.get_adj_matrix(v, 0)  # S contiene un unico elemento che è v, stiamo andando da 0 --> v
    elif graph.get_distances((v, S)) is not None:
        return graph.get_distances((v, S))
    else:
        mindist = INFINITY
        minprec = None
        S1 = tuple([u for u in S if u != v])
        for u in S1:
            dist = held_karp(graph, u, S1)  # chiamata ricorsiva
            # print("Dist:", dist)
            # print("Arco attuale:", graph.get_adj_matrix(u, v))
            # print("Confronto:", dist + graph.get_adj_matrix(u, v), mindist)
            if dist + graph.get_adj_matrix(u, v) < mindist:  # aggiorno nel caso sia una quantità minore
                mindist = dist + graph.get_adj_matrix(u, v)
                minprec = u
        graph.set_distances((v, S), mindist)
        graph.set_parents((v, S), minprec)
        return mindist


if __name__ == "__main__":
    # print("min(len(lul))")

    dataset = np.loadtxt("datasets/burma14.tsp", skiprows=8, comments="EOF")
    l = len(dataset)
    lul = tuple(np.arange(l))
    # create_adj_matrix(n)
    # adj_matrix = create_adj_matrix(dataset)

    graph = Graph(dataset)
    # print("Matrice: \n", graph.get_adj_matrix())
    held_karp(graph, 0, lul)
    random_insertion(graph)
