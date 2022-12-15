#! /usr/bin/env python3

import time


start_time = time.process_time()


def setup():
    shapes = (('A', 'B', 'C'), ('X', 'Y', 'Z'))
    with open('2-input.txt', 'r') as f:
        inp = [line.split(' ') for line in f.read().split('\n')[:-1]]
    # Convert from strings to ints (0 = rock, 1 = paper, or 2 = scissors)
    inp = [[shapes[round.index(move)].index(move) for move in round] for round in inp]
    return inp


def solve(parsed, part):
    total_score = 0
    for round in parsed:
        if part == 1:
            choice = round[1]
        else:
            choice = (round[0] + round[1] - 1) % 3
        win_score = 3 * ((choice - round[0] + 1) % 3)
        shape_score = choice + 1
        total_score += win_score + shape_score
    print(f'Part {part}: {total_score}')


parsed = setup()
solve(parsed, 1)
solve(parsed, 2)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
