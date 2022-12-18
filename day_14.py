#! /usr/bin/env python3

import time
import numpy as np
import os


start_time = time.process_time()


def setup(viz=True):
    with open('14-input.txt', 'r') as f:
        inp = [[[int(coord)
                 for coord in coords.split(',')]
                for coords in path.split(' -> ')]
               for path in f.read().split('\n')[:-1]]
    height = max([coord[1] for path in inp for coord in path]) + 3
    # The cave array's width is based on its height, such that it is just wide
    # enough to contain all the sand units in part 2
    cave = np.full((height, (2 * height) - 1), '.')
    start_x = 500
    x_adj = height - start_x - 1
    # Add the walls
    for path in inp:
        for i in range(len(path) - 1):
            x_vals = sorted((path[i][0] + x_adj, path[i + 1][0] + x_adj))
            y_vals = sorted((path[i][1], path[i + 1][1]))
            cave[y_vals[0]:y_vals[1] + 1, x_vals[0]:x_vals[1] + 1] = ['#']
    # Add the floor
    cave[-1, :] = ['#']
    start_coord = (0, start_x + x_adj)
    return (cave, start_coord)


def solve(cave, start_coord, part):
    # This could definitely be optimized more (i.e. don't start each bit of
    # sand from the top), but in its current form vizualization is simple.
    resting_sand = 0
    try:
        while True:
            sand_coord = start_coord
            while True:
                old_coord = sand_coord
                if cave[sand_coord[0] + 1, sand_coord[1]] == '.':
                    sand_coord = (sand_coord[0] + 1, sand_coord[1])
                elif cave[sand_coord[0] + 1, sand_coord[1] - 1] == '.':
                    sand_coord = (sand_coord[0] + 1, sand_coord[1] - 1)
                elif cave[sand_coord[0] + 1, sand_coord[1] + 1] == '.':
                    sand_coord = (sand_coord[0] + 1, sand_coord[1] + 1)
                else:
                    resting_sand += 1
                    if part == 2 and sand_coord == start_coord:
                        raise IndexError
                    break
                if part == 1 and sand_coord[0] == len(cave) - 2:
                    raise IndexError
                cave[old_coord] = '.'
                cave[sand_coord] = 'o'
    except IndexError:
        pass
    print(f'Part {part}: {resting_sand}')


parsed = setup()
solve(parsed[0].copy(), parsed[1], 1)
solve(parsed[0].copy(), parsed[1], 2)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
