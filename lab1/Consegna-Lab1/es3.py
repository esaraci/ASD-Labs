import numpy as np
import random
import matplotlib.pyplot as plt


class DPATrial:
    def __init__(self, m):
        self.numNodes = m  # numero iniziale di nodi
        self.nodeNumbers = [] 

        for i in range(m):
            for j in range(m):
                self.nodeNumbers.append(i)

    def run_trial(self, m):
        V = set()

        for i in range(m):
            u = random.choice(self.nodeNumbers) # estratto a caso
            V.add(u)

        self.nodeNumbers.append(self.numNodes)
        self.nodeNumbers.extend(V)
        self.numNodes += 1

        return V

# n >= 1, 1 <= m <= n
def DPA(n, m):
    V = [x for x in range(m)]
    E = [(i, j) for i in V for j in V if i != j]

    trial = DPATrial(m)

    for u in range(m, n):
        V_1 = trial.run_trial(m)  # nodi estratti da trial
        V.append(u)
        for v in V_1:
            E.append((u, v))
    return V, E

def in_degree(E, n):
    cont = 0
    for x in E:
        if x[1] == n:
            cont+=1
    return cont

def tot_in_degree(V, E):
    in_degrees = np.zeros(len(V))

    for i in V:
        in_degrees[in_degree(E, i)]+=1

    real_in_degrees = [(x/len(V)) for x in in_degrees if x != 0]

    return real_in_degrees


if __name__ == '__main__':

    n = 27770
    m = 13 #arrotondamento di 12.7046092906, media del grado uscente del grafo dell'es 1

    fig, ax = plt.subplots()
    ax.set_xscale('log', basex=10)
    ax.set_yscale('log', basey=10)

    axes = plt.gca()
    axes.set_xlim([0.9, 400])

    vertices, edges = DPA(n, m)
    real_in_degrees = tot_in_degree(vertices, edges)
    plt.xlabel("In-degree")
    plt.ylabel("Probability")

    ax.scatter(np.arange(len(real_in_degrees)), real_in_degrees, s=10)
    plt.savefig("es3.png")
    plt.show()