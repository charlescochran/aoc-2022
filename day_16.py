#! /usr/bin/env python3

import time
import re
import numpy as np
import itertools
from tqdm import tqdm


start_time = time.process_time()


def setup():
    with open('16-input.txt', 'r') as f:
        inp = f.read().split('\n')[:-1]
        valve_ids = {}
        for i, line in enumerate(inp):
            valve_ids[re.search('[A-Z]{2}', line).group(0)] = i  # type: ignore
        neighbors = []
        flowrates = []
        for line in inp:
            neighbor_names = re.findall('[A-Z]{2}', line)[1:]
            neighbors.append([valve_ids[name] for name in neighbor_names])
            flowrates.append(int(re.findall('[0-9]+', line)[0]))
    dists = calc_dists(valve_ids, neighbors)
    # List the valves with non-zero flowrates
    working_valves = set([id for id, flowrate in enumerate(flowrates) if flowrate > 0])
    return valve_ids, working_valves, flowrates, dists


def calc_dists(valve_ids, neighbors):
    # Implementation of the Floyd-Warshall algorithm. This calculates the
    # shortest path between all rooms and stores the result in an n x n numpy
    # matrix.
    n = len(valve_ids)
    dists = np.full((n, n), np.inf)
    # The distance between any room and itself is zero
    for i in range(n):
        dists[i][i] = 0
    # The distance between any room and one of its neighbors is one
    for valve_id, neighbor_ids in enumerate(neighbors):
        for neighbor_id in neighbor_ids:
            dists[valve_id][neighbor_id] = 1
    # Calculate the shortest dist of all remaining rooms
    for k in range(n):
        for i in range(n):
            for j in range(n):
                new_dist = dists[i][k] + dists[k][j]
                if new_dist < dists[i][j]:
                    dists[i][j] = new_dist
    return dists.astype(int)


