#! /usr/bin/env python3

import time


start_time = time.process_time()


def setup():
    with open('3-input.txt', 'r') as f:
        inp = f.read().split('\n')[:-1]
    return inp


def solve_1(parsed):
    priority_sum = 0
    for line in parsed:
        for char in line[int(len(line) / 2):]:
            if char in line[:int(len(line) / 2)]:
                priority_sum += get_char_priority(char)
                break
    print(f'Part 1: {priority_sum}')


def solve_2(parsed):
    priority_sum = 0
    for i in range(0, len(parsed), 3):
        for char in parsed[i]:
            if char in parsed[i + 1] and char in parsed[i + 2]:
                priority_sum += get_char_priority(char)
                break
    print(f'Part 2: {priority_sum}')


def get_char_priority(char):
    priority = ord(char)
    # if letter is capital
    if priority < 91:
        priority -= 38
    # otherwise, letter is lowercase
    else:
        priority -= 96
    return priority


parsed = setup()
solve_1(parsed)
solve_2(parsed)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
