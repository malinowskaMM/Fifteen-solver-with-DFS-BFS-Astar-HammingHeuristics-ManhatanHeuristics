import numpy as np
import matplotlib.pyplot as plt


def avg(first, last, arr):
    result = arr[first: last]
    count = last - first + 1
    return np.sum(result)/count


def mapAvereges(arr):
    result = {}
    result[1] = avg(0, 1, arr)
    result[2] = avg(2, 5, arr)
    result[3] = avg(6, 15, arr)
    result[4] = avg(16, 39, arr)
    result[5] = avg(40, 93, arr)
    result[6] = avg(94, 200, arr)
    result[7] = avg(201, 412, arr)
    return result


def dataAlgo(filename):
    pathPrefix = 'WYNIKI/'
    my_data = np.genfromtxt(pathPrefix+filename, delimiter=',')
    moves = my_data[:, 1]
    visited = my_data[:, 2]
    processed = my_data[:, 3]
    depth = my_data[:, 4]
    time = my_data[:, 5]
    algo = {'moves': mapAvereges(moves)}
    algo['visited'] = mapAvereges(visited)
    algo['processed'] = mapAvereges(processed)
    algo['depth'] = mapAvereges(depth)
    algo['time'] = mapAvereges(time)
    return algo

# ---------------------- LOAD DATA INTO MAPS ----------------------

BFS_DRLU = dataAlgo('output_BFS_DRLU.csv')
BFS_DRUL = dataAlgo('output_BFS_DRUL.csv')
BFS_LUDR = dataAlgo('output_BFS_LUDR.csv')
BFS_LURD = dataAlgo('output_BFS_LURD.csv')
BFS_RDLU = dataAlgo('output_BFS_RDLU.csv')
BFS_RDUL = dataAlgo('output_BFS_RDUL.csv')
BFS_ULDR = dataAlgo('output_BFS_ULDR.csv')
BFS_ULRD = dataAlgo('output_BFS_ULRD.csv')

astar_hamm = dataAlgo('output_astar_hamm.csv')
astar_manh  = dataAlgo('output_astar_manh.csv')

DFS_DRLU = dataAlgo('output_DFS_DRLU.csv')
DFS_DRUL = dataAlgo('output_DFS_DRUL.csv')
DFS_LUDR = dataAlgo('output_DFS_LUDR.csv')
DFS_LURD = dataAlgo('output_DFS_LURD.csv')
DFS_RDLU = dataAlgo('output_DFS_RDLU.csv')
DFS_RDUL = dataAlgo('output_DFS_RDUL.csv')
DFS_ULDR = dataAlgo('output_DFS_ULDR.csv')
DFS_ULRD = dataAlgo('output_DFS_ULRD.csv')

# print(BFS_DRLU['moves'][3])

# ---------------------- PLOT GENERATION ----------------------

n_groups = 7

bar1 = []
for i in range(1, 8):
    bar1.append(astar_hamm['moves'][i])

bar2 = []
for i in range(1, 8):
    bar2.append(astar_manh['moves'][i])

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, bar1, bar_width,
alpha=opacity,
color='b',
label='Hamming')

rects2 = plt.bar(index + bar_width, bar2, bar_width,
alpha=opacity,
color='g',
label='Manhattan')

plt.xlabel('Pomieszanie planszy')
plt.ylabel('Ilość ruchów')
plt.title('Długość rozwiązania A*')
plt.xticks(index + bar_width, ('1', '2', '3', '4', '5', '6', '7'))
plt.legend()

plt.tight_layout()
plt.show()