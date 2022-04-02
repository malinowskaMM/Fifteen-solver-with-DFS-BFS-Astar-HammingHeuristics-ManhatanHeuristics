import copy
import sys
import time
from collections import deque

STARTBOARD = []
SOLVEDBOARD = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]
BLANK = {}
ORDER = []
MAXDEPTH = 10


def readFromFileToBoard(fileName):
    file = open(fileName, 'r')
    w = file.read(1)  # w - numbers of rows
    file.seek(2)
    k = file.read(1)  # k - numbers of columns
    file.seek(5)  # set postion at the beginning of second line of file
    for line in file:
        STARTBOARD.append(line.split())  # every line is a table with char values

    return STARTBOARD


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
                break

    return BLANK


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
        self.gCost = 0
        self.hCost = 0
        self.totalCost = 0
        self.depth = 0

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


def boardToStr(board):
    result = ""
    for row in board:
        for val in row:
            result = f'{result}{val}'
    return result


def dfs(node, startTime):
    isSolutionFound = False
    visitedStatesCount = 0
    nodeList = deque()
    way = deque()
    nodeList.append(node)
    processedStateCounter = 0
    solution = -1

    while nodeList and not isSolutionFound:
        currentNode = nodeList.pop()
        if currentNode.visited:
            continue
        currentNode.visited = True
        visitedStatesCount += 1
        # -------- process currentNode --------
        processedStateCounter += 1
        isSolutionFound = currentNode.isBoardCorrect
        if isSolutionFound:
            solution = currentNode.board
            solutionDepth = currentNode.depth
            wayNode = currentNode
            for i in range(solutionDepth):
                way.appendleft(wayNode.birthMove)
                wayNode = wayNode.parent
            continue

        if currentNode.depth < MAXDEPTH:
            for o in ORDER:
                currentNode.restrictMovement(o)
        # -------------------------------------
        for child in currentNode.children:
            if not child.visited:
                nodeList.append(child)

    elapsedTime = time.time_ns() - startTime
    return [solution, way, visitedStatesCount, processedStateCounter, solutionDepth, elapsedTime]


def bfs(node, processedStates=0):
    way = deque()
    startTime = time.time_ns()
    if node is not None:
        visitedStates = []
        listOfNodes = []
        visitedStates.append(node)
        processedStates += 1
        listOfNodes.append(node)
        discoveredSolutionFlag = node.isBoardCorrect
        while listOfNodes and discoveredSolutionFlag is False:
            vertex = listOfNodes.pop(0)
            processedStates += 1
            discoveredSolutionFlag = vertex.isBoardCorrect
            for o in ORDER:
                vertex.restrictMovement(o)
            for child in vertex.children:
                if child.isBoardCorrect is True:
                    solutionDepth = child.depth
                    wayNode = child
                    for i in range(solutionDepth):
                        way.appendleft(wayNode.birthMove)
                        wayNode = wayNode.parent

                    return [child.board, way, len(visitedStates), processedStates, solutionDepth,
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
    openList = []
    closedList = []
    openList.append(node)
    visitedStates += 1
    while openList:
        currentNode = min(openList, key=lambda node: node.totalCost)
        processedStates += 1
        depthCounter += 1
        if currentNode.birthMove is not None:
            way.append(currentNode.birthMove)
        openList.remove(currentNode)
        closedList.append(currentNode)

        if check(currentNode.board, SOLVEDBOARD) is True:
            return [currentNode.board, way, visitedStates, processedStates, depthCounter, time.time_ns() - startTime]

        for o in ORDER:
            currentNode.restrictMovement(o)
            visitedStates += 1
        for child in currentNode.children:
            child.gCost = currentNode.gCost + 1
            if heuristic == "manh":
                child.hCost = manhattanDist(child.board, SOLVEDBOARD)
            if heuristic == "hamm":
                child.hCost = hammingDist(child.board, SOLVEDBOARD)
            child.totalCost = child.gCost + child.hCost

            if child in openList:
                if child.gCost > min(openList, key=lambda node: node.totalCost).gCost:
                    continue
            openList.append(child)

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
            file.write("{:.6f}".format(time))
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
    ORDER = ['L', 'U', 'D', 'R']
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
