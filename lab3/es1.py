# coding=utf-8
import numpy as np

import heapq

# CONSTS
INFINITY = float('inf')

# Useful dictionaries for converting road_type to speed limits and capacities
SPEED_LIMIT = {-1: INFINITY, 1: 30, 2: 50, 3: 50, 4: 70, 5: 70, 6: 90}
CAPACITY = {-1: INFINITY, 1: 500, 2: 750, 3: 1000, 4: 1500, 5: 2000, 6: 4000}

# sources and destinations of the evacuation plan
sources = [3718987342, 915248218, 65286004]
destinations = [261510687, 3522821903, 65319958, 65325408, 65295403, 258913493]


# adapting heapq to our problem
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
        """Takes the node with index i and puts it in the correct position to restore the heap state.
        :param i: index of the node to bubble up
        :return: None
        """
        p = self.parent(i)
        while i > 0 and self.heap[i] < self.heap[p]:
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
            i = p
            p = self.parent(i)

    def decrease_key(self, node, old_val, new_val):
        """Updates the distance of the node (old_val) with the new computed distance (new_val), only if the latter
        is greater than the first.

        :param node: identifier of the node, it's not its index
        :param old_val: used as heap.index([old_val, node]) just to find the index of the node that needs the update
        :param new_val: value that will be assigned to the target node - only if new_val > old_val
        :return:
        """
        i = self.heap.index([old_val, node])
        if self.heap[i][0] < new_val:
            return False

        self.heap[i][0] = new_val
        self.bubble_up(i)
        return True


def path_cost(path, weights):
    """Returns the cost, in seconds, of the path.

    :param path: path to evaluate, ordered list of nodes. In our case from super-source to a destination
    :param weights: dictionary containing the costs of each edge, keys as tuples of nodes e.g. (u, v)
    :return: cost of the path, in seconds
    """
    cost = 0
    for i, u in enumerate(path):
        if i + 1 < len(path):  # bound checking
            v = path[i + 1]  # arriving end ot the node, (u --> v)
            cost += weights[(u, v)]

    return cost


def get_path_with_min_cost(plan, weights):
    """Returns the destination wich has the path (in plan) with min cost from the super-source
    :param plan: dictionary of the min paths from the super-source 0 to all the destinations. {destination: path[]}
    :param weights: dictionary containing the costs of each edge, keys as tuples of nodes e.g. (u, v)
    :return: the destination (which is the key of the dictionary) of the path with min cost
    """

    min_path = None  # destination with currently min path
    current_min_cost = INFINITY  # cost of the current min path
    for key in plan:
        cost = 0
        path = plan[key]
        for i, u in enumerate(path):
            if i + 1 < len(path):  # bound checking
                v = path[i + 1]  # arriving end ot the node, (u --> v)
                cost += weights[(u, v)]

        if cost < current_min_cost and cost != 0:
            current_min_cost = cost
            min_path = key

    # min_path = destination which has the min path from the super-source. It's not a path!
    # can be used as a key for plan.
    # current_min_cost holds the cost of the path plan[min_path]
    # if min_path is not None:
        # print(min_path, plan[min_path])
        # print(current_min_cost)
    return min_path


def get_flow(plan, dest, capacity):
    # [dest, [cammino ...]]
    # (adj_list[u][v])[1] = road_type

    # DOBBIAMO SCORRERE SOLO IL MINORE DEI CAMMINI
    min_flow = INFINITY
    for i, v in enumerate(plan[dest]):
        if v != dest:  # bound checking
            next = plan[dest][i + 1]
            if capacity[v][next] < min_flow:  # converto capacity, assumo sia ordinata
                min_flow = capacity[v][next]  # aggiorno min

    return min_flow


def find_paths(parents):
    """Finds a path from the super-source to each one of the destinations and returns them.
    Each path will be a min path for a destination because of the updates on parents performed by Dijkstra

    :param parents: dictionary --> {node: parent}
    :return: a dictionary with min paths for each destination {destination: path[]}
    """
    dict_paths = {}
    for dest in destinations:
        path = [dest]
        u = dest
        while parents[u] is not None:
            path.insert(0, parents[u])
            u = parents[u]
        dict_paths[dest] = path

    return dict_paths


