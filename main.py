import copy
import sys

STARTBOARD = []
SOLVEDBOARD = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]
BLANK = {}
ORDER = []
MAXDEPTH = 5
DFS_MOVE_COUNTER = 0


def readFromFileToBoard(fileName):
    file = open(fileName, 'r')
    w = file.read(1)  # w - numbers of rows
    file.seek(2)
    k = file.read(1)  # k - numbers of columns
    file.seek(5)  # set postion at the beginning of second line of file
    for line in file:
        STARTBOARD.append(line.split())  # every line is a table with char values


def readFromInputToBoard():
    file = open('input.txt', 'r')
    w = file.read(1)  # w - numbers of rows
    file.seek(2)
    k = file.read(1)  # k - numbers of columns
    file.seek(5)  # set postion at the beginning of second line of file
    for line in file:
        STARTBOARD.append(line.split())  # every line is a table with char values


def writeBoardToFile(fileName, board):
    file = open(fileName, 'w')
    for col in range(0, len(board)):
        line = ""
        for row in range(0, len(board[col])):
            line += board[col][row] + " "
        file.write(line)
        file.write("\n")


def findZero(board):
    for col in range(0, len(board)):
        for row in range(0, len(board[col])):
            if board[row][col] == '0':
                BLANK['row'] = row
                BLANK['col'] = col
    # print(BLANK)


def check(board, solvedBoard):
    if board == solvedBoard:
        return True
    else:
        return False


class Node:
    def __init__(self, board, parent=None, birthMove=None):
        self.board = board
        self.isBoardCorrect = check(self.board, SOLVEDBOARD)
        self.parent = parent
        self.birthMove = birthMove
        self.leftChild = None
        self.rightChild = None
        self.upChild = None
        self.downChild = None
        self.children = []
        self.visited = False
        self.depthCounter = 0

    def makeChild(self, board, birthMove):
        child = Node(board, self, birthMove)
        self.children.append(child)
        return child

    def move(self, move):
        # print(move)
        findZero(self.board)
        y = BLANK['row']
        x = BLANK['col']
        if move == 'L':
            BLANK['col'] = BLANK['col'] - 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y][x - 1] = tempBoard[y][x - 1], tempBoard[y][x]
            self.leftChild = self.makeChild(tempBoard, move)
        if move == 'R':
            BLANK['col'] = BLANK['col'] + 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y][x + 1] = tempBoard[y][x + 1], tempBoard[y][x]
            self.rightChild = self.makeChild(tempBoard, move)
        if move == 'U':
            BLANK['row'] = BLANK['row'] - 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y - 1][x] = tempBoard[y - 1][x], tempBoard[y][x]
            self.upChild = self.makeChild(tempBoard, move)
        if move == 'D':
            BLANK['row'] = BLANK['row'] + 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y + 1][x] = tempBoard[y + 1][x], tempBoard[y][x]
            self.downChild = self.makeChild(tempBoard, move)

    def restrictMovement(self, move):
        findZero(self.board)
        y = BLANK['row']
        x = BLANK['col']
        if move == 'L':
            if x == 0:
                return None
            self.move(move)
        if move == 'R':
            if x == 3:
                return None
            self.move(move)
        if move == 'U':
            if y == 0:
                return None  # Ending branch up
            self.move(move)
        if move == 'D':
            if y == 3:
                return None  # Ending branch down
            self.move(move)

    def backMove(self):
        findZero(self.board)
        y = BLANK['row']
        x = BLANK['col']
        if self.birthMove == 'L':
            if x == 3:
                return None
            self.board[y][x], self.board[y][x + 1] = self.board[y][x + 1], self.board[y][x]
        elif self.birthMove == 'R':
            if x == 0:
                return None
            self.board[y][x], self.board[y][x - 1] = self.board[y][x - 1], self.board[y][x]
        elif self.birthMove == 'U':
            if y == 3:
                return None
            self.board[y][x], self.board[y + 1][x] = self.board[y + 1][x], self.board[y][x]
        elif self.birthMove == 'D':
            if y == 0:
                return None
            self.board[y][x], self.board[y - 1][x] = self.board[y - 1][x], self.board[y][x]
        self.children.clear()
        self.leftChild = None
        self.rightChild = None
        self.upChild = None
        self.downChild = None


