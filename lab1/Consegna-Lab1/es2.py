import numpy as np
import random
import matplotlib.pyplot as plt


def ER(n,p):
    V = [x for x in range(n)]
    E = []
    for i in V:
        for j in V:
            a = random.uniform(0, 1)
            if a < p and i != j:
                E.append((i, j))
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

    real_in_degrees = [(x/len(V)) for x in in_degrees if x!=0]

    return real_in_degrees


if __name__ == '__main__':

    for i in range(4):

        n = 200*(i+1)
        p = 0.5

        fig, ax = plt.subplots()
        # ax.set_xscale('log', basex=10)
        # ax.set_yscale('log', basey=10)

        axes = plt.gca()
        # axes.set_xlim([1, 400])

        vertices, edges = ER(n, p)
        real_in_degrees = tot_in_degree(vertices, edges)
        plt.xlabel("In-degree")
        plt.ylabel("Probability")

        ax.scatter(np.arange(len(real_in_degrees)), real_in_degrees, s=10)
        plt.savefig("es2_{}.png".format(i))