def dijkstra(V, adj_list):
    # INIT SSSP
    parents = {}  # padri dei nodi
    dict_distances = {}  # dizionario delle distanze
    weights = {}  # costo dell arco fra i due nodi

    for s in sources:
        weights[(0, s)] = 0

    for v in V:
        dict_distances[v] = INFINITY
        parents[v] = None

    parents[0] = None  # parent della super source
    dict_distances[0] = 0
    # END INIT SSSP

    # poplamento pesi degli archi
    for v in V:
        for u in adj_list[v].keys():
            edge = adj_list[v][u]  # edge[0] = length, edge[1] road_type
            weights[(v, u)] = edge[0] / 1000 / SPEED_LIMIT[edge[1]] * 3600  # aggiungo peso dell'arco in secondi

    Q = PriorityQueue([[cost, node] for node, cost in dict_distances.items()])  # creo la coda in base a dict_distances
    # utilizziamo un array anziché una tupla perché queste ultime sono immutabili e non sarebbero aggiornabili con
    # decrease key

    while not Q.is_empty():
        u = Q.extract_min()  # u = (distance, u) distanza per arrivare al nodo u
        for v in adj_list[u[1]]:  # dict_distances = costo/distanza per arrivare a v
            if dict_distances[u[1]] + weights[(u[1], v)] < dict_distances[v]:
                # BEGIN RELAX
                old_val = dict_distances[v]
                dict_distances[v] = dict_distances[u[1]] + weights[(u[1], v)]
                parents[v] = u[1]
                # END RELAX
                Q.decrease_key(v, old_val, dict_distances[v])

    return parents, weights  # abbiamo bisogno di weights per calcolare velocemente il costo dei cammini


def ccrp(V, adj_list, sources, destinations):
    # aggiungo super sorgente con costo 0 e capacità infinity
    adj_list[0] = {}
    for s in sources:
        adj_list[0][s] = [0, -1]  # -1 = road_type di super
        # sorgente ovvero infinito

    # creo dizionario per salvare le capacità, ci serve eprchè una volta a zero togliamo l'arco dal dizionario
    capacity = {}
    for i in adj_list.keys():
        capacity[i] = {}
        for j in adj_list[i].keys():
            capacity[i][j] = CAPACITY[adj_list[i][j][1]]

    parents, weights = dijkstra(V, adj_list)
    plan = find_paths(parents)  # mappa dei cammini minimi dalla source alla dest

    min_path = get_path_with_min_cost(plan, weights)  # destinazione con path costo minimo

    b = True
    if min_path is None:
        b = False

    planCCRP = []
    flows = []

    while b:
        # print("Sto lavorando")
        planCCRP.append(plan[min_path])
        # dest=destinazione del cammino minimo, uso la lunghezza della lista per prendere l'ultimo elemento

        # get_flow torna la capacità (minima) di un cammino
        flow = get_flow(plan, min_path, capacity)
        flows.append(flow)

        for i in range(len(plan[min_path]) - 1):  # -1 per non uscire dal range
            # (stiamo considerando archi, l'ultimo elemento non ha un arco uscente)

            # arco da vi a vi1
            vi = plan[min_path][i]
            vi1 = plan[min_path][i + 1]
            capacity[vi][vi1] -= flow  # sottraggo capacità minima del path all'arco
            if capacity[vi][vi1] == 0:
                del adj_list[vi][vi1]

        # ricalcolo i cammini minimi una volta tolto l'arco
        parents, weights = dijkstra(V, adj_list)
        plan = find_paths(parents)
        min_path = get_path_with_min_cost(plan, weights)

        # se il cammino minimo non esiste esco dal while
        if min_path is None:
            # print("PRINTO PLAN:", plan)
            b = False

    # print(sum(flows))
    return planCCRP


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

    # Processing
    adj_list = create_adj_list(z, tails, heads, length, road_type)
    lul = ccrp(z, adj_list, sources, destinations)
    print(len(lul))
