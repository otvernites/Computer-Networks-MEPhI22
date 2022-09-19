"""
Оценка сложности алгоритма в .doc файле с соответствующим именем
"""
import re
import numpy as np


def adjacency_matrix(adj, coords):
    for coord in coords:
        adj[coord[0], coord[1]] = 1
        adj[coord[1], coord[0]] = 1
    for i in range(adj.shape[0]):
        for j in range(adj.shape[0]):
            if i == j:
                adj[i, i] = 0


def diameter(net):
    n = len(net)

    # Floyd's algorithm - calculate the shortest path matrix
    for k in range(n):
        for i in range(n):
            for j in range(n):
                net[i, j] = min(net[i, j], net[i, k] + net[k, j])

    # Finding the maximum value from all maximum values by columns/rows
    diam = max(np.amax(net, axis = 0))
    return int(diam)


if __name__ == "__main__":
    coordinates = []
    with open("Network2.txt", "r") as network:
        for line in network:
            tmp_arr = re.findall(r'\d+\, \d+', line)

            for coord in tmp_arr:
                x, y = map(int, coord.split(", "))
                coordinates.append((x, y))

    max_value = 0
    for coord in coordinates:
        if coord[0] > max_value:
            max_value = coord[0]
        elif coord[1] > max_value:
            max_value = coord[1]

    net = np.full((max_value+1, max_value+1), np.inf)
    adjacency_matrix(net, coordinates)
    d = diameter(net)
    print(d)