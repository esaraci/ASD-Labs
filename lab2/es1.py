import numpy as np
import random
import matplotlib.pyplot as plt


class UPATrial:
    def __init__(self, m):
        self.numNodes = m  # numero iniziale di nodi
        self.nodeNumbers = []  # lista di 111122223333444455...

        for i in range(m):
            for j in range(m):
                self.nodeNumbers.append(i)

    def run_trial(self, m):
        V = set()

        for i in range(m):  # estrae m nodi sempre
            u = random.choice(self.nodeNumbers) # estratto a caso
            V.add(u)  # contiene tutti i nodi estratti in questo turno

        for i in range(len(V)+1):  # len(V) può essere diverso da m perchè posso estrarre più volte lo stesso nodo
            self.nodeNumbers.append(self.numNodes)

        self.nodeNumbers.extend(V)  # aumentiamo la probabilità degli altri
        self.numNodes += 1

        return V


# n >= 1, 1 <= m <= n
def UPA(n, m):
    V = [x for x in range(m)]
    E = [(i, j) for i in V for j in V if i != j]

    trial = UPATrial(m)

    for u in range(m, n):
        V_1 = trial.run_trial(m)  # nodi estratti da trial
        V.append(u)
        for v in V_1:
            E.append((u, v))
    return V, E


def ER(n,p):
    V = [x for x in range(n)]
    E = []
    for i in V:
        for j in V:
            a = random.uniform(0, 1)
            if a < p and i != j:
                E.append((i, j))
    return V, E


def create_adj_list_from_graph(V, E):
    adj_list = {}
    for v in V:
        adj_list[v] = []

    for e in E:
        if e[0] != e[1]:  # evita cappi
            if e[1] not in adj_list[e[0]]:
                adj_list[e[0]].append(e[1])
                adj_list[e[1]].append(e[0])

    return adj_list


if __name__ == '__main__':
    data = np.loadtxt("./as19991212.txt", dtype=int)
    coda = data[:,0]
    testa = data[:,1]
    x = set(coda)
    y = set(testa)
    z = x.union(y)
    n = len(z) # numero di nodi

    adj_list_net = create_adj_list_from_graph(z, data)
    degrees = [len(adj_list_net[i]) for i in z]
    mean = int(np.average(degrees))

    print("NODI NET:", n)
    print("ARCHI NET:", int(sum([len(adj_list_net[i]) for i in z])/2))  # /2 perchè ci sono 2 archi


    # mean non serve, la grado medio di NET ha un significato diverso su UPA
    V_UPA, E_UPA = UPA(n, 2)
    # ADJ_UPA = create_adj_list_from_graph(V_UPA, E_UPA)
    print("NODI UPA:", len(V_UPA))
    print("ARCHI UPA:", len(E_UPA))

    V_ER, E_ER = ER(n, 0.0015)
    ADJ_ER = create_adj_list_from_graph(V_ER, E_ER)
    print("NODI ER:", len(V_ER))
    print("ARCHI ER:", len(E_ER))