# def DFS(node, counter=0):
#     counter = 0
#     if node is not None:
#         if node.isBoardCorrect is False:
#             visited = []
#             listOfNodes = []
#             visited.append(node)
#             listOfNodes.append(node)
#             discoveredSolutionFlag = node.isBoardCorrect
#             while listOfNodes and discoveredSolutionFlag is False:
#                 vertex = listOfNodes.pop()
#                 counter += 1
#                 discoveredSolutionFlag = node.isBoardCorrect
#                 print("Counter: ", counter)
#                 for o in ORDER:
#                     vertex.restrictMovement(o)
#                 for child in vertex.children:
#                     if child.isBoardCorrect is True:
#                         print("Wynik:")
#                         print(child.board)
#                         return child.board
#                     if child not in visited:
#                         visited.append(child)
#                         listOfNodes.append(child)


def dfs(node, moveCounter, depthCounter=0):
    if node is None:
        return
    if node.visited:
        return

    node.depthCounter = depthCounter
    node.visited = True
    discoveredSolutionFlag = node.isBoardCorrect

    if check(node.board, SOLVEDBOARD):
        # print("Wynik:")
        # print(node.board)
        return node.board

    if node.depthCounter < MAXDEPTH:
        # print("Depth: ", node.depthCounter)
        for o in ORDER:
            node.restrictMovement(o)
            if node.children:
                child = node.children[-1]
                result = dfs(child, node.depthCounter + 1, moveCounter)
                if result is not None:
                    #print("Zbadana glebokosc drzewa:", node.depthCounter)
                    return result


def bfs(node, counter=0):
    counter = 0
    if node is not None:
        visited = []
        listOfNodes = []
        visited.append(node)
        listOfNodes.append(node)
        discoveredSolutionFlag = node.isBoardCorrect
        while listOfNodes and discoveredSolutionFlag is False:
            vertex = listOfNodes.pop(0)
            counter += 1
            discoveredSolutionFlag = vertex.isBoardCorrect
            for o in ORDER:
                vertex.restrictMovement(o)
            for child in vertex.children:
                if child.isBoardCorrect is True:
                    print("Ilosc odwiedzonych wezlow: ", counter)
                    print("Wynik:")
                    print(child.board)
                    return child.board
                if child not in visited:
                    visited.append(child)
                    listOfNodes.append(child)


def searchByValue(matrix, value):
    rows = len(matrix)
    columns = len(matrix[0])
    for i in range(0, rows):
        for j in range(0, columns):
            if matrix[i][j] == value:
                return [i, j]


def manhattanDist(matrix, modelMatrix):
    distance = 0
    rows = len(matrix)
    columns = len(matrix[0])
    for i in range(0, rows):
        for j in range(0, columns):
            if matrix[i][j] != modelMatrix[i][j]:
                indexCorrect = searchByValue(modelMatrix, matrix[i][j])
                distance += abs(j - indexCorrect[1]) + abs(i - indexCorrect[0])
    return distance


def hammingDist(matrix, modelMatrix):
    diffCounter = 0
    rows = len(matrix)
    columns = len(matrix[0])
    for i in range(0, rows):
        for j in range(0, columns):
            if matrix[j][i] != modelMatrix[j][i]:
                diffCounter += 1
    return diffCounter


def astar(node, heuristic):
    while check(node.board, SOLVEDBOARD) is False:
        minCost = sys.maxsize
        minCostMove = []
        for o in ORDER:
            node.restrictMovement(o)
        for child in node.children:
            if heuristic == "manh":
                cost = manhattanDist(child.board, SOLVEDBOARD)
                if cost < minCost:
                    minCost = cost
                    minCostMove.clear()
                    minCostMove.append(child.birthMove)
            if heuristic == "hamm":
                cost = hammingDist(child.board, SOLVEDBOARD)
                if cost < minCost:
                    minCost = cost
                    minCostMove.clear()
                    minCostMove.append(child.birthMove)
            child.backMove()
        #print(minCostMove[0])
        node.restrictMovement(minCostMove[0])
        for child in node.children:
            if check(node.board, child.board) is False:
                return astar(child, heuristic)
    return node.board


def getOrder(orderSequence):
    ORDER.clear()
    for i in range(4):
        ORDER.append(orderSequence[i])


def getSolutionFileName():
    return sys.argv[3] + "_" + sys.argv[1] + "_" + sys.argv[2] + "_sol.txt"


if __name__ == '__main__':
    readFromFileToBoard(sys.argv[3])
    ORDER = ['L', 'R', 'D', 'U']
    findZero(STARTBOARD)
    root = Node(STARTBOARD)
    if sys.argv[1] == 'bfs':
        getOrder(sys.argv[2])
        writeBoardToFile(getSolutionFileName(), bfs(root, 0))
    elif sys.argv[1] == 'dfs':
        getOrder(sys.argv[2])
        writeBoardToFile(getSolutionFileName(), dfs(root, 0, 0))
    elif sys.argv[1] == 'astar':
        writeBoardToFile(getSolutionFileName(), astar(root, sys.argv[2]))
