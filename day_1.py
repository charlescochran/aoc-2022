#! /usr/bin/env python3

import time


start_time = time.process_time()


def setup():
    with open('1-input.txt', 'r') as f:
        inp = f.read().split('\n\n')
    inp = [elf.split('\n') for elf in inp]
    # Remove extra empty string from the final elf's calorie list
    inp[-1].pop()
    inp = [list(map(int, elf)) for elf in inp]
    return inp


def solve(parsed):
    top_cals = [0, 0, 0]
    for elf in parsed:
        elf_cals = sum(elf)  # type: ignore
        if elf_cals > top_cals[0]:
            top_cals.append(elf_cals)
            top_cals.pop(0)
            top_cals = sorted(top_cals)
    print(f'Part 1: {top_cals[2]}')
    print(f'Part 2: {sum(top_cals)}')


parsed = setup()
solve(parsed)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
