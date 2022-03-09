import math
import random

model_matrix_4x4 = [[1, 2, 3, 4],
                    [5, 6, 7, 8],
                    [9, 10, 11, 12],
                    [13, 14, 15, 0]]
matrix_4x4 = [[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 0, 12],
              [13, 14, 15, 11]]


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

def vertex_count_per_level(depth, leave_count):
    return pow(leave_count, depth)

def vertex_count(tree_depth, leave_count):
    result = 0
    for i in range(tree_depth):
        result += vertex_count_per_level(i, leave_count)
    return result

 def generate_tree_2_leafs(tree_depth):
     leaves_per_vertex_count = 2

     vertex_total = vertex_count(tree_depth, leaves_per_vertex_count)
     node_list = []
     vert_data = 1

     for i in range(vertex_total):
         n = Node(vert_data)
         node_list.append(n)
         vert_data += 1

     lower_lvl_counter = 0

     # idziemy po drzewie od dolu
     for depth_current in range(tree_depth -1, 0, -1):
         lower_lvl_vert_count = vertex_count_per_level(depth_current, leaves_per_vertex_count)
         higher_lvl_vert_count = vertex_count_per_level(depth_current - 1, leaves_per_vertex_count)

         lower_lvl_first_node = vertex_total - lower_lvl_vert_count - lower_lvl_counter
         higher_lvl_first_node = lower_lvl_first_node - higher_lvl_vert_count
         lower_lvl_counter += lower_lvl_vert_count

         for vert in range(higher_lvl_vert_count):
             # tutaj przy 4 galeziach bedzie do zmiany .left .right
             node_list[higher_lvl_first_node + vert].left = node_list[lower_lvl_first_node]
             node_list[higher_lvl_first_node + vert].right = node_list[lower_lvl_first_node + 1]
             lower_lvl_first_node += leaves_per_vertex_count
     return node_list

#zeby to dzialalo, Node musi miec self.left, self.right, self.up, self.down
#def generate_tree_4_leafs(tree_depth):
#    leaves_per_vertex_count = 4
#
#    vertex_total = vertex_count(tree_depth, leaves_per_vertex_count)
#    node_list = []
#    vert_data = 1
#
#    for i in range(vertex_total):
#        n = Node(vert_data)
#        node_list.append(n)
#        vert_data += 1
#
#    lower_lvl_counter = 0
#
#    # idziemy po drzewie od dolu
#    for depth_current in range(tree_depth -1, 0, -1):
#        lower_lvl_vert_count = vertex_count_per_level(depth_current, leaves_per_vertex_count)
#        higher_lvl_vert_count = vertex_count_per_level(depth_current - 1, leaves_per_vertex_count)
#
#        lower_lvl_first_node = vertex_total - lower_lvl_vert_count - lower_lvl_counter
#        higher_lvl_first_node = lower_lvl_first_node - higher_lvl_vert_count
#        lower_lvl_counter += lower_lvl_vert_count
#
#        for vert in range(higher_lvl_vert_count):
#            # tutaj przy 4 galeziach bedzie do zmiany .left .right
#            node_list[higher_lvl_first_node + vert].left = node_list[lower_lvl_first_node]
#            node_list[higher_lvl_first_node + vert].right = node_list[lower_lvl_first_node + 1]
#            node_list[higher_lvl_first_node + vert].up = node_list[lower_lvl_first_node + 2]
#            node_list[higher_lvl_first_node + vert].down = node_list[lower_lvl_first_node + 3]
#            lower_lvl_first_node += leaves_per_vertex_count
#    return node_list

class Node:
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.visited = False


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


def dfs_or_bfs(graph, root, chooser):
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


def search_by_value(matrix, value):
    rows = len(matrix)
    columns = len(matrix[0])
    for i in range(0, rows):
        for j in range(0, columns):
            if matrix[i][j] == value:
                return [i, j]


def manhattan_dist(matrix, model_matrix):
    rows = len(matrix)
    columns = len(matrix[0])
    for i in range(0, rows):
        for j in range(0, columns):
            if matrix[i][j] != model_matrix[i][j]:
                index_correct = search_by_value(model_matrix, matrix[i][j])
                return math.sqrt((j - index_correct[0]) ** 2 + (i - index_correct[1]) ** 2)


print(hamming_dist(matrix_4x4, model_matrix_4x4))
print(manhattan_dist(matrix_4x4, model_matrix_4x4))
#                 3
#       2           |        6
#           4       |    5       7
#       1       11  |  0           13
#

# BFSorDFS(graph, 3, 'dfs')
print("\n")
# BFSorDFS(graph, 3, 'bfs')
