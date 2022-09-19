import re
import math
import numpy as np


# Заполнение матрицы коэффициентов α, поучение списков смежности для графа сетей
def get_adjacency_lists(adj, coords, alph, alphas):
    i = 0
    for coord in coords:
        adj[coord[0]] = adj.get(coord[0], []) + [coord[1]]
        adj[coord[1]] = adj.get(coord[1], []) + [coord[0]]

        alph[coord[0], coord[1]] = alphas[i]
        alph[coord[1], coord[0]] = alphas[i]
        i += 1


# Добавление промежуточных путей (для нижней функции)
def append_new_paths(paths, old_list, adj_list):
    for net in adj_list:
        if old_list[-1] < net:
            paths.append(old_list + [net])


# Построение списка всех путей
def get_paths(adj_lists, paths, end):
    i = 0
    while True:
        # добавление промежуточных маршрутов
        if paths[i][-1] != end:
            append_new_paths(paths, paths[i], adj_lists[paths[i][-1]])

        # удаление рассмотренного маршрута
        if paths[i][-1] != end:
            paths.pop(i)
        # все маршруты рассчитаны
        elif paths[i][-1] == end and len(paths) == i+1:
            break
        # переход к следующему маршруту
        else:
            i += 1
    print(len(paths))


# Вычисление вероятности для конкретного файрвола
def probability_calculation(start, end, alpha_matrix, t):
    alpha = alpha_matrix[start, end]
    return math.exp(-alpha*t*10**(-3))


if __name__ == "__main__":

    # Инициализация начальных значений
    start = 1
    end = 50
    alphas = [1082, 625, 816, 744, 1806, 1798, 1182, 453, 1251, 1970, 1894, 980, 747, 1353, 693, 1577, 1559, 1060, 635, 764, 1897, 1947, 577, 1988, 875, 782, 358, 578, 1155, 348, 1779, 1353, 1661, 957, 1696, 1006, 1232, 1123, 1007, 1572, 1407, 1556, 1744, 783, 1306, 1910, 1953, 1508, 815, 749, 1851, 726, 1984, 1298, 1531, 362, 1453, 1197, 539, 1048, 1752, 1148, 1742, 1674, 1117, 585, 1430, 1321, 1218, 1826, 414, 1046, 1297, 774, 491, 1721, 680, 1605, 1772, 1651, 1281, 460, 1809, 1911, 1290, 594, 789, 630, 1478, 391, 1628, 883, 1564, 538, 1757, 1368, 693, 1249, 754, 1555, 972, 1538, 1996, 281, 1807, 743, 858, 1528, 1140, 510, 301, 1361]
    t = 0.4888

    # Построение списков смежности графа, а также матрицы коэффициентов альфа
    networks = []
    with open("Networks.txt", "r") as n:
        for line in n:
            tmp_arr = re.findall(r'\d+\, \d+', line)

            for net in tmp_arr:
                x, y = map(int, net.split(", "))
                networks.append((x, y))

    adjacency_list = {}
    alpha_matrix = np.zeros((end+1, end+1))
    get_adjacency_lists(adjacency_list, networks, alpha_matrix, alphas)

    # Получение списка всех путей
    paths = [[start]]
    get_paths(adjacency_list, paths, end)

    # Для каждого пути необходимо высчитать вероятность прохождения плохого пакета, что означает -
    # все файрволы его пропустят.
    # Общая вероятность рассчитывается как произведение вероятностей P прохождения пакета между парами файрволов
    # в маршруте, потому что все эти события независимы.
    probabilities = []
    for path in paths:
        tmp_prob = []
        for i in range(len(path)-1):
            tmp_prob.append(probability_calculation(path[i], path[i+1], alpha_matrix, t))
        probabilities.append(math.prod(tmp_prob))

    # Зная то, что хакер изучил структуру сети и свойства файрволов, а также то, что он очень хочет,
    # чтобы пакет дошел, можно сделать следующий вывод:
    # для пересылки пакета он выберет тот путь, на котором ВЕРОЯТНОСТЬ его доставки МАКСИМАЛЬНАЯ.
    # Получаем ответ:
    print(max(probabilities))





