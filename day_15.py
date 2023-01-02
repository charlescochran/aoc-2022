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

def solve_2(parsed):
    # Note: this algorithm does assume that the beacon location is not adjacent
    # to one of the edges of the search area and, as a result, is surrounded by
    # (at least) four different diamonds.

    # -- 1. Generate potential solutions --
    # This list will be populated with potential solutions
    potentials = []
    # A dict in which each key is an x-y tuple, denoting a position, and each
    # value is an integer, denoting the number of diamonds surrounding the
    # position
    pos_counts = {}
    # For each sensor-beacon pair...
    for pair in parsed:
        # Find the pair's Manhattan distance
        dist = abs(pair[2] - pair[0]) + abs(pair[3] - pair[1])
        # Create a set of x-y tuples containing all the border positions
        # (positions surrounding this pair's diamond)
        top_left_border = zip(range(pair[0] - dist - 1, pair[0] + 1),
                              range(pair[1], pair[1] - dist - 2, -1))
        bottom_left_border = zip(range(pair[0] - dist - 1, pair[0] + 1),
                                 range(pair[1], pair[1] + dist + 2))
        top_right_border = zip(range(pair[0], pair[0] + dist + 2),
                               range(pair[1] - dist - 1, pair[1] + 1))
        bottom_right_border = zip(range(pair[0], pair[0] + dist + 2),
                                  range(pair[1] + dist + 1, pair[1] - 1, -1))
        border = {*top_left_border, *bottom_left_border, *top_right_border, *bottom_right_border}
        # For each border position...
        for pos in border:
            # Increment the position's diamond count by one
            if pos in pos_counts:
                pos_counts[pos] += 1
                # If the count has reached four, this position is touching four
                # diamonds and could be the beacon location
                if pos_counts[pos] == 4:
                    potentials.append(pos)
            else:
                pos_counts[pos] = 1

    # -- 2. Check potential solutions --
    # For each potential solution...
    for pos in potentials:
        possible = True
        # For each sensor-beacon pair...
        for pair in parsed:
            dist = abs(pair[2] - pair[0]) + abs(pair[3] - pair[1])
            # If this pair excludes this position, move on to the next position
            if abs(pos[0] - pair[0]) + abs(pos[1] - pair[1]) <= dist:
                possible = False
                break
        # Since no pairs excluded this position, it is the solution
        if possible:
            # Calculate and print the tuning frequency
            print(f'Part 2: {pos[0] * 4000000 + pos[1]}')
            return


parsed = setup()
solve_1(parsed)
solve_2(parsed)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
