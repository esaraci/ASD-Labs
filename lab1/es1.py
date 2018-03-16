# coding=utf-8
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

edges = np.loadtxt('./cit-HepTh.txt', dtype=int)

coda = edges[:, 0]
testa = edges[:, 1]

x = set(coda)
y = set(testa)

z = x.union(y)

print(len(z))

adj_list = {}
node_in_degrees = {}



for i in z:
    adj_list[i] = []
    node_in_degrees[i] = 0

for i in edges:
    adj_list[i[0]].append(i[1])
    node_in_degrees[i[1]] += 1

in_degrees = np.zeros(len(z))

for i in z:
    in_degrees[node_in_degrees[i]] += 1

print(in_degrees)

real_in_degrees = [(x/len(z)) for x in in_degrees]

out_degrees = np.zeros(len(z))

print(sum(real_in_degrees))
print(len(real_in_degrees))

for i in adj_list:
#    print(i, adj_list[i])
    out_degrees[len(adj_list[i])]+=1

av = 0

for i in range(len(out_degrees)):
    av += out_degrees[i]*i

av = av/(len(out_degrees))

print("media grado uscente")  # serve per esercizio 3
print(av)

fig, ax = plt.subplots()
ax.set_xscale('log', basex=10)
ax.set_yscale('log', basey=10)

axes = plt.gca()
# axes.set_xlim([0.9, 400])

ax.scatter(np.arange(len(real_in_degrees)), real_in_degrees, s=10)
plt.xlabel("In-degree")
plt.ylabel("Probability")
plt.savefig("es1.png")
plt.show()