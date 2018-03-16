import numpy as np
import random
import matplotlib.pyplot as plt

data = np.loadtxt("./as19991212.txt")

class UPATrial:
    def __init__(self, m):
        self.numNodes = m  # numero iniziale di nodi
        self.nodeNumbers = []  # lista di 111122223333444455...

        for i in range(m):
            for j in range(m):
                self.nodeNumbers.append(i)

    def run_trial(self, m):
        V = set()

        for i in range(m): # estrae m nodi sempre
            u = random.choice(self.nodeNumbers) # estreatto a caso
            V.add(u) # contiene tutti i nodi estratti in questo turno

        for i in range(len(V)+1): # len(V) può essere diverso da m perchè posso estrarre due volte lo stesso nodo
            self.nodeNumbers.append(self.numNodes)

        self.nodeNumbers.extend(V)  # aumentiamo la probabilità degli altri
        self.numNodes += 1

        return V




# 1 1 1 1 1 2 2 2 2 2 3 3 3 3 3 4 4 4 4 4 5 5 5 5 5

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




def degree(E, n):
    cont = 0
    for x in E:
        if x[1] == n:
            cont+=1
    return cont

def tot_in_degree(V, E):
    in_degrees = np.zeros(len(V))

    for i in V:
        in_degrees[in_degree(E, i)]+=1

    real_in_degrees = [(x/len(V)) for x in in_degrees]

    return real_in_degrees
