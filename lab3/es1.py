# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from algorithms import ccrp

# CONSTS
INFINITY = float('inf')

# Useful dictionaries for converting road_type to speed limits and capacities
SPEED_LIMIT = {-1: INFINITY, 1: 30, 2: 50, 3: 50, 4: 70, 5: 70, 6: 90}
CAPACITY = {-1: INFINITY, 1: 500, 2: 750, 3: 1000, 4: 1500, 5: 2000, 6: 4000}

# sources and destinations of the evacuation plan
sources = [3718987342, 915248218, 65286004]
destinations = [261510687, 3522821903, 65319958, 65325408, 65295403, 258913493]


def create_adj_list(V, tails, heads, length, road_type):
    """Returns
    :param V: list of all the nodes
    :param tails: list all  the nodes having out-degree > 0
    :param heads: list of all the nodes having in-degree > 0
    :param length: length of the edges between the nodes
    :param road_type: type of the road
    :return:
    """
    adj_list = {}
    for v in V:
        adj_list[v] = {}

    for i, t in enumerate(tails):
        h = heads[i]
        if t != h:  # evito cappi
            if h not in adj_list[t].keys():  # evito archi paralleli
                adj_list[t][h] = [length[i], road_type[i]]

    return adj_list


if __name__ == '__main__':
    # Loading file
    data = np.loadtxt("./SFroad.txt")

    # Setting starting variables
    tails = [int(i) for i in data[:, 0]]
    heads = [int(i) for i in data[:, 1]]
    length = data[:, 2]
    road_type = [int(i) for i in data[:, 3]]

    x = set(tails)
    y = set(heads)
    z = x.union(y)
    n = len(z)

    # creazione lista delle adiacenze
    adj_list = create_adj_list(z, tails, heads, length, road_type)

    max_capacity = []
    for s in sources:
        capacity = 0
        for u in adj_list[s]:
            capacity += CAPACITY[adj_list[s][u][1]]
        max_capacity.append(capacity)

    print("Capacità max di veicoli che possono entrare in città:", sum(max_capacity))

    max_capacity_destinations = []
    for d in destinations:
        capacity = 0
        for u in adj_list:
            for v in adj_list[u]:
                if v == d:
                    capacity += CAPACITY[adj_list[u][v][1]]
        max_capacity_destinations.append(capacity)

    print("Capacità max di veicoli che possono arrivare contemporamente agli ospedali:", sum(max_capacity_destinations))

    # Processing
    plan, flows, costs = ccrp(z, adj_list, sources, destinations)

    print("Capacità max di veicoli del piano trovato:", flows[-1])

    x_range = np.arange(1, len(plan) + 1)

    # creiamo il primo plot
    plt.plot(x_range, flows, label="Capacità")
    plt.xlabel("Numero di cammini")
    plt.ylabel("Capacità")
    plt.title("CCRP - Capacità massima", y=1.08)
    plt.xticks(np.arange(min(x_range), max(x_range) + 1, 1))
    plt.grid()

    plt.savefig("lab3-grafico-Capacita.png")

    plt.clf()  # pulisco il plot

    # creiamo il secondo plot
    plt.plot(x_range, costs, label="Tempo (s)", color='orange')
    plt.xlabel("Numero di cammini")
    plt.ylabel("Tempo (s)")
    plt.title("CCRP - Tempo impiegato", y=1.08)
    plt.xticks(np.arange(min(x_range), max(x_range) + 1, 1))
    plt.yticks(np.arange(100, 800, 100))
    plt.grid()

    plt.savefig("lab3-grafico-Tempo.png")
