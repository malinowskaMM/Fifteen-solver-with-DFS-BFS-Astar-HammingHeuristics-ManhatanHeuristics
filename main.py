import random

model_matrix = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 0]]


def generate_random_matrix():
    list_of_numbers = list(range(0, 16))
    random.shuffle(list_of_numbers)
    matrix = [list_of_numbers[0:4], list_of_numbers[4:8], list_of_numbers[8:12], list_of_numbers[12:16]]
    return matrix


def check_valid(matrix):
    if matrix == model_matrix:
        return True
    else:
        return False


print(generate_random_matrix())