def dfs(released, best_released, clock, mins, closed, bar, cur=None, optimize=True):
    # Recursively search all possible paths and return the score (and path) of
    # the best one. Overall runtime for part 2 is about 50 minutes.
    bar.update(1)
    # -- 1. Update clock and released, get next valve combinations --
    # If this is the beginning of the search, search only the pick-1 or pick-2
    # (depending on how many agents there are) combination (as opposed to
    # permutation) of the closed valves (i.e., 'AB...' is the same as 'BA...',
    # but only at the beginning)
    if cur is None:
        agents = len(clock)
        cur = [valve_ids['AA']] * agents
        next_valves = itertools.combinations(closed, r=agents)
    # Otherwise, if we are in the search...
    else:
        # Increment the clock
        clock = [time + 1 for time in clock]
        # Remove the current valves from the closed list and increment the
        # overall pressure released by the total future pressure released by
        # each valve
        for valve in cur:
            closed.remove(valve)
        released += sum([flowrates[valve] * (mins - clock[i]) for i, valve in enumerate(cur)])
        # If we have run out of closed valves, end this branch
        if not closed:
            return released, []
        # An agent has expired if it has two or less minutes left, since it
        # will need, at the very least, one minute to travel to the next valve
        # and one to open it (and a third for it to take effect). Thus, remove
        # expired agents by removing their timestamp from the clock and their
        # position from the cur list.
        # Note: pair designates a (time, valve) pair, produced by zipping clock
        # and cur.
        try:
            clock, cur = zip(*filter(lambda pair: pair[0] < mins - 2, zip(clock, cur)))
        # If all the agents have expired, scrap the rest of this branch
        except ValueError:
            return released, []
        # Otherwise, update the number of agents
        agents = len(clock)
        # From here, we should next explore the pick-1/2 (depending on the
        # number of agents) permutations (as opposed to combinations) of the
        # still-closed valves (i.e., 'ABCD...' is different from 'ABDC...').
        # If the number of closed valves is greater than zero but less than the
        # number of agents, pad the list with Nones such that all remaining
        # permutations are still explored.
        next_valves = itertools.permutations(list(closed) + [None] * (agents - len(closed)),
                                             r=agents)

    # -- 2. Fancy optimization --
    # Without taking into account how the rooms are arranged, the best possible
    # situation (resulting in the most pressure released) would be that the
    # remaining valves are lined up such that we can open N valves every 2
    # minutes, starting with those with the highest flowrate (N is the number
    # of agents). In other words, if there are two agents, they can each open
    # one of the two highest flowrate valves after two minutes from now (this
    # coming minute will be spent traveling, and the next one opening them).
    # Then, every two minutes after that, they can open the next two
    # highest-flowrate valves.
    # Thus, calculate the maximum possible pressure released by this branch,
    # assuming the remaining closed valves are all opened in this ideal fashion
    # (or the agent with the most time left expires). If this pressure is less
    # than the actual amount released by the best path we've found so far,
    # scrap the rest of this branch.
    # In practice, this optimization is fairly expensive. Despite lowering the
    # number of recursive dfs() calls needed in part two by roughly 45%, it
    # only speeds the solution up by about 25%.
    # Note: A simpler optimization was also tried in which all the remaining
    # valves were assumed to be opened as the soonest possible opportunity (two
    # minutes plus the current time of the agent with the most time left). This
    # optimization is less expensive, but it does not cut off as many branches,
    # dropping the number of total dfs() calls by only about 1%. It performs
    # comparably with the unoptimized version.
    if optimize:
        # Find the largest amount of time that any agent has left
        most_mins_remaining = mins - min(clock)
        # Find and sort the flowrates of the remaining valves
        sorted_flowrates = sorted([flowrates[valve] for valve in closed],
                                  reverse=True)
        # Calculate the number of valve-opening groups based on the number of
        # closed valves and the number of agents. If there are 5 closed valves
        # (AA-EE) and 2 agents, there will be three groups, corresponding to (AA,
        # BB), (CC, DD), and (EE,).
        num_groups = min(int((len(sorted_flowrates) + 1) / agents),
                         int((most_mins_remaining - 1) / 2))
        # Add up the flowrates for each group
        group_flowrates = [sum(sorted_flowrates[i:i + agents])
                           for i in range(0, agents * num_groups, agents)]
        # Calculate the flowtimes for each group. For the first group, this is
        # the max remaining time minus two. For the second, subtract four. For
        # the third, six...
        group_flowtimes = [most_mins_remaining - (2 * n) for n in range(1, num_groups + 1)]
        # To find the pressure released by the branch in this ideal circumstance,
        # multiply each group's flowrate by the corresponding flowtime and add this to
        # the amount already released
        max_possible_released = released + np.dot(group_flowrates, group_flowtimes)
        # If this branch cannot beat the current best one, scrap it
        if max_possible_released < best_released:
            return 0, []

    # Temp: Jank Optimization
    most_mins_remaining = mins - min(clock)
    max_possible_released = released + sum([flowrates[valve] for valve in closed]) * most_mins_remaining - 2;
    if max_possible_released < best_released:
        return 0, []

    # -- 3. Recursively explore next valve combinations --
    best_released = released
    best_path = []
    for next in next_valves:
        # Generate the clock to use for the next exploration
        next_clock = []
        for i in range(len(clock)):
            # If a value is None, there is no valve for this agent to open, so
            # go ahead and make sure its time expires
            if next[i] is None:
                next_clock.append(mins)
            # Otherwise, increment this agent's time based on the distance it
            # has to travel
            else:
                next_clock.append(clock[i] + dists[cur[i], next[i]])
        # Recursively explore the next permutation
        total_released, next_path = dfs(released, best_released, next_clock, mins, closed.copy(),
                                        bar, cur=list(next), optimize=optimize)
        # Update the best_released variable and construct the best path from
        # the end to the beginning
        if total_released > best_released:
            best_released = total_released
            best_path = [next] + next_path
    # Return the overall amount of pressure released and the path in the best
    # scenario (so far)
    return best_released, best_path


def solve(part):
    clock = [0] * part
    mins = 30 if part == 1 else 26
    best, path = dfs(0, 0, clock, mins, working_valves, tqdm())
    print(f'Part {part}: {best}')
    print(f'Solution: {path}')


valve_ids, working_valves, flowrates, dists = setup()
solve(1)
solve(2)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
