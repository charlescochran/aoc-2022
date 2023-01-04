#! /usr/bin/env python3

import time
import sys


sys.setrecursionlimit(7500)
start_time = time.process_time()


def setup():
    with open('18-input.txt', 'r') as f:
        inp = [eval(line) for line in f.read().split('\n')[:-1]]
    return inp


def get_neighbors(cube):
    neighbors = [(cube[0] + 1, cube[1], cube[2]),
                 (cube[0] - 1, cube[1], cube[2]),
                 (cube[0], cube[1] + 1, cube[2]),
                 (cube[0], cube[1] - 1, cube[2]),
                 (cube[0], cube[1], cube[2] + 1),
                 (cube[0], cube[1], cube[2] - 1)]
    return neighbors


def explore(cube, parsed, bounds, blacklist):
    blacklist.append(cube)
    surface_area = 0
    # For each of the six neighbors...
    for neighbor in get_neighbors(cube):
        # If we have previously explored the neigbor, skip it
        if neighbor in blacklist:
            continue
        try:
            # If the neighbor is outside the search-space boundary, skip it
            for i in range(3):
                if neighbor[i] < bounds[i][0] or neighbor[i] > bounds[i][1]:
                    raise IndexError
        except IndexError:
            continue
        # If the neighbor is a filled space, add one to the surface area
        if neighbor in parsed:
            surface_area += 1
        # Otherwise, the neighbor is empty, so recursively explore it
        else:
            surface_area += explore(neighbor, parsed, bounds, blacklist)
    # Return the surface area, contributed to by this exploration and all
    # explorations caused by this one
    return surface_area


def solve_2(parsed):
    # Convert input coordinate format from
    # [(x1, y1, z1), (x2, y2, z2), ...]
    # to
    # [(x1, x2, ...), (y1, y2, ...), (z1, z2, ...)]
    dimensions = list(zip(*parsed))
    # Calculate the rectangular search-space boundary based on the min and max
    # coordinates in each of three dimensions, adding an en extra layer around
    # the perimeter
    bounds = [(min(dimension) - 1, max(dimension) + 1) for dimension in dimensions]
    # Start at the first corner, which will be an empty space
    start_coord = [bound[0] for bound in bounds]
    # Calculate the outer surface area using recursion
    surface_area = explore(start_coord, parsed, bounds, [])
    print(f'Part 2: {surface_area}')


def solve_1(parsed):
    surface_area = 0
    # For each cube in the input...
    for cube in parsed:
        # Add the number of non-contacted sides this cube has to the total
        # surface area
        surface_area += 6 - sum([neighbor in parsed for neighbor in
                                 get_neighbors(cube)])
    print(f'Part 1: {surface_area}')


parsed = setup()
solve_1(parsed)
solve_2(parsed)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
