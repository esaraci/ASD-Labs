# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import heapq

INFINITY = float('inf')  # infinito secondo python
SPEED_LIMIT = {-1: INFINITY, 1: 30, 2: 50, 3: 50, 4: 70, 5: 70, 6: 90}
CAPACITY = {-1: INFINITY, 1: 500, 2: 750, 3: 1000, 4: 1500, 5: 2000, 6: 4000}

sources = [3718987342, 915248218, 65286004]  # insieme delle sorgenti
destinations = [261510687, 3522821903, 65319958, 65325408, 65295403, 258913493]  # insieme delle destinazioni


# costo sono i secondi tempo di percorrenza
# si parte da sorgente per forza perchè ha costo 0 e ordino per costo minimo
# tempo di percorrenza: int((km / (km/h)) * 3600)


class PriorityQueue:
    def __init__(self, heap):
        self.heap = heap
        heapq.heapify(self.heap)

    def get_heap(self):
        return self.heap

    def extract_min(self):
        return heapq.heappop(self.heap)

    def parent(self, i):
        return int((i - 1) / 2)

    def is_empty(self):
        return len(self.heap) == 0

    def bubble_up(self, i):
        p = self.parent(i)
        while i > 0 and self.heap[i] < self.heap[p]:
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]  # scambio valori fra parent e figlio
            i = p
            p = self.parent(i)

    def decrease_key(self, node, old_val, new_val):
        i = self.heap.index([old_val, node]) # ricavo l'indice dal vecchio valore per aggiornarlo successivamente
        if self.heap[i][0] < new_val:  # controllo concettuale
            return False

        self.heap[i][0] = new_val
        self.bubble_up(i)
        return True


def dijkstra(V, adj_list):
    # INIT SSSP
    parents = {} # padri dei nodi
    dict_distances = {} # dizionario delle distanze
    weights = {} # costo dell arco fra i due nodi

    for s in sources:
        weights[(0, s)] = 0

    for v in V:
        dict_distances[v] = INFINITY
        parents[v] = None

    dict_distances[0] = 0
    # END INIT SSSP

    # poplamento pesi degli archi
    for v in V:
        for u in adj_list[v].keys():
            edge = adj_list[v][u]  # edge[0] = length, edge[1] road_type
            weights[(v, u)] = edge[0] / 1000 / SPEED_LIMIT[edge[1]] * 3600 # aggiungo peso dell'arco in secondi

    Q = PriorityQueue([[cost, node] for node, cost in dict_distances.items()]) # creo la coda in base a dict_distances
    # utilizziamo un array anziché una tupla perché queste ultime sono immutabili e non sarebbero aggiornabili con
    # decrease key

    while not Q.is_empty():
        u = Q.extract_min()  # u = (distance, u) distanza per arrivare al nodo u
        print("ExtractMin", u)
        for v in adj_list[u[1]]:  # dict_distances = costo/distanza per arrivare a v
            # print(weights[(u[1], v)])
            if dict_distances[u[1]] + weights[(u[1], v)] < dict_distances[v]:
                # BEGIN RELAX
                old_val = dict_distances[v]
                dict_distances[v] = dict_distances[u[1]] + weights[(u[1], v)]
                parents[v] = u[1]
                # END RELAX
                Q.decrease_key(v, old_val, dict_distances[v])

    # print("From Dijkstra:", Q)
    return Q


def ccrp(V, adj_list, sources, destinations):
    # aggiungo super sorgente con costo 0 e capacità infinity
    adj_list[0] = {}
    for s in sources:
        adj_list[0][s] = (0, -1)  # -1 = road_type di super
        # sorgente ovvero infinito

    print("ADJ_0", adj_list[0])
    return dijkstra(V, adj_list)


def create_adj_list(V, tails, heads, length, road_type):
    adj_list = {}
    for v in V:
        adj_list[v] = {}

    for i, t in enumerate(tails):
        h = heads[i]
        if t != h:  # evita cappi
            if h not in adj_list[t].keys():  # sono apposto devo aggiungere il nodo
                adj_list[t][h] = (length[i], road_type[i])

    return adj_list


if __name__ == '__main__':
    data = np.loadtxt("./SFroad.txt")

    tails = [int(i) for i in data[:, 0]]
    heads = [int(i) for i in data[:, 1]]
    length = data[:, 2]
    road_type = [int(i) for i in data[:, 3]]

    x = set(tails)
    y = set(heads)
    z = x.union(y)
    n = len(z)

    adj_list = create_adj_list(z, tails, heads, length, road_type)
    lul = ccrp(z, adj_list, sources, destinations)
    print(lul)