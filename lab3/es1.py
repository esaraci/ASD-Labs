import numpy as np
import matplotlib.pyplot as plt
from heapq import heappop, heappush


INFINITY = float('inf')  # infinito secondo python
SPEED_LIMIT = {-1: INFINITY, 1: 30, 2: 50, 3: 50, 4: 70, 5: 70, 6: 90}
CAPACITY = {-1: INFINITY, 1: 500, 2: 750, 3: 1000, 4: 1500, 5: 2000, 6: 4000}

sources = [3718987342, 915248218, 65286004]  # insieme delle sorgenti
destinations = [261510687, 3522821903, 65319958, 65325408, 65295403, 258913493]  # insieme delle destinazioni

# costo sono i secondi tempo di percorrenza
# si parte da sorgente per forza perchè ha costo 0 e ordino per costo minimo
# tempo di percorrenza: int((km / (km/h)) * 3600)


def dijkstra(V, adj_list):
    parents = {}
    costs = {}

    for v in V:
        costs[v] = INFINITY

    costs[0] = 0  # distanza dal nodo supersorgente a se stesso = 0


    Q = []
    for v in V:
        for u in adj_list[v].keys():
            edge = adj_list[v][u]  # edge[0] = length, edge[1] road_type
            Q.append(((u, v), edge[0]/1000 / SPEED_LIMIT[edge[1]] * 3600))

    print(Q)


def ccrp(V, adj_list, sources, destinations):
    # aggiungo super sorgente con costo 0 e capacità infinity
    adj_list[0] = {}
    for s in sources:
        adj_list[0][s] = (0, -1)  # -1 = road_type di supersorgente ovvero infinito


def create_adj_list(V, tails, heads, length, road_type):
    adj_list = {}
    for v in V:
        adj_list[v] = {}

    for i, t in enumerate(tails):
        h = heads[i]
        if t != h:  # evita eugen
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

    dijkstra(z, adj_list)