#! /usr/bin/env python3

import time
import numpy as np
import re


start_time = time.process_time()


def setup():
    with open('5-input.txt', 'r') as f:
        inp = f.read().split('\n\n')
    crate_rows = inp[0].split('\n')[:-1]
    crates = np.zeros((int(len(crate_rows)), int((len(crate_rows[0]) + 1) / 4)), dtype='str')
    for row in range(len(crate_rows)):
        for col in range(len(crate_rows[row])):
            char = crate_rows[row][col]
            ascii = ord(char)
            if ascii in range(65, 91):
                crates[row, int((col - 1) / 4)] = char
    instructions = inp[1].split('\n')[:-1]
    plan = [list(map(int, filter(None, re.split('move | from | to ', line))))
            for line in instructions]
    return (crates, plan)


def solve(parsed, part):
    # Note: this solution is kind of overkill, as it involves literally moving
    # the crates around a 2D numpy array. It makes visualization easy, but it
    # is quite slow and it probably would have been much easier to just use a
    # list of lists and pop()/append()!
    crates = parsed[0].copy()
    plan = parsed[1]
    for instruction in plan:
        # -- 1. Copy and delete old crates --
        copy_row = find_first_crate_row(crates, instruction[1] - 1)
        copy = crates[copy_row:copy_row + instruction[0], instruction[1] - 1].copy()
        crates[copy_row:copy_row + instruction[0], instruction[1] - 1] = ['']
        # Reverse the copy in part 1
        if part == 1:
            copy = copy[::-1]
        # -- 2. Paste --
        first_crate_row = find_first_crate_row(crates, instruction[2] - 1)
        if len(copy) > first_crate_row:
            # We need to add row(s) to accomadate the whole paste
            crates = np.r_[np.zeros((len(copy) - first_crate_row, len(crates[0])), dtype=str),
                           crates]
            paste_row = 0
        else:
            paste_row = first_crate_row - len(copy)
        crates[paste_row:paste_row + instruction[0], instruction[2] - 1] = copy
    message = ''
    for col in np.transpose(crates):
        for crate in col:
            if crate:
                message = message + crate
                break
    print(f'Part {part}: The message is {message}.')


def find_first_crate_row(crates, col):
    for row in range(len(crates)):
        if crates[row, col]:
            return row
    # Stack is empty, so return the index of the non-existent row after the last one
    return len(crates)


parsed = setup()
solve(parsed, 1)
solve(parsed, 2)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
