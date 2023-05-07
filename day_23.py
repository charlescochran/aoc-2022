#! /usr/bin/env python3

import time
import re


start_time = time.process_time()


def setup():
    with open('23-input.txt', 'r') as f:
        positions = []
        lines = f.read().split('\n')[:-1]
        for r, line in enumerate(lines):
            cols = [m.start() for m in re.finditer('#', line)]
            rows = [r] * len(cols)
            positions.extend(zip(rows, cols))
    # Return a list of tuples, where each tuple stores the (y, x) position of
    # each # in the input data (relative to the top left)
    return positions


def solve(positions, part):
    # Note: neighbors are given in the following order. This order seems
    # strange, but it allows the dir_map below to specify the three indices of
    # each direction using a single slice object while also ensuring that the
    # adjacent position to the middle is the highest index in each group of
    # three.
    #   0 2 1
    #   6╶┼╴7
    #   3 5 4
    #
    # Tuple mapping each neighbor's index to its (y, x) step
    neighbor_steps = ((-1, -1), (-1, 1), (-1, 0), (1, -1), (1, 1), (1, 0), (0, -1), (0, 1))
    # Dict mapping dirs to their corresponding neighbor indices (as slice objects)
    dir_map = {'N': slice(0, 3),
               'S': slice(3, 6),
               'W': slice(0, 7, 3),
               'E': slice(1, 8, 3)}
    # The starting order of the directions
    dirs = ['N', 'S', 'W', 'E']

    round = 1
    # Loop until the simulation is finished
    while True:
        # -- Planning phase --
        planned = positions.copy()
        # For each position
        for i, pos in enumerate(positions):
            # Find out which neighboring positions already have elves
            neighbors = [tuple(map(sum, zip(step, pos))) for step in neighbor_steps]
            filled_neighbors = [neighbor in positions for neighbor in neighbors]
            # If all neighbors are empty, do nothing
            if not any(filled_neighbors):
                continue
            # Otherwise, try each direction, in order
            for dir in dirs:
                # If all three spaces in that direction are empty
                if not any(filled_neighbors[dir_map[dir]]):
                    # Plan a move to the appropriate adjacent neighbor
                    planned[i] = neighbors[dir_map[dir]][2]
                    break
        # In part 2, end the simulation if no elf wants to move
        if part == 2 and planned == positions:
            print(f'Part 2: {round}')
            return
        # -- Moving phase --
        # For each planned position
        for i, pos in enumerate(planned):
            # If this position was only planned once, move there
            if planned.count(pos) == 1:
                positions[i] = pos
        # -- Round end --
        # Move the first dir to the end of the list
        dirs.append(dirs.pop(0))
        # Increment the round counter
        round += 1
        # In part 1, break if end of tenth round
        if part == 1 and round > 10:
            break
    # In part 1, count the number of empty spaces in the bounding rectangle
    x_coords = [pos[0] for pos in positions]
    y_coords = [pos[1] for pos in positions]
    width = max(x_coords) - min(x_coords) + 1
    height = max(y_coords) - min(y_coords) + 1
    empty_positions = width * height - len(positions)
    print(f'Part 1: {empty_positions}')


parsed = setup()
solve(parsed.copy(), 1)
solve(parsed.copy(), 2)
# Note: Part 2 takes about 15 min on my input.

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
