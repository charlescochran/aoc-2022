#! /usr/bin/env python3

import time
import numpy as np


start_time = time.process_time()


def setup():
    with open('10-input.txt', 'r') as f:
        inp = [instruction.split(' ') for instruction in f.read().split('\n')[:-1]]
    return inp


def solve(parsed):
    score = 0
    screen = np.full((6, 40), '.', dtype=str)
    vals_to_add = [0, 0]
    x = 1
    i = 0
    while True:
        render_pos = (int(i / 40), i % 40)
        val_to_add = 0
        if not parsed[i][0] == 'noop':
            val_to_add = int(parsed[i][1])
            parsed.insert(i + 1, ['noop'])
        vals_to_add.append(val_to_add)
        x += vals_to_add.pop(0)
        if (i + 21) % 40 == 0:
            score += (i + 1) * x
        if abs(render_pos[1] - x) < 2:
            screen[render_pos[0], render_pos[1]] = '#'
        i += 1
        if i == len(parsed):
            break
    print(f'Part 1: {score}')
    with np.printoptions(linewidth=1000, formatter={'numpystr':lambda x: x}):  # type: ignore
        print(f'Part 2:\n{screen}')

parsed = setup()
solve(parsed)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
