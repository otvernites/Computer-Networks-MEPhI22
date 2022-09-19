"""
Оценка сложности алгоритма в .doc файле с соответствующим именем
"""
import re
import math


def adjacency_lists(adj, coords):
    for coord in coords:
        adj[coord[0]] = adj.get(coord[0], []) + [coord[1]]
        adj[coord[1]] = adj.get(coord[1], []) + [coord[0]]


def bfs(adjacency_lists, start):
    distance_lengths = {elem: math.inf for elem in adjacency_lists.keys()}
    distance_lengths[start] = 0
    queue = []
    queue.append(start)

    while len(queue):
        vertex = queue.pop()
        for neighbor in adjacency_lists[vertex]:
            if distance_lengths[neighbor] == math.inf:
                distance_lengths[neighbor] = distance_lengths[vertex] + 1
                queue.append(neighbor)
    return distance_lengths


def diameter(net):
    v = u = w = 0
    d = bfs(net, v)
    for i in enumerate(d):
        if d[i[1]] > d[u]:
            u = i[1]
    d = bfs(net, u)
    for i in enumerate(d):
        if d[i[1]] > d[w]:
            w = i[1]
    return d[w]


if __name__ == "__main__":
    coordinates = []
    with open("Network1.txt", "r") as network:
        for line in network:
            tmp_arr = re.findall(r'\d+\, \d+', line)

            for coord in tmp_arr:
                x, y = map(int, coord.split(", "))
                coordinates.append((x, y))

    net = {}
    adjacency_lists(net, coordinates)
    d = diameter(net)
    print(d)