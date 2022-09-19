"""
Задаем веса = 1 для инициализации первого верхнего слоя графа.
Высчитываем веса вершин каждой новой строки матрицы, исходя из значений предыдущей:
для вершин каждой последующей строки суммируем веса входящих в нее ребер.
Результирующее количество маршрутов содержится в последнем элементе массива paths_number на конечной итерации
при его заполнении.
                                Сложность алгоритма:
В строке 37 при итерации по высоте графа мы используем вложенный цикл (строки 38, 21), который,
в свою очередь, итерируется уже по его ширине.
Поэтому сложность алгоритма составляет O(MN), где М - высота графа, N - ширина <=> (N+1)+N*(M-1) ∈ O(MN)
"""


# calculation of the number of paths for the vertices of the i-row
# (using the previously calculated values of the i-1 row)
# O(N)
def layer_calculation(arr, w):
    new_arr = []
    new_arr.append(arr[0])

    for i in range(w):
        new_arr.append(new_arr[i] + arr[i] + arr[i + 1])

    return new_arr


if __name__ == "__main__":
    width = 794
    height = 871

    paths_number = []
    # initialization of the vertices of the first row ... O(N+1)
    for i in range(width + 1):
        paths_number.append(1)

    # updating array for row-layers ... O(N*(M-1))
    for i in range(height - 1):
        paths_number = layer_calculation(paths_number, width)

    # got the number of paths for the vertices of the last row of the matrix
    print(paths_number[width - 1])
