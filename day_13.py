#! /usr/bin/env python3

import time
import math
import re


start_time = time.process_time()


def setup():
    with open('13-input.txt', 'r') as f:
        inp = [line.split('\n') for line in f.read().split('\n\n')]
        inp[-1].pop()  # Remove the extra '\n' element in the last pair
        inp = [[eval(packet) for packet in pair] for pair in inp]
    return inp


def get_depth(packet):
    # This will return the nested level of the deepest integer in the packet.
    # Ex: The packet [2, [3], [[4]]] has a depth of 3 (due to the 4).
    depths = [0]
    for item in packet:
        if isinstance(item, list):
            depths.append(get_depth(item))
    return max(depths) + 1


def normalize_int_depths(packet, depth):
    # This will recursively wrap all integers in the packet with lists such
    # that they are all nested to the same level (the level of the integer
    # originally nested the deepest). This is done to facilitate the
    # alphabetical sorting of string representations of the packets.
    # Ex: [2, [3], [[4]]] will become [[[2]], [[3]], [[4]]].
    for index, item in enumerate(packet):
        if isinstance(item, list):
            normalize_int_depths(item, depth - 1)
        else:
            normalized_int = item
            for _ in range(depth - 1):
                normalized_int = [normalized_int]
            packet[index] = normalized_int


def normalize_packets(packets):
    # After normalizing the the packet's int depths (see
    # normalize_int_depths()), this returns a string representation of the
    # packet with certain substitutions to facilitate alphabetical sorting.
    depth = max([get_depth(packet) for packet in packets])
    for packet in packets:
        normalize_int_depths(packet, depth)
    normalized_packets = []
    for packet in packets:
        normalized = repr(packet)
        # Commas need to sort before brackets, so replace with tildes
        normalized = normalized.replace(',', '~')
        # Empty lists need to sort before non-empty lists, so put a space into
        # them
        normalized = normalized.replace('[]', '[ ]')
        # 10 (the highest integer) needs to be only one character long, so
        # replace with a colon
        normalized = normalized.replace('10', ':')
        normalized_packets.append(normalized)
    return normalized_packets


def in_right_order(pair):
    normalized_pair = normalize_packets(pair)
    return sorted(normalized_pair) == normalized_pair


def solve_1(parsed):
    orders = []
    for pair in parsed:
        orders.append(in_right_order(pair))
    indice_sum = sum(map(math.prod, zip(orders, range(1, len(orders) + 1))))
    print(f'Part 1: {indice_sum}')


def solve_2(parsed):
    packets = [packet for pair in parsed for packet in pair]
    packets += [[[2]], [[6]]]
    organized = sorted(normalize_packets(packets))
    decoder_key = math.prod([index + 1 for index, item in enumerate(organized)
                             if re.search(r'^\[\[+[26]\]\]+$', item)])
    print(f'Part 2: {decoder_key}')


parsed = setup()
solve_1(parsed)
solve_2(parsed)

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
