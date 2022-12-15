#! /usr/bin/env python3

import time


start_time = time.process_time()


def setup():
    with open('9-input.txt', 'r') as f:
        inp = [move.split(' ') for move in f.read().split('\n')[:-1]]
    dirs = [move[0] for move in inp]
    distances = [int(move[1]) for move in inp]
    return (dirs, distances)


def solve(parsed, part):
    knots = [[0, 0] for _ in range(2 if part == 1 else 10)]
    seen = [knots[-1].copy()]
    dirs = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    for i in range(len(parsed[0])):
        for _ in range(parsed[1][i]):
            # 1. Move the head
            head = knots[0]
            head[0] += dirs[parsed[0][i]][0]
            head[1] += dirs[parsed[0][i]][1]
            # 2. Move the tails
            for j in range(1, len(knots)):
                knot = knots[j]
                row_delta = head[0] - knot[0]
                col_delta = head[1] - knot[1]
                if abs(row_delta) == 2:
                    knot[0] += int(row_delta / 2)
                    if abs(col_delta) == 1:
                        knot[1] += col_delta
                if abs(col_delta) == 2:
                    knot[1] += int(col_delta / 2)
                    if abs(row_delta) == 1:
                        knot[0] += row_delta
                # 3. If the last tail has moved to a new space, add that space
                # to the seen list
                if j == len(knots) - 1:
                    if knot not in seen:
                        seen.append(knot.copy())
                head = knot
    print(f'Part {part}: {len(seen)}')


parsed = setup()
solve(parsed, 1)
solve(parsed, 2)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
