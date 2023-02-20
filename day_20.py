#! /usr/bin/env python3

import time


start_time = time.process_time()


def setup():
    with open('20-input.txt', 'r') as f:
        inp = [int(num) for num in f.read().split('\n')[:-1]]
    return inp


def solve(nums, part):
    n = len(nums)
    if part == 2:
        nums = [(val * 811589153) for val in nums]
    # Create a list of two-item sublists, where the first item in each sublist
    # is the number from the file and the second item represents the position
    # (as an index) of that value. Originally, these indices are 0, 1, 2, ...
    # but they will change as mixing occurs.
    # Note that this is essentially a dictionary which maps each numbers to its
    # position, but it is actually a nested list instead of a dictionary so
    # that it can handle duplicate keys
    positions = list(map(list, zip(nums, range(n))))
    # For each round of mixing...
    for _ in range(10 if part == 2 else 1):
        # For each number (always in the original order)...
        for i in range(n):
            old_pos = positions[i][1]
            # Calculate its new position
            new_pos = (old_pos + positions[i][0]) % (n - 1)
            # Next, shift the positions of the other affected numbers (either
            # forward by 1 or back by 1, depending on if this item is moving
            # backward or forward)
            shift = -1 if new_pos > old_pos else 1
            shift_range = range(min(old_pos, new_pos), max(old_pos, new_pos) + 1)
            for j in range(n):
                if positions[j][1] in shift_range:
                    positions[j][1] += shift
            # Finally, update the position of this number
            positions[i][1] = new_pos
    # Sort the mixed list according to the positions
    positions = sorted(positions, key=lambda pos: pos[1])
    # Find the index of the 0
    zero_pos = [pos[0] for pos in positions].index(0)
    # Display the sum of the 1000th, 2000th, and 3000th numbers
    ans = 0
    for x in range(1, 4):
        ans += positions[(zero_pos + 1000 * x) % n][0]
    print(f'Part {part}: {ans}')


parsed = setup()
solve(parsed, 1)
solve(parsed, 2)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
