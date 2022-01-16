import copy
import random
from multiprocessing import Pool

import game_min

def calcFitness(game):
    height = [0 for i in range(5)]
    for i in range(5):
        j = 0
        while j <= 5 and game.grid[j][i] == -1:
            j += 1
        height[i] = j
    # print(min(height), end="")
    # don't want small numbers in bottom layer
    # low_cnt = 0
    # for i in range(5):
    #     if game.grid[5][i] < game.lowestBlockHeight + 4:
    #         low_cnt += 1
    return (min(height) + 5) ** 3

def simulate_with_set_value(game: game_min.Main, move_1, move_2, move_num):
    fitness_arr = [[0 for i in range(5)] for j in range(5)]
    for loc1 in range(5):
        for loc2 in range(5):
            game_copy = copy.deepcopy(game)
            game_copy.appendblock(loc1, move_1)
            game_copy.appendblock(loc2, move_2)
            # print(loc1, loc2, end=": ")
            fitness_arr[loc1][loc2] = simulate_with_value(game_copy, move_num)
            # print()
    max_fitness = [max(i) for i in fitness_arr]
    return max_fitness.index(max(max_fitness))

def simulate_with_value(game: game_min.Main, move_num):
    if not game.alive:
        return 0
    if move_num == 0:
        return calcFitness(game)

    fitness = 0
    for block_value in range(min(game.greatestBlockHeight - 10, game.lowestBlockHeight), game.greatestBlockHeight - 6):
        # print(block_value, end="{")
        for location in range(5):
            game_copy = copy.deepcopy(game)
            game_copy.appendblock(location, block_value)
            fitness += simulate_with_value(game_copy, move_num - 1)
        # print("}", end=" ")
    return fitness

def calculate_move(game, queue):
    return simulate_with_set_value(game, queue[0], queue[1], 1)

def simulate_game(this_variable_is_definitely_not_used=None):
    game = game_min.Main()
    queue = [1, 1]
    while game.alive:
        queue = [queue[1], random.randint(min(game.greatestBlockHeight - 10, game.lowestBlockHeight), game.greatestBlockHeight - 6)]
        game.appendblock(calculate_move(game, queue), queue[0])
    return game.score


def main():
    with Pool(6) as p:
        points = p.map(simulate_game, [None for i in range(7)])
        avg = 0
        for i in points:
            avg += i / 6
        print(points, avg)




if __name__ == '__main__':
    main()
