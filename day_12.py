#! /usr/bin/env python3

import time
import numpy as np
import math
import sys

sys.setrecursionlimit(3000)
start_time = time.process_time()


def setup():
    with open('12-input.txt', 'r') as f:
        inp = np.array([[ord(char) for char in line] for line in f.read().split('\n')[:-1]])
        cur = tuple([index[0] for index in np.where(inp == 83)])
        goal = tuple([index[0] for index in np.where(inp == 69)])
        inp[cur] = 97
        inp[goal] = 122
    return (inp, cur, goal)


def explore(cur, blacklist=[]):
    # This is not a particularly efficient solution (~100 s). Something like
    # Dijkstra would be faster, but I wanted to write it more or less from
    # scratch instead of looking up the answer.
    global heights
    global steps_map
    global shortest_path_steps
    if cur in steps_map:
        steps_map[cur] = min(steps_map[cur], len(blacklist))
    else:
        steps_map[cur] = len(blacklist)
    # The current elevation is the lowest, so potentially update the shortest
    # path accordingly (this if for part 2)
    if heights[cur] == 97:
        shortest_path_steps = min(shortest_path_steps, steps_map[cur])
    blacklist.append(cur)
    for neighbor in ((cur[0] - 1, cur[1]),   # N
                     (cur[0], cur[1] + 1),   # E
                     (cur[0] + 1, cur[1]),   # S
                     (cur[0], cur[1] - 1)):  # W
        # Skip this neighbor because it is in the blacklist
        if neighbor in blacklist:
            continue
        # Skip this neighbor because it already has an equal/shorter path to the goal
        if neighbor in steps_map and steps_map[neighbor] <= steps_map[cur] + 1:
            continue
        # Skip this neighbor because it doesn't exist
        if neighbor[0] not in range(len(parsed[0])) or neighbor[1] not in range(len(parsed[0][0])):
            continue
        # Skip this neighbor because it is too low
        if heights[neighbor] < heights[cur] - 1:
            continue
        explore(neighbor, blacklist.copy())


def solve(parsed):
    global heights
    global steps_map
    global shortest_path_steps
    heights = parsed[0]
    steps_map = {}
    shortest_path_steps = math.inf
    # Start the exploration from the goal
    explore(parsed[2])
    print(f'Part 1: {steps_map[parsed[1]]}')
    print(f'Part 2: {shortest_path_steps}')


parsed = setup()
solve(parsed)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
