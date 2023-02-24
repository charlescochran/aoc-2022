#! /usr/bin/env python3

import time
import re


start_time = time.process_time()


def setup():
    with open('21-input.txt', 'r') as f:
        pairs = [re.match('([a-z]{4}): (.+)\n', line).groups()  # type: ignore
                 for line in f.readlines()]
    # A two-dimensional list in which each sublist contains a string with a
    # monkey's name and a string with its formula (e.g. ['mnop', 'hjkl / wert'])
    return pairs


def solve_1(parsed):
    monkeys = solve_monkeys(parsed.copy())
    print(f'Part 1: {int(monkeys["root"])}')


def solve_2(parsed, delta):
    root_parents = []
    remaining = []
    # Remove the root and humn monkeys from the pairs list, storing the names
    # of the monkeys which the root monkey depends on
    for pair in parsed:
        if pair[0] == 'root':
            root_parents = re.split(' . ', pair[1])
        elif pair[0] != 'humn':
            remaining.append(pair)
    pairs = remaining
    # Solve as many of the monkeys as possible w/ the humn monkey removed
    monkeys = solve_monkeys(pairs)
    # One of the two root parent monkeys has been solved; it represents the
    # target (the value we are shooting for). The other parent is the monkey
    # whose value we want to reach the target value.
    if root_parents[0] in monkeys:
        target = monkeys[root_parents[0]]
        ans_monkey = root_parents[1]
    else:
        target = monkeys[root_parents[1]]
        ans_monkey = root_parents[0]
    # Using two guessed inputs (separated by delta, which should be a large
    # value), calculate the intercept and slope of the linear equation we are
    # trying to invert
    intercept = guess(pairs.copy(), monkeys.copy(), ans_monkey, 0)
    slope = (guess(pairs.copy(), monkeys.copy(), ans_monkey, delta) - intercept) / delta
    # Finally, invert the linear equation and calculate the input that should
    # result in the answer monkey reaching the target
    ans = int((target - intercept) / slope)
    # Verify that root's equality has been met
    assert guess(pairs.copy(), monkeys.copy(), ans_monkey, ans) == int(target)
    print(f'Part 2: {ans}')


def guess(pairs, monkeys, ans_monkey, guess):
    # Add a humn monkey which simply yells the guessed number to the pairs list
    pairs.insert(0, ('humn', repr(guess)))
    # Solving the monkeys and return the answer monkey's value
    monkeys = solve_monkeys(pairs, monkeys)
    return monkeys[ans_monkey]


def solve_monkeys(pairs, monkeys=None):
    # Using the data from the pairs list and any values already in the monkeys
    # dict, fill out the monkeys dict as much as possible. The returned dict
    # maps monkeys' names to values (as doubles).
    if monkeys is None:
        monkeys = {}
    prev_len = len(pairs) + 1
    # Loop until there are no more unsolved pairs or we have stopped making
    # progress
    while len(pairs) > 0 and len(pairs) < prev_len:
        prev_len = len(pairs)
        remaining = []
        # For each pair, try to evaluate its formula and store it in the monkey
        # dict. If this fails, this monkey needs one or both of its children to
        # be solved first, so put it back in the pairs list.
        for pair in pairs:
            try:
                exec(pair[0] + ' = ' + pair[1], globals(), monkeys)
            except NameError:
                remaining.append(pair)
        pairs = remaining
    return monkeys


pairs = setup()
solve_1(pairs)
solve_2(pairs, 100000000000)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
