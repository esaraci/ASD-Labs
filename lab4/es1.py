import numpy as np
from graph import *
from PriorityQueue import PriorityQueue
import random
from enum import Enum

# global
PI = 3.141592
RRR = 6378.388
INFINITY = float('inf')
# x[0][lat][long]


class Color(Enum):
    WHITE = 0
    GREY = 1
    BLACK = 2


def sons_of(T, v):
    return [x[0] for x in T if x[1] == v]


def DFS_Visited(T, u, visited, color):
    color[u] = Color.BLACK
    visited.append(u)
    # adj_matrix = G.get_adj_matrix
    for v in sons_of(T, u):
        # non controllo con u diverso da v perchè discrimino usando il colore
        if color[v] == Color.WHITE:
            visited = DFS_Visited(T, v, visited, color)

    return visited


def prim(G, r=0):

    keys = {}
    parents = {}
    adj_matrix = G.get_adj_matrix()

    for i in range(G.get_len()):
        keys[i] = INFINITY
        parents[i] = None

    keys[r] = 0

    array = [[keys[v], v] for v in range(G.get_len())]
    Q = PriorityQueue(array)

    while not Q.is_empty():
        u = Q.extract_min()  # u = array di 2 valori [chiave, nodo]

        # print("MINIMO", u)

        # print("ADJ", adj_matrix[u[1]])

        for v in range(G.get_len()):  # per ogni nodo nella lista delle adiacenze di u
            # print("Confronto", adj_matrix[u[1]][v])
            # print("Valore corrente", keys[v])
            # se u è in Q e il valore del nodo è minore di quello della chiave corrente e non è un cappio (elemento
            # della diagonale)
            if Q.is_there_element(v) and adj_matrix[u[1]][v] < keys[v] and u != v:
                old_val = keys[v]  # salvo il vecchio valore (serve per decrease_key)
                keys[v] = adj_matrix[u[1]][v]  # aggiorno il nuovo valore
                parents[v] = u[1]  # modifico il genitore del nodo
                Q.decrease_key(v, old_val, keys[v])  # decrem valore nell'albero per poi estrarre il minimo al prox giro

    return [(v, parents[v]) for v in range(G.get_len()) if v != r]


def get_cycle_cost(G, C):
    adj_matrix = G.get_adj_matrix()
    cost = 0
    lungh = len(C)
    for i in range(lungh):
        j = i + 1
        if j == lungh:
            # se sono out of bound con j, torno a 0 e chiudo il ciclo
            j = 0
        cost += adj_matrix[C[i]][C[j]]

    return cost


def random_insertion(G):

    # BEGIN INITIALIZATION
    C = [0]
    adj_matrix = G.get_adj_matrix()
    not_extracted = set((np.arange(G.get_len())))
    not_extracted.remove(0)

    min_ = INFINITY
    node_idx = None
    for i, val in enumerate(adj_matrix[0, 1:]):
        if val < min_:
            min_ = val
            node_idx = i

    C.append(node_idx)
    not_extracted.remove(node_idx)

    # Estraggo terzo nodo a caso, esistono solo 2 possibili archi che lo integrano nel circuito
    extracted = random.sample(not_extracted, 1)[0]  # random.sample ritorna una lista, prendo il primo ed unico elemento
    C.append(extracted)
    not_extracted.remove(extracted)

    # END INITIALIZATION

    # BEGIN SELECTION
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

    return get_cycle_cost(G, C)


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
        min_dist = INFINITY
        min_prec = None
        S1 = tuple([u for u in S if u != v])
        for u in S1:
            dist = held_karp(graph, u, S1)  # chiamata ricorsiva
            # print("Dist:", dist)
            # print("Arco attuale:", graph.get_adj_matrix(u, v))
            # print("Confronto:", dist + graph.get_adj_matrix(u, v), mindist)
            if dist + graph.get_adj_matrix(u, v) < min_dist:  # aggiorno nel caso sia una quantità minore
                min_dist = dist + graph.get_adj_matrix(u, v)
                min_prec = u
        graph.set_distances((v, S), min_dist)
        graph.set_parents((v, S), min_prec)
        return min_dist


if __name__ == "__main__":
    # print("min(len(lul))")

    geo = False
    c = 1
    fname = "datasets/burma14.tsp"
    with open(fname) as f:
        line = f.readline()
        while line != "NODE_COORD_SECTION\n":

            if "EDGE_WEIGHT_TYPE" in line:
                if line.split(":")[1] == " GEO\n":
                    geo = True

            line = f.readline()
            c += 1

    dataset = np.loadtxt(fname, skiprows=c, comments=["EOF"])

    l = len(dataset)
    lul = tuple(np.arange(l))

    graph = Graph(dataset, geo)

    T = prim(graph)
    color = {}
    for i in T:
        color[i[0]] = Color.WHITE
    D = DFS_Visited(T, 0, [], color)

    print("PRIM:", get_cycle_cost(graph, D))
    print("HELD_KARP:", held_karp(graph, 0, lul))
    print("RANDOM:", random_insertion(graph))


