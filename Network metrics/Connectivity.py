"""
Оценка сложности алгоритма в .doc файле с соответствующим именем
"""
import re
import math


def adjacency_lists(adj, coords):
    for coord in coords:
        adj[coord[0]] = adj.get(coord[0], []) + [coord[1]]
        adj[coord[1]] = adj.get(coord[1], []) + [coord[0]]


def bfs(adjacency_lists, start, unique_points):
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
                unique_points.discard(neighbor)
    return distance_lengths


if __name__ == "__main__":
    my_data_file = open('data.txt', 'w')
    coordinates = []
    unique_points = set()
    with open("Network3.txt", "r") as network:
        for line in network:
            tmp_arr = re.findall(r'\d+\, \d+', line)
            for coord in tmp_arr:
                x, y = map(int, coord.split(", "))
                unique_points.add(x)
                unique_points.add(y)
                coordinates.append((x, y))
                my_data_file.write(str(x)+','+str(y)+'\n')

    my_data_file.close()
    my_data_file = open('data.txt', 'r')
    str_list = []
    for i in my_data_file.readlines():
        if i not in str_list:
            str_list.append(i)
    my_data_file.close()
    true_file = open('DATA.txt', 'w')
    for j in str_list:
        true_file.write(j)
    true_file.close()

    net = {}
    adjacency_lists(net, coordinates)

    connectivity = 0
    while len(unique_points):
        bfs(net, unique_points.pop(), unique_points)
        connectivity += 1
    print(connectivity)
