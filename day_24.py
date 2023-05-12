#! /usr/bin/env python3

import time


start_time = time.process_time()


def setup():
    with open('24-input.txt', 'r') as f:
        # A list of tuples, each representing a blizzard: (y, x, dir)
        blizzards = []
        # Blizzard directions assigned as follows:
        #     1
        #   2╶┼╴0
        #     3
        dirs = ['>', '^', '<', 'v']
        lines = f.read().split('\n')[:-1]
        height = len(lines) - 2
        width = len(lines[0]) - 2
        for r, line in enumerate(lines):
            for c, char in enumerate(line):
                try:
                    blizzards.append((r, c, dirs.index(char)))
                except ValueError:
                    continue
    return blizzards, height, width


def solve(part, blizzards, height, width):
    # The starting position (the hole in the wall in the top left)
    start = (0, 1)
    # The ending position (the hole in the wall on the bottom left)
    end = (height + 1, width)
    # The ordered list of goals (depending on the part)
    goals = (end,) if part == 1 else (end, start, end)
    # How many goals we have completed (and the index of the current goal)
    completed = 0
    # The time counter
    minute = 0
    # Movement tuples corresponding to the four directions
    steps = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    # Set of possible positions for the expedition (originally only the
    # starting position)
    possible = {start}
    # Loop until goals are met
    while True:
        # Remove possible positions currently covered by a blizzard
        possible = trim_possible(possible, blizzards)
        # Check if any of the possible positions are adjacent to the current
        # goal. If so...
        if check_goal(possible, goals[completed]):
            # Add a minute to the clock to account for travelling to the
            # current goal
            minute += 1
            # If we just completed the final goal, end the simulation
            if completed >= len(goals) - 1:
                print(f'Part {part}: {minute}')
                return
            # Update the blizzards once to account for travelling to the
            # current goal
            blizzards = move_blizzards(blizzards, steps)
            # Reset the possible positions to the current goal tile
            possible = {goals[completed]}
            # Select the next goal
            completed += 1
        # Add adjacent possible positions
        possible = grow_possible(possible, steps)
        # Move the blizzards
        blizzards = move_blizzards(blizzards, steps)
        # Increment the time
        minute += 1

def check_goal(possible, goal):
    # Return true if one of the possible positions is directly above/below the
    # current goal, else false
    for pos in possible:
        if pos[1] == goal[1] and abs(pos[0] - goal[0]) <= 1:
            return True
    return False


def trim_possible(possible, blizzards):
    # Return the set of possible positions that are not currently occupied by a
    # blizzard
    blizzard_positions = {blizzard[:2] for blizzard in blizzards}
    return possible - blizzard_positions


def grow_possible(possible, steps):
    # Return a set of possible positions which has expanded to include adjacent
    # positions
    neighbors = set()
    for pos in possible:
        for step in steps:
            neighbor = (max(1, min(height, pos[0] + step[0])),
                        max(1, min(width, pos[1] + step[1])))
            neighbors.add(neighbor)
    return possible | neighbors


def move_blizzards(blizzards, steps):
    # Move each blizzard one step, according to its direction
    new_blizzards = []
    for blizzard in blizzards:
        step = steps[blizzard[2]]
        new = ((blizzard[0] + step[0] - 1) % height + 1,
               (blizzard[1] + step[1] - 1) % width + 1,
               blizzard[2])
        new_blizzards.append(new)
    return new_blizzards


blizzards, height, width = setup()
solve(1, blizzards.copy(), height, width)
solve(2, blizzards.copy(), height, width)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
