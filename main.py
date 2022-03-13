import copy
from random import random

STARTBOARD = []
SOLVEDBOARD = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]
BLANK = {}
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
        self.way=[]

    def makeChild(self, board, birthMove):
        child = Node(board, self, birthMove)
        self.children.append(child)
        return child

    def move(self, move):
        findZero(self.board)
        y = BLANK['row']
        x = BLANK['col']
        if move == 'L':
            if x == 0 or (self.birthMove == 'R'):
                return None
            BLANK['col'] = BLANK['col'] - 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y][x - 1] = tempBoard[y][x - 1], tempBoard[y][x]
            print(tempBoard)
            left = self.makeChild(tempBoard,move)
            self.leftChild = left
            self.leftChild.way.append(move)
        if move == 'R':
            if x == 3 or (self.birthMove == 'L'):
                return None
            BLANK['col'] = BLANK['col'] + 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y][x + 1] = tempBoard[y][x + 1], tempBoard[y][x]
            print(tempBoard)
            self.rightChild = self.makeChild(tempBoard, move)
            self.rightChild.way.append(move)
        if move == 'D':
            if y == 0 or (self.birthMove == 'U'):
                return None  # Ending branch up
            BLANK['row'] = BLANK['row'] - 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y - 1][x] = tempBoard[y - 1][x], tempBoard[y][x]
            print(tempBoard)
            self.upChild = self.makeChild(tempBoard, move)
            self.upChild.way.append(move)
        if move == 'U':
            if y == 3 or (self.birthMove == 'D'):
                return None  # Ending branch down
            BLANK['row'] = BLANK['row'] + 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y + 1][x] = tempBoard[y + 1][x], tempBoard[y][x]
            print(tempBoard)
            self.downChild = self.makeChild(tempBoard, move)
            self.downChild.way.append(move)


def DFS(node, counter=0):
    if node is not None:
        if node.isBoardCorrect is False:
            node.vistied = True
            node.move('L')
            node.move('U')
            node.move('D')
            node.move('R')
            counter += 1
            for child in node.children:
                if not child.vistied:
                    DFS(child, counter)
        print("TUTAJ")




if __name__ == '__main__':
    readFromFileToBoard()
    findZero(STARTBOARD)
    root = Node(STARTBOARD)
    root.move('L')
    root.move('U')
    root.move('D')
    root.move('R')
    #DFS(root)
