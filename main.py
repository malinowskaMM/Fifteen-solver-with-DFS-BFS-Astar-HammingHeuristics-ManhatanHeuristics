import random

model_matrix_4x4 = [[1, 2, 3, 4],
                    [5, 6, 7, 8],
                    [9, 10, 11, 12],
                    [13, 14, 15, 0]]
matrix_4x4 = [[1, 2, 3, 8],
              [5, 6, 7, 8],
              [9, 9, 11, 12],
              [13, 14, 15, 1]]


def check_valid(matrix):
    if matrix == model_matrix_4x4:
        return True
    else:
        return False


def generate_random_matrix():
    list_of_numbers = [*range(1, 16, 1)]
    print(list_of_numbers)
    random.shuffle(list_of_numbers)
    matrix = [list_of_numbers[0:4], list_of_numbers[4:8], list_of_numbers[8:12], list_of_numbers[12:16] + [0]]
    return matrix


class Node:
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.visited = False

    def __add__(self, node):
        if self.data > node.data:
            self.left = node
        else:
            self.right = node


def DFS(node, visited_list):
    if node:
        visited_list.append(node.data)
        DFS(node.left, visited_list)
        DFS(node.right, visited_list)


graph = {3: [2, 6],
         2: [3, 4],
         4: [2, 1, 11],
         11: [4],
         6: [3, 5, 7],
         5: [6, 0],
         0: [5],
         7: [6, 13],
         13: [7],
         1: [4]}


def BFSorDFS(graph, root, chooser):
    visited = []
    list_od_nodes = []
    visited.append(root)
    list_od_nodes.append(root)
    while list_od_nodes:
        if chooser == 'bfs':
            vertex = list_od_nodes.pop(0)
        elif chooser == 'dfs':
            vertex = list_od_nodes.pop()
        print(str(vertex) + " ")
        for g in graph[vertex]:
            if g not in visited:
                visited.append(g)
                list_od_nodes.append(g)


def hamming_dist(matrix, model_matrix):
    diff_counter = 0
    rows = len(matrix)
    columns = len(matrix[0])
    for i in range(0, rows):
        for j in range(0, columns):
            if matrix[j][i] != model_matrix[j][i]:
                diff_counter += 1
    return diff_counter


print(hamming_dist(matrix_4x4, model_matrix_4x4))
#                 3
#       2           |        6
#           4       |    5       7
#       1       11  |  0           13
#

# BFSorDFS(graph, 3, 'dfs')
print("\n")
# BFSorDFS(graph, 3, 'bfs')
