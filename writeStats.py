import main as m
from os import listdir
import time
import cProfile

m.ORDER = ['L', 'U', 'R', 'D']

inputPath = 'F:\Studia\sem4\SISE\Projekt_SISE\puzzles'
outputFilename = 'F:\Studia\sem4\SISE\Projekt_SISE\output_BFS_LURD.csv'
inputFiles = listdir(inputPath)

outputFile = open(outputFilename, 'a')
counter = 0
for inputFile in inputFiles:
    counter += 1
    m.STARTBOARD = []
    m.STARTBOARD = m.readFromFileToBoard('puzzles/'+inputFile)
    m.BLANK = m.findZero(m.STARTBOARD)
    root = m.Node(m.STARTBOARD)

    solution = m.bfs(root)
    wayLen = len(solution[1])
    visitedStatesCount = solution[2]
    processedStatesCount = solution[3]
    depth = solution[4]
    elapsedTime = "{:.3f}".format(solution[5] / 1000000)

    line = f'{inputFile},{wayLen},{visitedStatesCount},{processedStatesCount},{depth},{elapsedTime}'
    outputFile.write(line)
    outputFile.write('\n')
    print("Rozwiązanych plansz:", counter)

outputFile.close()

