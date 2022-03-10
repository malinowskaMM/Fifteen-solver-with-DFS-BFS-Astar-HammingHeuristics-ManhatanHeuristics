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
        if parent is not None:  # None is reserved for ROOT node
            self.parent = parent

    def makeChild(self, board, move):
        child = Node(board, self)

    def move(self, move):
        yPos=BLANK['row']
        xPos=BLANK['col']
        if move == 'L':
            BLANK['col'] -= 1
            temp = self.board
            temp[yPos][xPos] = temp[yPos][xPos-1]
            temp[yPos][xPos-1] = '0'
            print(temp)
            self.makeChild(temp, move)
        if move == 'P':
            BLANK['col'] += 1
            temp = self.board
            temp[yPos][xPos] = temp[yPos][xPos+1]
            temp[yPos][xPos+1] = '0'
            print(temp)
            self.makeChild(temp, move)
        if move == 'U':
            BLANK['row'] -= 1
            temp = self.board
            temp[yPos][xPos] = temp[yPos-1][xPos]
            temp[yPos-1][xPos] = '0'
            print(temp)
            self.makeChild(temp, move)
        if move == 'D':
            BLANK['row'] += 1
            temp = self.board
            temp[yPos][xPos] = temp[yPos+1][xPos]
            temp[yPos+1][xPos] = '0'
            print(temp)
            self.makeChild(temp, move)




if __name__ == '__main__':
    readFromFileToBoard()
    findField(STARTBOARD)
    root = Node(STARTBOARD,None)
    root.move('L')
    root.move('P')
    root.move('U')
    root.move('D')
