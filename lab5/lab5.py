import numpy as np
from hierarchical_clustering import *
from kmeans import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time


def error(cluster):
    tot_error = 0
    for elem in cluster.elements:
        w_i = pop[coordinates.index(elem)]
        tot_error += (w_i * euclidean_distance(elem, cluster.centroid)**2)

    return tot_error


def distortion(clusters):
    _distortion = 0
    for cluster in clusters:
        _distortion += error(cluster)

    return _distortion


if __name__ == '__main__':
    f_code = "290"
    f_name = "unifiedCancerData/unifiedCancerData_{}.csv".format(f_code)
    dataset = np.loadtxt(f_name, dtype=float, delimiter=',')

    n = len(dataset)
    number_of_clusters = 9
    x = dataset[:, 1]  # coordinate x
    y = dataset[:, 2]  # coordinate y
    pop = dataset[:, 3]  # population
    coordinates = [(x[i], y[i]) for i in range(n)]  # points

    start_time = time.time()
    # clusters = hierarchical_clustering(coordinates, number_of_clusters)
    clusters = kmeans(coordinates, number_of_clusters, pop, q=6)
    end_time = time.time() - start_time
    print("TEMPO: {}s".format(end_time))

    img = plt.imread("./immagini/USA_Counties.png")
    fig, ax = plt.subplots()
    ax.imshow(img)
    # ax.imshow(img, extent=[0, 400, 0, 300])

    # palette = itertools.cycle(sns.color_palette())

    colors = np.asarray(cm.rainbow(np.linspace(0, 1, number_of_clusters)))
    for cluster in clusters:
        elements = cluster.get_elements()
        centroid = cluster.get_centroid()
        # get random index
        ind = np.random.choice(colors.shape[0])
        # get random color from colors
        c = colors[ind]

        for element in elements:
            ax.plot((centroid[0], element[0]), (centroid[1], element[1]), linestyle='dashed',  color='black',
                    linewidth=0.4)
            # sns.pointplot(element[0], element[1], color=next(palette))
            ax.scatter(element[0], element[1], color=c)
        # delete color so it won't be picked in the future
        colors = np.delete(colors, ind, 0)

        ax.scatter(centroid[0], centroid[1], color='black')

    # plt.savefig("risposte/kmeans_{}_domanda5.png".format(f_code))
    plt.show()

    print("Distorsione:", distortion(clusters))
