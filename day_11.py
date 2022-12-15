#! /usr/bin/env python3

import time
import re
import math
import copy


start_time = time.process_time()


class Monkey():

    def __init__(self, data):
        self.items = list(map(int, re.findall('[0-9]+', data[1])))
        self.operate = lambda old: eval(data[2][re.search('= ', data[2]).end():])  # type: ignore
        self.test_factor = int(re.search('[0-9]+', data[3]).group())  # type: ignore
        self.receivers = (int(re.search('[0-9]+', data[4]).group()),  # type: ignore
                          int(re.search('[0-9]+', data[5]).group()))  # type: ignore
        self.num_items_inspected = 0
        # The following are overridden by setup() once all monkeys are created
        self.lcm = 0
        self.monkeys = []

    def decrease(self, item, part):
        if part == 1:
            return int(item / 3)
        else:
            return item % self.lcm

    def test(self, item):
        return not item % self.test_factor

    def inspect_items(self, part):
        for item in self.items:
            item = self.decrease(self.operate(item), part)
            if self.test(item):
                self.monkeys[self.receivers[0]].items.append(item)
            else:
                self.monkeys[self.receivers[1]].items.append(item)
        self.num_items_inspected += len(self.items)
        self.items = []


def setup():
    with open('11-input.txt', 'r') as f:
        inp = [monkey.split('\n') for monkey in f.read().split('\n\n')]
    monkeys = []
    for monkey_data in inp:
        monkeys.append(Monkey(monkey_data))
    # All test factors are prime, so this is equivalent to just multiplying
    # them together, but this would also handle non-prime test factors
    lcm = math.lcm(*[monkey.test_factor for monkey in monkeys])  # Requires Python 3.9
    # Finish setting up the monkeys
    for monkey in monkeys:
        monkey.lcm = lcm
        monkey.monkeys = monkeys
    return monkeys


def solve(parsed, part):
    for _ in range(20 if part == 1 else 10000):
        for monkey in parsed:
            monkey.inspect_items(part)
    inspection_counts = sorted([monkey.num_items_inspected for monkey in parsed])
    print(f'Part {part}: {inspection_counts[-1] * inspection_counts[-2]}')


parsed = setup()
solve(copy.deepcopy(parsed), 1)
solve(copy.deepcopy(parsed), 2)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
