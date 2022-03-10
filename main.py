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


def findField(board):
    for col in range(0, len(board)):
        for row in range(0, len(board[col])):
            if board[row][col] == '0':
                BLANK['row'] = row
                BLANK['col'] = col
    print(BLANK)


def check(board, solvedBoard):
    if board == solvedBoard:
        return True


class Node:
    def __init__(self, board, parent):
        self.board = board
        self.children = []
        if parent is not None:  # None is reserved for ROOT node
            self.parent = parent

    def makeChild(self, board, move):
        child = Node(board, self)
        self.children.append(child)

    def move(self, move):
        yPos=BLANK['row']
        xPos=BLANK['col']
        if move == 'L':
            if xPos == 0:
                return 0        # Ending branch on left
            BLANK['col'] -= 1
            tempBoard = self.board
            tempBoard[yPos][xPos] = tempBoard[yPos][xPos-1]
            tempBoard[yPos][xPos-1] = '0'
            print(tempBoard)
            self.makeChild(tempBoard, move)
        if move == 'R':
            if xPos == 3:
                return 0        # Ending branch on right
            BLANK['col'] += 1
            tempBoard = self.board
            tempBoard[yPos][xPos] = tempBoard[yPos][xPos+1]
            tempBoard[yPos][xPos+1] = '0'
            print(tempBoard)
            self.makeChild(tempBoard, move)
        if move == 'U':
            if yPos == 3:
                return 0        # Ending branch up
            BLANK['row'] -= 1
            tempBoard = self.board
            tempBoard[yPos][xPos] = tempBoard[yPos-1][xPos]
            tempBoard[yPos-1][xPos] = '0'
            print(tempBoard)
            self.makeChild(tempBoard, move)
        if move == 'D':
            if yPos == 0:
                return 0        # Ending branch down
            BLANK['row'] += 1
            tempBoard = self.board
            tempBoard[yPos][xPos] = tempBoard[yPos+1][xPos]
            tempBoard[yPos+1][xPos] = '0'
            print(tempBoard)
            self.makeChild(tempBoard, move)


def dfs():
    root=Node(STARTBOARD, None)
    continueFlag = True
    while continueFlag:
        if check(STARTBOARD, SOLVEDBOARD):
            continueFlag = False
        else:
            root.move('L')
            root.move('R')
            root.move('U')
            root.move('D')




if __name__ == '__main__':
    readFromFileToBoard()
    findField(STARTBOARD)
    root = Node(STARTBOARD,None)
    root.move('L')
    root.move('R')
    root.move('U')
    root.move('D')
