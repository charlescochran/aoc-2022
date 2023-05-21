#! /usr/bin/env python3

import time


start_time = time.process_time()


def setup():
    # The values of the five digits in SNAFU
    vals = (2, 1, 0, -1, -2)
    # Their string representations
    digits = ('2', '1', '0', '-', '=')
    # Read the input SNAFU numbers
    with open('25-input.txt', 'r') as f:
        snafus = f.read().split('\n')[:-1]
    return snafus, vals, digits


def solve():
    # Convert each SNAFU number to decimal, add them up, and convert the result
    # to SNAFU
    ans = decimal_to_snafu(sum(snafu_to_decimal(snafu) for snafu in snafus))
    print(f'Part 1: {ans}')


def snafu_to_decimal(snafu):
    # An integer containing the result, in decimal
    decimal = 0
    # The least signficant place value is 1
    multiplier = 1
    # Iterate over the digits backwards (starting in the 1s place, then 5s
    # place, then 25s place, etc.)
    for digit in snafu[::-1]:
        # Add to the total the result of multiplying this digit's value (given
        # by its character) by its place value (given by the multiplier)
        decimal += multiplier * vals[digits.index(digit)]
        # Multiply the multiplier by five to prepare for the next place (moving
        # to the left)
        multiplier *= 5
    return decimal


def decimal_to_snafu(decimal):
    # Find the most significant place value, assuming the decimal input is
    # positive (the greatest power of five that is less than it)
    multiplier = 1
    while multiplier * 5 < decimal:
        multiplier *= 5
    # A string containing the result, in SNAFU
    snafu = ''
    # The current remaining amount
    remainder = decimal
    # Until we have run of out of places...
    while multiplier >= 1:
        # Find which of the five allowable values (2, 1, 0, -1, -2), if written
        # in this place, would make the remainder the closest to zero
        val = sorted(vals, key=lambda val: abs(remainder - multiplier * val))[0]
        # Add the corresponding digit character to the right of the others
        snafu += digits[vals.index(val)]
        # Decrease the remainder by the corresponding amount
        remainder -= multiplier * val
        # Divide the multiplier by five to prepare to the next place (moving to
        # the right)
        multiplier /= 5
    return snafu


snafus, vals, digits = setup()
solve()

print(f'\nCPU execution time: {(time.process_time() - start_time) * 1000:.4f} ms')
