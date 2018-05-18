import threading
import time
INFINITY = float('inf')


class HeldKarpThread(threading.Thread):
    def __init__(self, graph, v, S):
        threading.Thread.__init__(self)  # superclasse
        self.min_dist = INFINITY
        self.partial_solution = None
        self.graph = graph
        self.v = v
        self.S = S
        self.timestamp = None

    def get_results(self):
        return self.min_dist

    def run(self):
        self.timestamp = int(time.time())
        tmp = self.held_karp(self.graph, self.v, self.S)
        print("Passati {} secondi".format(int(time.time()) - self.timestamp))
        # print("distances", self.graph.distances)
        print("PART SOL:", self.partial_solution)
        print("MIN_DIST:", self.min_dist)

    def held_karp(self, graph, v, S):
        """
        :param graph: Graph
        :param v: target node
        :param S: nodi poer cui dobbiamo passare
        :return:
        """
        #if int(time.time()) - self.timestamp <= 120:
        # Caso base
        if len(S) == 1:
            # print("Caso base:", v)
            # return INFINITY
            return graph.get_adj_matrix(v, 0)  # S contiene un unico elemento che è v, stiamo andando da 0 --> v
        elif graph.get_distances((v, S)) is not None:
            return graph.get_distances((v, S))
        else:
            min_dist = INFINITY
            min_prec = None
            S1 = tuple([u for u in S if u != v])
            time_passed = False
            for u in S1:
                dist = self.held_karp(graph, u, S1)  # chiamata ricorsiva
                if dist == INFINITY:
                    time_passed = True
                    break

                if dist + graph.get_adj_matrix(u, v) < min_dist:  # aggiorno nel caso sia una quantità minore
                    min_dist = dist + graph.get_adj_matrix(u, v)
                    min_prec = u
            if not time_passed:
                self.partial_solution = (v, S)

            graph.set_distances((v, S), min_dist)
            graph.set_parents((v, S), min_prec)
            self.min_dist = min_dist  # salvo il valore di mindist
            return min_dist

        #return INFINITY