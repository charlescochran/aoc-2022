#! /usr/bin/env python3

import time
import numpy as np


start_time = time.process_time()


def setup():
    with open('8-input.txt', 'r') as f:
        inp = np.array([[int(col) for col in row] for row in f.read().split('\n')[:-1]])
    return inp


def solve_1(parsed):
    # Initialize num_visible with the number of trees on the outside
    num_visible = 2 * len(parsed) + 2 * len(parsed[0]) - 4
    for c in range(1, len(parsed) - 1):
        for r in range(1, len(parsed[0]) - 1):
            max_heights = (max(parsed[:r, c]),      # N
                           max(parsed[r + 1:, c]),  # S
                           max(parsed[r, :c]),      # W
                           max(parsed[r, c + 1:]))  # E
            for height in max_heights:
                if height < parsed[r, c]:
                    num_visible += 1
                    break
    print(f'Part 1: {num_visible}')


def solve_2(parsed):
    max_score = 0
    for c in range(len(parsed)):
        for r in range(len(parsed[0])):
            scores = [0, 0, 0, 0]
            tree_ranges = (np.flip(parsed[:r, c]),  # N
                           parsed[r + 1:, c],       # S
                           np.flip(parsed[r, :c]),  # W
                           parsed[r, c + 1:])       # E
            for i in range(len(tree_ranges)):
                for height in tree_ranges[i]:
                    scores[i] += 1
                    if height >= parsed[r, c]:
                        break
            max_score = max((max_score, scores[0] * scores[1] * scores[2] * scores[3]))
    print(f'Part 2: {max_score}')


parsed = setup()
solve_1(parsed)
solve_2(parsed)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
