#! /usr/bin/env python3

import time
import numpy as np


start_time = time.process_time()


def setup():
    with open('17-input.txt', 'r') as f:
        jets = f.read().rstrip()
    shapes = np.array([[[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 1, 1, 1, 0]],
                       [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0]],
                       [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 1, 1, 1, 0, 0]],
                       [[0, 0, 1, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0]],
                       [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 1, 0, 0, 0],
                        [0, 0, 1, 1, 0, 0, 0]]])
    cave = np.ones((1, 7), dtype=int)
    return jets, shapes, cave


def is_valid(cave, rock):
    # Return False if the rock is overlapping any of the other rocks in the
    # cave
    return np.max(cave[:len(rock)] + rock) < 2


def trim_top(cave):
    # Remove empty rows from top of the cave
    trimmed = cave.copy()
    while np.sum(trimmed[0]) == 0:
        trimmed = np.delete(trimmed, 0, 0)
    return trimmed


def trim_bottom(cave):
    # Remove sealed-off rows from the bottom of the cave (also returning the number
    # of removed rows).
    trimmed = cave.copy()
    r = 0
    edges = [0, len(trimmed[0]) - 1]
    while True:
        increment = 1
        for dir in (1, -1):
            e = int(abs((dir - 1) / 2))
            if trimmed[r, edges[e]] == 1:
                if trimmed[r, edges[e] + dir] == 1:
                    edges[e] += dir
                    increment = 0
            elif edges[e] not in (0, len(trimmed[0]) - 1) and trimmed[r, edges[e] - dir] == 0:
                edges[e] -= dir
                increment = 0
        if edges[0] >= edges[1]:
            break
        r += increment
    num_trimmed = len(trimmed) - r - 1
    trimmed = trimmed[:r + 1]
    return trimmed, num_trimmed


def solve(jets, shapes, cave, part):
    num_rocks = 2022 if part == 1 else 1000000000000
    num_rocks_done = 0
    ticks = 0
    num_extra_rows = 0
    tick_wraps = []
    cycle_detected = False
    while num_rocks - num_rocks_done > 0:
        # Trim the cave, keeping track of rows trimmed from the bottom
        cave, num_trimmed_bottom = trim_bottom(trim_top(cave))
        num_extra_rows += num_trimmed_bottom
        # Add 7 empty rows on top
        cave = np.vstack((np.zeros((7, 7), dtype=int), cave))
        # Create a new rock
        rock = shapes[num_rocks_done % len(shapes)].copy()
        # Move the rock until it comes to rest
        while True:
            # In part 2, try to detect a cycle
            if part == 2 and not cycle_detected and ticks % len(jets) == 0:
                height = len(trim_top(cave)) - 1 + num_extra_rows
                for tick_wrap in tick_wraps:
                    # If we've seen this shape at the beginning of a previous
                    # tick loop, we've identified a cycle
                    if np.array_equal(rock, tick_wrap[2]):
                        rocks_per_cycle = num_rocks_done - tick_wrap[0]
                        height_per_cycle = height - tick_wrap[1]
                        num_cycles = int((num_rocks - num_rocks_done + 1) / rocks_per_cycle)
                        # Increment the extra rows by the appropriate amount
                        # and skip most of the rest of the rocks
                        num_extra_rows += num_cycles * height_per_cycle
                        num_rocks_done += num_cycles * rocks_per_cycle
                        cycle_detected = True
                        break
                if not cycle_detected:
                    tick_wraps.append((num_rocks_done, height, rock))
            # Handle jetstream movements
            pushed = None
            if jets[ticks % len(jets)] == '>':
                if np.sum(rock[:, -1]) == 0:
                    pushed = np.hstack((np.zeros((len(rock), 1), dtype=int), rock[:, :-1]))
            else:
                if np.sum(rock[:, 0]) == 0:
                    pushed = np.hstack((rock[:, 1:], np.zeros((len(rock), 1), dtype=int)))
            if pushed is not None and is_valid(cave, pushed):
                rock = pushed
            ticks += 1
            # Handle gravity movements
            fallen = np.vstack((np.zeros((1, 7), dtype=int), rock))
            if is_valid(cave, fallen):
                rock = fallen
            else:
                # Rock has come to rest
                cave[:len(rock)] += rock
                num_rocks_done += 1
                break
    print(f'Part {part}: {len(trim_top(cave)) - 1 + num_extra_rows}')


parsed = setup()
solve(parsed[0], parsed[1], parsed[2].copy(), 1)
solve(parsed[0], parsed[1], parsed[2].copy(), 2)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
