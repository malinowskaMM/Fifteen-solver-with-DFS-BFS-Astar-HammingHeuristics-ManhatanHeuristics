import copy
import math
import sys
from random import random

STARTBOARD = []
SOLVEDBOARD = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]
BLANK = {}
ORDER = []
MAXDEPTH = 20


def readFromFileToBoard():
    file = open('input.txt', 'r')
    w = file.read(1)  # w - numbers of rows
    file.seek(2)
    k = file.read(1)  # k - numbers of columns
    file.seek(5)  # set postion at the beginning of second line of file
    for line in file:
        STARTBOARD.append(line.split())  # every line is a table with char values
    print(STARTBOARD)


def findZero(board):
    for col in range(0, len(board)):
        for row in range(0, len(board[col])):
            if board[row][col] == '0':
                BLANK['row'] = row
                BLANK['col'] = col
    print(BLANK)


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
        self.vistied = False

    def makeChild(self, board, birthMove):
        child = Node(board, self, birthMove)
        self.children.append(child)
        return child

    def move(self, move):
        findZero(self.board)
        y = BLANK['row']
        x = BLANK['col']
        if move == 'L':
            BLANK['col'] = BLANK['col'] - 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y][x - 1] = tempBoard[y][x - 1], tempBoard[y][x]
            print(tempBoard)
            left = self.makeChild(tempBoard, move)
            self.leftChild = left
        if move == 'R':
            BLANK['col'] = BLANK['col'] + 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y][x + 1] = tempBoard[y][x + 1], tempBoard[y][x]
            print(tempBoard)
            self.rightChild = self.makeChild(tempBoard, move)
        if move == 'U':
            BLANK['row'] = BLANK['row'] - 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y - 1][x] = tempBoard[y - 1][x], tempBoard[y][x]
            print(tempBoard)
            self.upChild = self.makeChild(tempBoard, move)
        if move == 'D':
            BLANK['row'] = BLANK['row'] + 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y + 1][x] = tempBoard[y + 1][x], tempBoard[y][x]
            print(tempBoard)
            self.downChild = self.makeChild(tempBoard, move)


    def restrictMovement(self, move):
        if move == 'L':
            if x == 0 or (self.birthMove == 'R'):
                return None
            move(move)
        if move == 'R':
            if x == 3 or (self.birthMove == 'L'):
                return None
            move(move)
        if move == 'U':
            if y == 0 or (self.birthMove == 'D'):
                 return None  # Ending branch up
            move(move)
        if move == 'D':
             if y == 3 or (self.birthMove == 'U'):
                  return None  # Ending branch down
             move(move)

    def backMove(self):
        if move == 'L':
            move('R')
        if move == 'R':
            move('L')
        if move == 'U':
            move('D')
        if move == 'D':
            move('U')

def DFS(node, counter=0):
    if node is not None:
        if node.isBoardCorrect is False:
            visited = []
            listOfNodes = []
            visited.append(node)
            listOfNodes.append(node)
            discoveredSolutionFlag = node.isBoardCorrect
            while listOfNodes and discoveredSolutionFlag is False:
                vertex = listOfNodes.pop()
                for o in ORDER:
                    vertex.restrictMovement(o)
                for child in vertex.children:
                    if child.isBoardCorrect is True:
                        print("Wynik:")
                        print(child.board)
                        return child.board
                    if child not in visited:
                        visited.append(child)
                        listOfNodes.append(child)


def BFS(node, counter=0):
    if node is not None:
        visited = []
        listOfNodes = []
        visited.append(node)
        listOfNodes.append(node)
        discoveredSolutionFlag = node.isBoardCorrect
        while listOfNodes and discoveredSolutionFlag is False:
            vertex = listOfNodes.pop(0)
            discoveredSolutionFlag = vertex.isBoardCorrect
            for o in ORDER:
                vertex.restrictMovement(o)
            for child in vertex.children:
                if child.isBoardCorrect is True:
                    print("Wynik:")
                    print(child.board)
                    print(child.way)
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
                distance += abs(j - indexCorrect[0]) + abs(i - indexCorrect[1])
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


def ASTAR(node, heuristic):
    discoveredSolutionFlag = node.isBoardCorrect
    while discoveredSolutionFlag is False:
        minCost = sys.maxsize
        for o in ORDER:
            vertex = node.move(o)
            if heuristic == 'manhattan':
                cost = manhattanDist(vertex.board, SOLVEDBOARD)
                if cost < minCost:
                    minCost = cost
            if heuristic == 'manhattan':
                cost = hammingDist(vertex.board, SOLVEDBOARD)
                if cost < minCost:
                    minCost = cost

    return 0;


if __name__ == '__main__':
    readFromFileToBoard()
    findZero(STARTBOARD)
    root = Node(STARTBOARD)
    ORDER = ['L', 'R', 'D', 'U']
    print(BFS(root))
