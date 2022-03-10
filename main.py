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
    else:
        return False

counter = 0
def createTree(root):
    while counter < 20:
        root.move('L')


class Node:
    def __init__(self, board, parent, birthMove):
        self.board = board
        self.isBoardCorrect = check(self.board, SOLVEDBOARD)
        # self.children = []
        self.childLeft = None
        self.childRight = None
        self.childUp = None
        self.childDown = None
        if parent is not None:  # None is reserved for ROOT node
            self.parent = parent
            self.birthMove = birthMove

    def makeChild(self, board, move):
        child = Node(board, self, move)
        return child
        # self.children.append(child)

    def move(self, move):
        yPos = BLANK['row']
        xPos = BLANK['col']
        if move == 'L':
            if xPos == 0:
                return 0        # Ending branch on left
            BLANK['col'] -= 1
            tempBoard = self.board
            tempBoard[yPos][xPos] = tempBoard[yPos][xPos-1]
            tempBoard[yPos][xPos-1] = '0'
            print(tempBoard)
            self.childLeft = self.makeChild(tempBoard, move)
            return self.childLeft
        if move == 'R':
            if xPos == 3:
                return 0        # Ending branch on right
            BLANK['col'] += 1
            tempBoard = self.board
            tempBoard[yPos][xPos] = tempBoard[yPos][xPos+1]
            tempBoard[yPos][xPos+1] = '0'
            print(tempBoard)
            self.childRight = self.makeChild(tempBoard, move)
            return self.childRight
        if move == 'U':
            if yPos == 3:
                return 0        # Ending branch up
            BLANK['row'] -= 1
            tempBoard = self.board
            tempBoard[yPos][xPos] = tempBoard[yPos-1][xPos]
            tempBoard[yPos-1][xPos] = '0'
            print(tempBoard)
            self.childUp = self.makeChild(tempBoard, move)
            return self.childDown
        if move == 'D':
            if yPos == 0:
                return 0        # Ending branch down
            BLANK['row'] += 1
            tempBoard = self.board
            tempBoard[yPos][xPos] = tempBoard[yPos+1][xPos]
            tempBoard[yPos+1][xPos] = '0'
            print(tempBoard)
            self.childDown = self.makeChild(tempBoard, move)
            return self.childDown


def DFS(node):
    # node.visited = True
    if node != 0:
        if not node.isBoardCorrect:
            DFS(node.move('L'))
            DFS(node.move('R'))
            DFS(node.move('U'))
            DFS(node.move('D'))


# counter = 0
# def createTree(root):
#     while counter < MAXDEPTH:



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
    root = Node(STARTBOARD, None, None)
    DFS(root)
    # root.move('L')
    # root.move('R')
    # root.move('U')
    # root.move('D')
