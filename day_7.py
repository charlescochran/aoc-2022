#! /usr/bin/env python3

import time
import math


start_time = time.process_time()


def setup():
    with open('7-input.txt', 'r') as f:
        inp = f.read().split('\n')[:-1]
    return inp


def solve(parsed):
    total_size = 0
    dirs = {}
    up_dirs = []
    cur_dir = ''
    for line in parsed:
        if line[0:4] == '$ cd':
            dir_name = line[5:]
            if dir_name == '..':
                cur_dir = up_dirs.pop()
            else:
                if cur_dir:
                    up_dirs.append(cur_dir)
                dir_path = '/'
                if len(up_dirs) >= 1:
                    dir_path = ''.join((up_dirs[-1], dir_name, '/'))
                if dir_path not in dirs.keys():
                    dirs[dir_path] = 0
                cur_dir = dir_path
        # If the line starts with a number, it is a file
        if ord(line[0]) in range(48, 58):
            size = int(line[:line.index(' ')])
            dirs[cur_dir] += size
            for up_dir in up_dirs:
                dirs[up_dir] += size
    unused = 70000000 - dirs['/']
    need_to_free = 30000000 - unused
    smallest = math.inf
    for size in dirs.values():
        if size <= 100000:
            total_size += size
        if size < smallest and size >= need_to_free:
            smallest = size
    print(f'Part 1: {total_size}')
    print(f'Part 2: {smallest}')


parsed = setup()
solve(parsed)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
