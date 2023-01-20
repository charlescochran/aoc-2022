#! /usr/bin/env python3

import time
import re
import random
import copy


start_time = time.process_time()


def setup():
    with open('16-input.txt', 'r') as f:
        inp = f.read().split('\n')[:-1]
        flowrates = {}
        neighbors = {}
        for line in inp:
            valve_names = re.findall('[A-Z]{2}', line)
            neighbors[valve_names[0]] = valve_names[1:]
            valve_flowrate = int(re.findall('[0-9]+', line)[0])
            flowrates[valve_names[0]] = valve_flowrate
    return neighbors, flowrates


def generate_sols(num, part):
    sols = []
    for _ in range(num):
        sol = []
        for _ in range(part):
            path = []
            cur = 'AA'
            for _ in range(30 if part == 1 else 26):
                cur = random.choice((cur, *neighbors[cur]))
                path.append(cur)
            sol.append(path)
        sols.append(sol)
    return sols


def fitness(sol, part):
    cur = ['AA'] * part
    released = 0
    rate = 0
    closed_valves = []
    if part == 2:
        ticks = zip(*sol)
    else:
        ticks = [(step,) for step in sol[0]]
    for steps in ticks:
        released += rate
        for p in range(part):
            if cur[p] == steps[p]:
                if cur[p] not in closed_valves:
                    rate += flowrates[cur[p]]
                    closed_valves.append(cur[p])
            else:
                cur[p] = steps[p]
    return released


def crossover(gen, fitnesses, part):
    attempts_remaining = 14
    parents = random.choices(population=gen, weights=fitnesses, k=2)
    children = copy.deepcopy(parents)
    for p in range(part):
        while True:
            s = random.randrange(1, len(parents[0][p]))
            if (not parents[0][p][s] in (parents[1][p][s - 1], *neighbors[parents[1][p][s - 1]])
                    or not parents[1][p][s] in (parents[0][p][s - 1],
                                                *neighbors[parents[0][p][s - 1]])):
                attempts_remaining -= 1
                if attempts_remaining <= 0:
                    # Crossover pair didn't work... Pick another pair.
                    return crossover(gen, fitnesses, part)
                # Crossover point didn't work... Pick another point.
                continue
            children[0][p][s:] = parents[1][p][s:]
            children[1][p][s:] = parents[0][p][s:]
            break
    return children


def get_neighbor(sol, shift_prob, part):
    neighbor = copy.deepcopy(sol)
    init_fitness = fitness(neighbor, part)
    while True:
        neighbor = mutate(neighbor, 3, shift_prob, part)
        if not fitness(neighbor, part) == init_fitness:
            return neighbor


def mutate(sol, max_mutations, shift_prob, part):
    for p in range(part):
        for _ in range(random.choice(range(max_mutations + 1))):
            if random.random() <= shift_prob:
                shift_mutate(sol[p])
            else:
                replace_mutate(sol[p])
    return sol


def replace_mutate(path):
    while True:
        s = random.randrange(1, len(path) - 1)
        replacements = get_between_steps(path[s - 1], path[s + 1])
        if path[s] in replacements:
            replacements.remove(path[s])
        if replacements:
            path[s] = random.choice(replacements)
            break


def shift_mutate(path):
    path = path
    while True:
        s = random.randrange(1, len(path) - 1)
        if random.choice((True, False)):
            # Shift right
            additions = get_between_steps(path[s - 1], path[s])
            if additions:
                path.pop()
                path.insert(s, random.choice(additions))
                break
        elif path[s - 1] in (path[s + 1], *neighbors[path[s + 1]]):
                # Shift left
                path.pop(s)
                path.append(random.choice((path[-1], *neighbors[path[-1]])))
                break


def get_between_steps(first_step, second_step):
    return list(set((first_step, *neighbors[first_step])) &
                set((second_step, *neighbors[second_step])))


def sort_gen(gen, part):
    fitnesses = [fitness(sol, part) for sol in gen]
    sorted_gen = sorted(gen, key=lambda sol: fitnesses[gen.index(sol)], reverse=True)
    return (sorted_gen, fitnesses)


def solve(gen_size, num_random, num_kept, stale_period, max_mutations, shift_mutation_prob,
          num_iters, part):
    iter_fitnesses = []
    for i in range(num_iters):
        iter_start_time = time.process_time()
        print(f'========== Iteration {i + 1} ==========')
        gen, fitnesses = sort_gen(generate_sols(gen_size, part), part)
        gen_num = 0
        gens_until_stale = stale_period
        prev_best_fitness = 0
        while True:
            gen_num += 1
            gens_until_stale -= 1
            new_gen = gen[:num_kept] + generate_sols(num_random, part)
            for _ in range(int((gen_size - num_random - num_kept) / 2)):
                pair = crossover(gen, fitnesses, part)
                new_gen.append(mutate(pair[0], max_mutations, shift_mutation_prob, part))
                new_gen.append(mutate(pair[1], max_mutations, shift_mutation_prob, part))
            gen, fitnesses = sort_gen(new_gen, part)
            best_fitness = fitnesses[0]
            if best_fitness > prev_best_fitness:
                gens_until_stale = stale_period
                print(f'Generation {gen_num}: Best Fitness: {best_fitness}')
                print(f'  Top Solution:')
                print(f'  {gen[0]}')
                prev_best_fitness = best_fitness
            if gens_until_stale <= 0:
                iter_fitnesses.append(best_fitness)
                iter_time = time.process_time() - iter_start_time
                print(f'Iteration CPU execution time: {iter_time:.4f} s')
                iter_start_time = time.process_time()
                break
    sorted_fitnesses = sorted(iter_fitnesses, reverse=True)
    print(f'After {num_iters} iterations:')
    for i, iter_fitness in enumerate(sorted(list(set(sorted_fitnesses)), reverse=True)):
        print(f'{i + 1}. {iter_fitness} ({sorted_fitnesses.count(iter_fitness)}/{num_iters})')
    return sorted_fitnesses[0]


neighbors, flowrates = setup()
print(f'Part 1: {solve(1000, 100, 50, 60, 6, 0.6, 100, 1)}')

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
