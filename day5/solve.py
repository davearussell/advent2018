#! /usr/bin/python3
import string
import sys


def react(polymer):
    seqs = [a + a.upper() for a in string.ascii_lowercase]
    seqs += [x[::-1] for x in seqs]
    next_polymer = polymer
    while True:
        for seq in seqs:
            next_polymer = next_polymer.replace(seq, '')
        if next_polymer == polymer:
            break
        polymer = next_polymer
    return len(polymer)


def main(input_file):
    polymer = open(input_file).read().strip()

    print("Part 1:", react(polymer))

    scores = []
    for char in set(polymer.lower()):
        stripped = polymer.replace(char, '').replace(char.upper(), '')
        scores.append(react(stripped))
    print("Part 2:", min(scores))


if __name__ == '__main__':
    main(sys.argv[1])
