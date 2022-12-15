#! /usr/bin/env python3

import time


start_time = time.process_time()


def setup():
    with open('4-input.txt', 'r') as f:
        inp = f.read().split('\n')[:-1]
    pairs = [[[int(num) for num in section.split('-')]
                        for section in pair.split(',')]
                        for pair in inp]
    return pairs


def solve_1(parsed):
    num_contained = 0
    for pair in parsed:
        for i in range(2):
            if (pair[i][0] <= pair[(i + 1) % 2][0] and pair[i][1] >= pair[(i + 1) % 2][1]):
                num_contained += 1
                break
    print(f'Part 1: {num_contained}')


def solve_2(parsed):
    num_overlaps = 0
    for pair in parsed:
        if pair[0][0] <= pair[1][1] and pair[1][0] <= pair[0][1]:
            num_overlaps += 1
    print(f'Part 2: {num_overlaps}')


parsed = setup()
solve_1(parsed)
solve_2(parsed)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
