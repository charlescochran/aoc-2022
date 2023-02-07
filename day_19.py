#! /usr/bin/env python3

import time
import re
import numpy as np
import operator
from tqdm import tqdm


start_time = time.process_time()


def setup():
    with open('19-input.txt', 'r') as f:
        blueprints = []
        inp = f.read().split('\n')[:-1]
        for line in inp:
            blueprints.append(tuple([int(cost) for cost in re.findall('[0-9]+', line)][1:]))
    # blueprint format: (ore robot ore cost ore, clay robot ore cost ore,
    #                    obsidian robot ore cost, obsidian robot clay cost,
    #                    geode robot ore cost, geode robot obsidian cost)
    return blueprints


def explore(t, mins, robots, resources, blueprint, bar):
    bar.update()
    old_resources = resources.copy()
    # Add the resources generated this minute
    resources = list(map(operator.add, robots, resources))
    # Optimization: instead of cutting off the search once has expired, cut it
    # off early. If this is the third to last minute...
    if t == mins - 3:
        # Find the number of geodes that we'll have at the end with the current
        # geode robots
        geodes = resources[-1] + robots[3] * 2
        # Can we build a geode bot this round? If so, add the two geodes that
        # it will produce
        if old_resources[0] >= blueprint[4] and old_resources[2] >= blueprint[5]:
            geodes += 2
            resources[0] -= blueprint[4]
            resources[2] -= blueprint[5]
        # Can we build one next round? If so, add the one geode that it will
        # produce
        if resources[0] >= blueprint[4] and resources[2] >= blueprint[5]:
            geodes += 1
        return geodes

    # Try building each kind of robot
    best = 0
    num_buildable = 0
    # 0: Ore robot
    # If we can afford the ore robot...
    if old_resources[0] >= blueprint[0]:
        # Optimization: if we have enough ore robots and enough ore such that
        # we could build the robot with the highest ore cost every single
        # remaining minute (except for the last one, which doesn't matter), we
        # don't need any more ore robots
        if robots[0] < max(*blueprint[:3], blueprint[4]) - int(old_resources[0] / (mins - t - 1)):
            new_robots = robots.copy()
            new_robots[0] += 1
            new_resources = resources.copy()
            new_resources[0] -= blueprint[0]
            # Recursively explore the next minute after building an ore robot
            best = max(best, explore(t + 1, mins, new_robots, new_resources, blueprint, bar))
            num_buildable += 1
    # 1: Clay robot
    if old_resources[0] >= blueprint[1]:
        if robots[1] < blueprint[3] - int(old_resources[1] / (mins - t - 1)):
            new_robots = robots.copy()
            new_robots[1] += 1
            new_resources = resources.copy()
            new_resources[0] -= blueprint[1]
            best = max(best, explore(t + 1, mins, new_robots, new_resources, blueprint, bar))
            num_buildable += 1
            # Optimization: if we haven't yet built any clay robots and can now
            # afford one (and could also afford an ore robot), don't bother
            # "saving up" for an obsidian or geode bot (since we will need
            # clay/obsidian to build them)
            if robots[1] == 0 and num_buildable == 2:
                return best
    # 2: Obsidian robot
    if old_resources[0] >= blueprint[2] and old_resources[1] >= blueprint[3]:
        if robots[2] < blueprint[5] - int(old_resources[2] / (mins - t - 1)):
            new_robots = robots.copy()
            new_robots[2] += 1
            new_resources = resources.copy()
            new_resources[0] -= blueprint[2]
            new_resources[1] -= blueprint[3]
            best = max(best, explore(t + 1, mins, new_robots, new_resources, blueprint, bar))
            num_buildable += 1
            if robots[2] == 0 and num_buildable == 3:
                return best
    # 3: Geode robot
    if old_resources[0] >= blueprint[4] and old_resources[2] >= blueprint[5]:
        new_robots = robots.copy()
        new_robots[3] += 1
        new_resources = resources.copy()
        new_resources[0] -= blueprint[4]
        new_resources[2] -= blueprint[5]
        best = max(best, explore(t + 1, mins, new_robots, new_resources, blueprint, bar))
    # Optimization: if we were able to buy a geode bot, don't bother "saving
    # up" because there's nothing better to save up for
    else:
        best = max(best, explore(t + 1, mins, robots, resources, blueprint, bar))
    return best


def solve(blueprints, part):
    ans = 0
    for i, blueprint in enumerate(blueprints if part == 1 else blueprints[:3]):
        print(f'Exploring blueprint {i + 1}:')
        mins = 24 if part == 1 else 32
        geodes = explore(0, mins, [1, 0, 0, 0], [0] * 4, blueprint, tqdm())
        print(f'{geodes} geodes cracked.\n')
        if part == 1:
            ans += (i + 1) * geodes
        else:
            ans *= geodes
    print(f'Part {part}: {ans}')


blueprints = setup()
solve(blueprints, 1)  # Runtime: ~ 2 min
solve(blueprints, 2)  # Runtime: ~ 4 hrs

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
