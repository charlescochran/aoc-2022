#! /usr/bin/env python3

import time
import numpy as np
import re


start_time = time.process_time()


def setup():
    with open('22-input.txt', 'r') as f:
        inp = f.read().split('\n\n')
    board_lines = inp[0].split('\n')
    width = 150
    height = 200
    # Create the board, a 2D np array with the ascii values of each character
    board = np.array([[ord(char) for char in line.ljust(width, ' ')] for line
                      in board_lines])
    # Surround the board by a "frame" of spaces. This is to make wrap detection
    # easier.
    empty_col = np.full((height, 1), 32)
    empty_row = np.full((1, width + 2), 32)
    board = np.hstack((empty_col, board, empty_col))
    board = np.vstack((empty_row, board, empty_row))

    # Parse the path description, creating a tuple of instructions, where each
    # is a tuple with a distance and a -1 or 1 denoting a left or right turn,
    # respectively
    matches = re.findall(r'\d+|[RL]', inp[1])
    dists = []
    turns = []
    for match in matches:
        if match.isdigit():
            dists.append(int(match))
        else:
            turns.append(-1 if match == 'L' else 1)
    turns.append(0)

    return board, tuple(zip(dists, turns))


def solve(part, board, instructions):
    # Tuple to map each facing to a unit vector pointing that direction
    steps = ((1, 0), (0, 1), (-1, 0), (0, -1))
    # Find the starting position and facing
    pos = [board[1].tolist().index(46), 1]
    facing = 0
    # Carry out each instruction
    for instruction in instructions:
        # print(f'instruction: {instruction}')
        pos, facing = move(part, board, pos, facing, instruction, steps)
    # Display the final password
    print(f'Part {part}: {1000 * pos[1] + 4 * pos[0] + facing}')


def move(part, board, pos, facing, instruction, steps):
    cur_pos = pos.copy()
    cur_facing = facing
    # Loop N times, where N is the distance component of this instruction
    for _ in range(instruction[0]):
        # Identify the next tile we would move to
        next_pos = cur_pos.copy()
        next_facing = cur_facing
        next_pos[0] = next_pos[0] + steps[cur_facing][0]
        next_pos[1] = next_pos[1] + steps[cur_facing][1]
        next_tile = board[next_pos[1], next_pos[0]]
        # If the next tile is a space, apply the appropriate wrap and treat
        # that as the next tile instead
        if next_tile == 32:
            next_pos, next_facing = wrap(part, board, next_pos, next_facing, steps)
            next_tile = board[next_pos[1], next_pos[0]]
        # If the (new) next tile is a wall, stop before moving to it
        if next_tile == 35:
            break
        # Otherwise, it's a period, so move there
        cur_pos = next_pos
        cur_facing = next_facing
    # Return the latest position and the latest facing, with the instructed turn applied
    return cur_pos, (cur_facing + instruction[1]) % 4


def wrap(part, board, pos, facing, steps):
    cur_pos = pos.copy()
    cur_facing = facing
    # In part 1, wrap by simply moving forward (and screen-wrapping) until you
    # reach a tile that exists.
    if part == 1:
        # Move foward until this tile isn't a space
        while board[cur_pos[1], cur_pos[0]] == 32:
            cur_pos[0] = (cur_pos[0] + steps[cur_facing][0]) % board.shape[1]
            cur_pos[1] = (cur_pos[1] + steps[cur_facing][1]) % board.shape[0]
        return cur_pos, cur_facing
    # In part 2, wrap by moving between faces on the cube.
    # Note: I originally thought about designing a generic cube folder, but I
    # realized that this would be very difficult. In addition, I discovered
    # that Eric made all the inputs have the same shape, so hard-coding this
    # shape doesn't seem that bad.
    #
    #       ┌─A1─┬─B1─┐
    #       C1   │   D1
    #       ├────┼─E1─┘
    #       F1  E2
    #  ┌─F2─┼────┤
    #  C2   │   D2
    #  ├────┼─G1─┘
    #  A2  G2
    #  └─B2─┘
    else:
        # Tuples of the edges forming the border *around* the valid board
        # positions
        A1 = tuple(zip(range(51, 101),  [0] * 50))
        A2 = tuple(zip([0] * 50,        range(151, 201)))
        B1 = tuple(zip(range(101, 151), [0] * 50))
        B2 = tuple(zip(range(1, 51),    [201] * 50))
        C1 = tuple(zip([50] * 50,       range(1, 51)))
        C2 = tuple(zip([0] * 50,        range(101, 151)))
        D1 = tuple(zip([151] * 50,      range(1, 51)))
        D2 = tuple(zip([101] * 50,      range(101, 151)))
        E1 = tuple(zip(range(101, 151), [51] * 50))
        E2 = tuple(zip([101] * 50,      range(51, 101)))
        F1 = tuple(zip([50] * 50,       range(51, 101)))
        F2 = tuple(zip(range(1, 51),    [100] * 50))
        G1 = tuple(zip(range(51, 101),  [151] * 50)) #
        G2 = tuple(zip([51] * 50,       range(151, 201)))
        # A list of tuples, where each tuple maps each edge to its adjacent
        # one. The boolean represents whether or not the connection should be
        # inverted when wrapping occurs.
        pairs = [(A1, A2, False),
                 (B1, B2, False),
                 (C1, C2, True),
                 (D1, D2, True),
                 (E1, E2, False),
                 (F1, F2, False),
                 (G1, G2, False)]
        # A dict mapping each edge to the direction it faces (outward)
        dirs = {A1: 3, A2: 2, B1: 3, B2: 1, C1: 2, C2: 2, D1: 0,
                D2: 0, E1: 1, E2: 0, F1: 2, F2: 3, G1: 1, G2: 0}
        for pair in pairs:
            for i in range(2):
                # If we are currently on one of the edges, facing outward...
                if tuple(cur_pos) in pair[i] and dirs[pair[i]] == cur_facing:
                    index = pair[i].index(tuple(cur_pos))
                    other = pair[(i + 1) % 2]
                    # Move to the corresponding position on the adjacent edge,
                    # inverting if necessary
                    if pair[2]:
                        cur_pos = list(other[-(index + 1)])
                    else:
                        cur_pos = list(other[index])
                    # Update the facing to point inward relative to the new edge
                    cur_facing = (dirs[other] + 2) % 4
                    # Take one step in the new direction, moving from the edge
                    # to a legal board position
                    cur_pos[0] += steps[cur_facing][0]
                    cur_pos[1] += steps[cur_facing][1]
                    return cur_pos, cur_facing
    # If we get here, we were unable to wrap the inputted position. This should
    # never happen.
    raise KeyError


parsed = setup()
solve(1, *parsed)
solve(2, *parsed)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
