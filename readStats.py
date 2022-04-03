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

BFS = [BFS_DRLU, BFS_DRUL, BFS_LUDR, BFS_LURD, BFS_RDLU, BFS_RDUL, BFS_ULDR, BFS_ULRD]

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

DFS = [DFS_DRLU, DFS_DRUL, DFS_LUDR, DFS_LURD, DFS_RDLU, DFS_RDUL, DFS_ULDR, DFS_ULRD]

moveOrders = [['D', 'R', 'L', 'U'],
              ['D', 'R', 'U', 'L'],
              ['L', 'U', 'D', 'R'],
              ['L', 'U', 'R', 'D'],
              ['R', 'D', 'L', 'U'],
              ['R', 'D', 'U', 'L'],
              ['U', 'L', 'D', 'R'],
              ['U', 'L', 'R', 'D']]
labels = ['DRLU', 'DRUL', 'LUDR', 'LURD', 'RDLU', 'RDUL', 'ULDR', 'ULRD']
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', (0.3, 0.4, 0.2, 1)]
# ---------------------- PLOT GENERATION ----------------------


def bigPlots(algo, attribute):
    groupCount = 7

    bars = []
    for al in range(8):
        bar = []
        for i in range(1, 8):
            bar.append(algo[al][attribute][i])
        bars.append(bar)
    print(bars)

    fig, ax = plt.subplots()
    index = np.arange(groupCount)
    bar_width = 0.1
    opacity = 0.8

    for i in range(8):
        rects1 = plt.bar(index + i*bar_width, bars[i], bar_width,
        alpha=opacity,
        color=colors[i],
        label=labels[i])

    # plt.yscale("log")
    plt.xlabel('Stopień pomieszania planszy')
    plt.ylabel('Stany przetworzone')
    plt.title('Ilość stanów przetworzonych DFS')
    plt.xticks(index + bar_width, ('1', '2', '3', '4', '5', '6', '7'))
    plt.legend()

    plt.tight_layout()
    plt.show()

# bigPlots(DFS, 'processed')


# ------------------ PLOT ASTAR ------------------
# n_groups = 7
# attribute = 'processed'
#
# bar1 = []
# for i in range(1, 8):
#     bar1.append(astar_hamm[attribute][i])
#
# bar2 = []
# for i in range(1, 8):
#     bar2.append(astar_manh[attribute][i])
#
# # create plot
# # plt.yscale('log')
# fig, ax = plt.subplots()
# index = np.arange(n_groups)
# bar_width = 0.2
# opacity = 0.8
#
# rects1 = plt.bar(index, bar1, bar_width,
# alpha=opacity,
# color='b',
# label='Hamming')
#
# rects2 = plt.bar(index + bar_width, bar2, bar_width,
# alpha=opacity,
# color='g',
# label='Manhattan')
#
# plt.xlabel('Stopień pomieszania planszy')
# plt.ylabel('Stany przetworzone')
# plt.title('Liczba stanów przetworzonych A*')
# plt.xticks(index + bar_width, ('1', '2', '3', '4', '5', '6', '7'))
# plt.legend()
#
# plt.tight_layout()
# plt.show()

# ------------------ PLOT THREE ON ONE ------------------

n_groups = 7

attribute = 'visited'
bar1 = []
for i in range(1, 8):
    val = astar_hamm[attribute][i] + astar_manh[attribute][i]
    if val < 0:
        val = 0
    bar1.append(val/2)

bar2 = []
for i in range(1, 8):
    val = DFS_DRLU[attribute][i]+DFS_DRUL[attribute][i]+DFS_LUDR[attribute][i]+DFS_LURD[attribute][i]+DFS_RDLU[attribute][i]+DFS_RDUL[attribute][i]+DFS_ULDR[attribute][i]+DFS_ULRD[attribute][i]
    if val < 0:
        val = 0
    bar2.append(val/8)

bar3 = []
for i in range(1, 8):
    val = BFS_DRLU[attribute][i]+BFS_DRUL[attribute][i]+BFS_LUDR[attribute][i]+BFS_LURD[attribute][i]+BFS_RDLU[attribute][i]+BFS_RDUL[attribute][i]+BFS_ULDR[attribute][i]+BFS_ULRD[attribute][i]
    if val < 0:
        val = 0
    bar3.append(val/8)

# create plot
plt.yscale('log')
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.2
opacity = 0.8

rects1 = plt.bar(index, bar1, bar_width,
alpha=opacity,
color='b',
label='A*')

rects2 = plt.bar(index + bar_width, bar2, bar_width,
alpha=opacity,
color='g',
label='DFS')

rects3 = plt.bar(index + 2*bar_width, bar3, bar_width,
alpha=opacity,
color='r',
label='BFS')

plt.xlabel('Stopień pomieszania planszy')
plt.ylabel('Stany odwiedzone')
plt.title('Ilość stanów odwiedzonych ogółem')
plt.xticks(index + bar_width, ('1', '2', '3', '4', '5', '6', '7'))
plt.legend()

plt.tight_layout()
plt.show()