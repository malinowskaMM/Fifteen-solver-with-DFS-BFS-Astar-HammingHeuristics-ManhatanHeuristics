import random

model_matrix = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 0]]


def check_valid(matrix):
    if matrix == model_matrix:
        return True
    else:
        return False

#0 musi być w prawym dolnym rogu
def generate_random_matrix():
    list_of_numbers = [*range(1, 16, 1)]
    print(list_of_numbers)
    random.shuffle(list_of_numbers)
    matrix = [list_of_numbers[0:4], list_of_numbers[4:8], list_of_numbers[8:12], list_of_numbers[12:16]+[0]]
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


def DFS(node, visitedList):
    if node:
        visitedList.append(node.data)
        DFS(node.left, visitedList)
        DFS(node.right, visitedList)



# print(generate_random_matrix())

# przykładowe drzewo dla sprawdzenia poparwności działania algorytmu DFS
#               3
#      2                    6
#          4            5       7
#       1       11    0           13
#
# zgodnie z DFS powinno byc
node1 = Node(1)
node11 = Node(11)
node0 = Node(0)
node13 = Node(13)
node4 = Node(4, node1, node11)
node5 = Node(5, node0)
node7 = Node(7, None, node13)
node2 = Node(2, None, node4)
node6 = Node(6, node5, node7)
node3 = Node(3, node2, node6)

list = []
DFS(node3, list)
print(list)
