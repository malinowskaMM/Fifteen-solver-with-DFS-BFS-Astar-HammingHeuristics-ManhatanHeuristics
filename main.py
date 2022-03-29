from collections import deque
import copy
import sys
import time

STARTBOARD = []
SOLVEDBOARD = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]
BLANK = {}
ORDER = []
MAXDEPTH = 9
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


def check(board, solvedBoard):
    if board == solvedBoard:
        return True
    else:
        return False


class Node:
    def __init__(self, board, parent=None, birthMove=None, depth=0):
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
        self.depth = depth

    def makeChild(self, board, birthMove):
        child = Node(board, self, birthMove)
        child.depth = self.depth + 1
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
            if self.birthMove == "R":
                return None
            self.move(move)
        if move == 'R':
            if x == 3:
                return None
            if self.birthMove == "L":
                return None
            self.move(move)
        if move == 'U':
            if y == 0:
                return None  # Ending branch up
            if self.birthMove == "D":
                return None
            self.move(move)
        if move == 'D':
            if y == 3:
                return None  # Ending branch down
            if self.birthMove == "U":
                return None
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


def dfs(node, startTime):
    isSolutionFound = False
    visitedStates = deque()
    nodeList = deque()
    way = []
    nodeList.append(node)
    processedStateCounter = 0
    solutionDepth = -1
    solution = -1

    while nodeList and not isSolutionFound:
        currentNode = nodeList.pop()
        if currentNode in visitedStates:
            continue
        visitedStates.append(currentNode)

        # -------- process currentNode --------
        processedStateCounter += 1
        if currentNode.birthMove is not None:
            way.append(currentNode.birthMove)
            isSolutionFound = currentNode.isBoardCorrect
        if isSolutionFound:
            solution = currentNode.board
            solutionDepth = currentNode.depth
            continue
        if currentNode.depth < MAXDEPTH:
            for o in ORDER:
                currentNode.restrictMovement(o)
        # -------------------------------------
        for child in currentNode.children:
            if child not in visitedStates:
                nodeList.append(child)

    elapsedTime = time.time_ns() - startTime
    print(solution)
    return [solution, way, len(visitedStates), processedStateCounter, solutionDepth, elapsedTime]


# def dfs(node, way, visitedStates, processedStates, startTime, depthCounter=0):
#     if node is not None:
#         if node in visitedStates:
#             return
#         visitedStates.append(node)
#         if check(node.board, SOLVEDBOARD):
#             return [node.board, way, len(visitedStates), processedStates, depthCounter,
#                     time.time_ns() - startTime]
#         if depthCounter < MAXDEPTH:
#             for o in ORDER:
#                 node.restrictMovement(o)
#                 if node.children:
#                     child = node.children[-1]
#                     way.append(child.birthMove)
#                     result = dfs(child, way, visitedStates, processedStates + 1, startTime, depthCounter + 1)
#                     if result is not None:
#                         return result


def bfs(node, processedStates=0):
    way = []
    startTime = time.time_ns()
    depthCounter = 0
    if node is not None:
        visitedStates = []
        listOfNodes = []
        visitedStates.append(node)
        processedStates += 1
        depthCounter += 1
        listOfNodes.append(node)
        discoveredSolutionFlag = node.isBoardCorrect
        while listOfNodes and discoveredSolutionFlag is False:
            vertex = listOfNodes.pop(0)
            processedStates += 1
            depthCounter += 1
            if vertex.birthMove is not None:
                way.append(vertex.birthMove)
            discoveredSolutionFlag = vertex.isBoardCorrect
            for o in ORDER:
                vertex.restrictMovement(o)
            for child in vertex.children:
                if child.isBoardCorrect is True:
                    return [child.board, way, len(visitedStates), processedStates, depthCounter,
                            time.time_ns() - startTime]
                if child not in visitedStates:
                    visitedStates.append(child)
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


def astar(node, heuristic, way, startTime, processedStates=0, visitedStates=0, depthCounter=0):
    while check(node.board, SOLVEDBOARD) is False:
        minCost = sys.maxsize
        minCostMove = []
        for o in ORDER:
            node.restrictMovement(o)
            visitedStates += 1
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
        node.restrictMovement(minCostMove[0])
        way.append((minCostMove[0]))
        for child in node.children:
            if check(node.board, child.board) is False:
                return astar(child, heuristic, way, startTime, processedStates + 1, visitedStates, depthCounter + 1)
    return [node.board, way, visitedStates, processedStates, depthCounter, time.time_ns() - startTime]


def getOrder(orderSequence):
    ORDER.clear()
    for i in range(4):
        ORDER.append(orderSequence[i])


def writeStatistics(fileName, result):
    file = open(fileName, 'w')
    for i in range(1, len(result)):
        if i == 1:
            file.write(str(len(result[i])))
            file.write("\n")
        elif i == 5:
            time = result[i] / 1000000
            file.write("{:.3f}".format(time))
        else:
            line = str(result[i])
            file.write(line)
            file.write("\n")


def writeSolution(fileName, result):
    file = open(fileName, 'w')
    sol = result[1]
    file.write(str(len(sol)))
    file.write("\n")
    way = ""
    for i in range(0, len(sol)):
        way += sol[i]
    file.write(way)


if __name__ == '__main__':
    readFromFileToBoard(sys.argv[3])
    ORDER = ['L', 'R', 'D', 'U']
    findZero(STARTBOARD)
    root = Node(STARTBOARD)
    if sys.argv[1] == 'bfs':
        getOrder(sys.argv[2])
        solution = bfs(root, 0)
        writeSolution(sys.argv[4], solution)
        writeStatistics(sys.argv[5], solution)
    elif sys.argv[1] == 'dfs':
        getOrder(sys.argv[2])
        solution = dfs(root, time.time_ns())
        writeSolution(sys.argv[4], solution)
        writeStatistics(sys.argv[5], solution)
    elif sys.argv[1] == 'astar':
        solution = astar(root, sys.argv[2], [], time.time_ns())
        writeSolution(sys.argv[4], solution)
        writeStatistics(sys.argv[5], solution)
