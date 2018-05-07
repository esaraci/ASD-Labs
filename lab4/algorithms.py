from enum import Enum
from PriorityQueue import PriorityQueue
from graph import *
import random
import numpy as np

# constants
INFINITY = float('inf')


class Color(Enum):
    WHITE = 0
    GREY = 1
    BLACK = 2


do_i_need_to_stop = False

# _sons_of returns the sons of node v in the tree T
# used by DFS
def _sons_of(T, v):
    return [x[0] for x in T if x[1] == v]


# Basic DFS algorithm
def DFS_Visited(T, u, visited, color):
    color[u] = Color.BLACK
    visited.append(u)
    for v in _sons_of(T, u):
        # don't need to check if u==v since u is set to black, and I check that v is white before proceeding
        if color[v] == Color.WHITE:
            visited = DFS_Visited(T, v, visited, color)

    return visited


# Get cycle cost, used by PRIM and Random Insertion
# Input: Graph, C:[node1, node2, node3]
# Output: cost of the CYCLE node1 --> node2 --> node3 --> node1
def _get_cycle_cost(G, C):
    adj_matrix = G.get_adj_matrix()
    cost = 0
    length_of_cycle = len(C)
    for i in range(length_of_cycle):
        j = i + 1
        if j == length_of_cycle:
            # if im out of bounds with j (=i+1)
            # i'm finished, i set j=0 and add to the total cost the cost of the last edge
            # v1 --> v2 --> v3 +[-->] v1
            j = 0
        cost += adj_matrix[C[i]][C[j]]

    return cost


# PRIM
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

        for v in range(G.get_len()):  # per ogni nodo nella lista delle adiacenze di u
            # se u è in Q e il valore del nodo è minore di quello della chiave corrente e non è un cappio (elemento
            # della diagonale)
            if Q.is_there_element(v) and adj_matrix[u[1]][v] < keys[v] and u != v:
                old_val = keys[v]  # salvo il vecchio valore (serve per decrease_key)
                keys[v] = adj_matrix[u[1]][v]  # aggiorno il nuovo valore
                parents[v] = u[1]  # modifico il genitore del nodo
                Q.decrease_key(v, old_val, keys[v])  # decrem valore nell'albero per poi estrarre il minimo al prox giro

    return get_prim_result(G, [(v, parents[v]) for v in range(G.get_len()) if v != r])


# PRIM returns a tree, performing DFS on int will give me a cycle
# after getting the cycle i can compute the cost of it using get_cycle_cost()
def get_prim_result(G, tree):
    color = {}
    for i in tree:
        color[i[0]] = Color.WHITE
    # creating cycle from tree
    C = DFS_Visited(tree, 0, [], color)

    return _get_cycle_cost(G, C)


# RANDOM INSERTION
def random_insertion(G):

    # BEGIN INITIALIZATION
    C = [0]  # putting 0 as the first node since we always start from 0
    adj_matrix = G.get_adj_matrix()
    not_extracted = set((np.arange(G.get_len())))
    not_extracted.remove(0)

    min_ = INFINITY
    node_idx = None
    for i, val in enumerate(adj_matrix[0, 1:]):
        if val < min_:
            min_ = val
            node_idx = i+1  # non primo nodo

    # adding the second node
    C.append(node_idx)
    not_extracted.remove(node_idx)

    # adding 3rd node, i do not need to perform any evaluation since i can attach it in only one way to C
    # C = existing cycle with 2 nodes added before
    extracted = random.sample(not_extracted, 1)[0]  # random.sample returns a list of length 1
    #C.append(extracted)
    C.insert(1,extracted)
    not_extracted.remove(extracted)
    # END INITIALIZATION

    # BEGIN SELECTION
    while not_extracted:
        extracted = random.sample(not_extracted, 1)[0]
        not_extracted.remove(extracted)

        min_ = INFINITY
        edges = None
        for i, node in enumerate(C):
            j = i + 1
            if j == len(C):
                # if i'm out of bounds with j (=i+1)
                # I put j=0 (<-- first node of the cycle)
                # "i" will the last node of the cycle
                j = 0

            # computing where (inside C) i need to insert "extracted" to minimize the increase of the cost
            if adj_matrix[C[i]][extracted] + adj_matrix[C[j]][extracted] - adj_matrix[C[i]][j] < min_:
                min_ = adj_matrix[C[i]][extracted] + adj_matrix[C[j]][extracted] - adj_matrix[C[i]][C[j]]
                edges = (i, j)

        # print("BEFORE", C)
        # print("NODO SCELTO", extracted)
        # print("FRA", C[edges[0]], C[edges[1]])
        if edges[1] == 0:
            # j == 0, so i need to insert this node as the last node of the cycle, linked with the 0 (= the first node)
            # BEFORE: 0 --> v_1 ... --> v_n (--> 0)
            # AFTER:  0 --> v_1 ... --> v_n --> "extracted" (--> 0)
            C.append(extracted)
        else:
            # i need to insert "extracted" where j was.
            # BEFORE: i --> j
            # AFTER:  i --> extracted --> j
            C.insert(edges[1],  extracted)
        #print(C)
        #print(C)

    return _get_cycle_cost(G, C)


