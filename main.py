import numpy as np
import graphviz


def dfs(matrix, column, visited):
    for i in range(len(set_edges)):
        if matrix[i][column] == '1' and column + 1 != len(set_nodes) or matrix[i][column] == '-1' and column + 1 != len(
                set_nodes):
            visited.add(str(column + 1))
            for j in range(column + 1, len(set_nodes)):
                if matrix[i][j] == '1' or matrix[i][j] == '-1':
                    visited.add(str(j + 1))
                    dfs(matrix, j, visited)

    if visited == set_nodes:
        return True
    else:
        return False


def count_degree(matrix, column, i):
    value = 0
    found_loop = True

    if matrix[i][column] == '1' or matrix[i][column] == '-1':
        for j in range(len(set_nodes)):
            if j != column and (matrix[i][j] == '1' or matrix[i][j] == '-1'):
                value = value + 1
                found_loop = False
                break
        if found_loop is True:
            value = value + 2

    return value


def insertion_sort(even_cort):
    for i in range(1, len(even_cort)):
        key = even_cort[i]
        j = i - 1
        while j >= 0 and key[0] < even_cort[j][0]:
            even_cort[j + 1] = even_cort[j]
            j -= 1
        even_cort[j + 1] = key


match input("Directed = yes, not directed = no\n"):
    case 'yes':
        dot = graphviz.Digraph()
    case 'no':
        dot = graphviz.Graph()
    case _:
        print("Unknown command")
        exit('-1')

# Считываем матрицу из файла
matrix_of_incedence = []
nodes = 0
with open("matrix.txt") as matrix_file:
    for string in matrix_file:
        nodes = nodes + 1
        row = string.split()
        matrix_of_incedence.append(row)

set_nodes = set()
# Добавляем вершины
for i in range(nodes):
    set_nodes.add(str(i + 1))
    dot.node(str(i + 1))

# Записали матрицу
arr = np.array(matrix_of_incedence, str)
# Оттранспонировали ее
matrix = arr.transpose()

print(matrix)

# Добавляем ребра
set_edges = []
simple_graph = True
for string_of_nodes in matrix:
    one_node = True
    for i in range(len(string_of_nodes)):
        for j in range(i + 1, len(string_of_nodes)):
            if string_of_nodes[i] == string_of_nodes[j] == '1':
                set_edges.append(str(i + 1) + str(j + 1))
                if (str(j + 1) + str(i + 1)) in set_edges:
                    simple_graph = False
                one_node = False
            else:
                if (string_of_nodes[i] == '1' and string_of_nodes[j] == '-1') or (
                        string_of_nodes[i] == '-1' and string_of_nodes[j] == '1'):
                    set_edges.append(str(j + 1) + str(i + 1))
                    if (str(i + 1) + str(j + 1)) in set_edges:
                        simple_graph = False
                    one_node = False
    if one_node:
        simple_graph = False
        for i in range(len(string_of_nodes)):
            if string_of_nodes[i] == '1':
                set_edges.append(str(i + 1) + str(i + 1))

dot.edges(list(set_edges))

# Выводим пользователю граф
dot.render('doctest-output/round-table.gv', view=True)

# Проверка графа на связность по теореме в случае, если граф простой
if simple_graph:
    if (nodes - 1) * (nodes - 2) / 2 < len(set_edges):
        print("The Graph is linked")
    # Перепроверка графа на связность
    else:
        column = 0
        visited = set()
        if dfs(matrix, column, visited) is True:
            print("The Graph is linked")
        else:
            print("The Graph is not linked")

# Проверка графа на связность, если он не простой
else:
    column = 0
    visited = set()
    if dfs(matrix, column, visited) is True:
        print("The Graph is linked")
    else:
        print("The Graph is not linked")

even_cort = list()
for j in range(len(set_nodes)):
    degree_list = list()
    degree = 0
    for i in range(len(set_edges)):
        degree = degree + count_degree(matrix, j, i)
    if degree % 2 == 0:
        degree_list.append(degree)
        degree_list.append("-- degree for node #" + str(j + 1))
        even_cort.append(degree_list)

print("\nInsertion sort:")
insertion_sort(even_cort)
for i in even_cort:
    print(*i)
