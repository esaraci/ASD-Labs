import numpy as np
from graph import *
import threading
import time
from algorithms import *
from multiprocessing.pool import ThreadPool
import signal
import sys

# global
PI = 3.141592
RRR = 6378.388
stopper = False

INFINITY = float('inf')

do_i_need_to_stop = False

def held_karp(graph, v, S):
    """
    :param graph: Graph
    :param v: target node
    :param S: nodi poer cui dobbiamo passare
    :return:

    """
    global do_i_need_to_stop
    if do_i_need_to_stop is False:
        # Caso base
        if len(S) == 1:
            # print("Caso base:", v)
            return graph.get_adj_matrix(v, 0)  # S contiene un unico elemento che è v, stiamo andando da 0 —> v
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
    else:
        return INFINITY


def log_result(result):
    print("HELD_KARP:", result)


def waiter(sec):
    time.sleep(sec)
    global do_i_need_to_stop
    do_i_need_to_stop = True
    print("STOPPING THREAD")


if __name__ == "__main__":

    # BEGIN PREPROCESSING
    # removing comments and checking coordinate type
    geo = False
    c = 1
    f_name = "datasets/pcb442.tsp"
    with open(f_name) as f:
        line = f.readline()
        while line != "NODE_COORD_SECTION\n":

            if "EDGE_WEIGHT_TYPE" in line:
                if line.split(":")[1] == " GEO\n":
                    geo = True

            line = f.readline()
            c += 1

    dataset = np.loadtxt(f_name, skiprows=c, comments=["EOF"])

    l = len(dataset)
    lul = tuple(np.arange(l))
    # END PREPROCESSING

    # GENERATING GRAPH
    graph = Graph(dataset, geo)

    # pool = ThreadPool(processes=1)
    # result = pool.apply_async(held_karp, (graph, 0, lul), callback=log_result)
    # t = threading.Thread(target=waiter, args=(60*2, ))
    # t.daemon = True
    # t.start()
    # result.get()

    print("RANDOM:", random_insertion(graph))
    # print("PRIM:", prim(graph))









