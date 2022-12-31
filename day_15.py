#! /usr/bin/env python3

import time
import re


start_time = time.process_time()


def setup():
    with open('15-input.txt', 'r') as f:
        inp = f.read()
    pairs = re.findall('Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), '
                       'y=(-?[0-9]+)\n', inp)
    pairs = [tuple(map(int, val)) for val in pairs]
    return pairs  # Format: [(sensor x, sensor y, beacon x, beacon y), ...]


def solve_1(parsed):
    # Harvest all of the x coordinates from the input
    x_coords = [pair[i] for pair in parsed for i in (0, 2)]
    # This value is added any position's calculated x coordinate before storing
    # it in the row
    x_adj = -min(x_coords)
    # The width of the row
    num_cols = x_adj + max(x_coords) + 1
    # The y coordinate of the row, specified by the problem
    r = 2000000
    # Start by assuming beacons are everywhere in the row
    row = [1] * num_cols
    # For each sensor-beacon pair...
    for pair in parsed:
        # Find the Manhattan distance
        dist = abs(pair[2] - pair[0]) + abs(pair[3] - pair[1])
        # Calculate the width of the no-beacon strip in the row
        width = 2 * (dist - abs(pair[1] - r)) + 1
        if width > 0:
            # Find the starting x coordinate of the no-beacon strip
            c = pair[0] + x_adj - int((width - 1) / 2)
            # If needed, add extra columns to the row (prepending and/or
            # appending as necessary)
            prepend_cols = max(-c, 0)
            if prepend_cols > 0:
                x_adj += prepend_cols
                c = 0
                row = [1] * prepend_cols + row
            append_cols = max(c + width - len(row), 0)
            if append_cols > 0:
                row = row + [1] * append_cols
            # Set the no-beacon strip in the row to 0s
            row[c:c + width] = [0] * width
        # If the nearest beacon is the row, reset its location to a 1
        if pair[3] == r:
            row[pair[2] + x_adj] = 1
    # The answer is the number of 0s in the row (representing no-beacon
    # locations)
    print(f'Part 1: {len(row) - sum(row)}')


parsed = setup()
solve_1(parsed)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
