#! /usr/bin/env python3

import time


start_time = time.process_time()


def setup():
    with open('6-input.txt', 'r') as f:
        inp = f.read()
    return inp


def solve(parsed, part):
    marker_len = 4 if part == 1 else 14
    seen = []
    for i in range(len(parsed)):
        if parsed[i] in seen:
            seen[:''.join(seen).rindex(parsed[i]) + 1] = []
        seen.append(parsed[i])
        if len(seen) >= marker_len:
            print(f'Part {part}: {i + 1}')
            break


parsed = setup()
solve(parsed, 1)
solve(parsed, 2)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
