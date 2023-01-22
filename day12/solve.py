#! /usr/bin/python3
import sys


def parse_input(path):
    state = None
    transitions = set()
    for line in open(path):
        if state is None:
            state = {i for i, c in enumerate(line.split(':')[1].strip()) if c == '#'}
        elif line.strip():
            k, v = line.strip().split(' => ')
            if v == '#':
                transitions.add(tuple((c == '#') for c in k))
    return state, transitions


def iterate(state, transitions, n):
    for _ in range(n):
        l = min(state) - 2
        r = max(state) + 2
        next_state = set()
        for i in range(l, r + 1):
            if tuple((i + x in state) for x in range(-2, 3)) in transitions:
                next_state.add(i)
        state = next_state
    return next_state


def main(input_file):
    state, transitions = parse_input(input_file)

    part1_generations = 20
    stable_generations = 1000
    part2_generations = 50000000000

    state = iterate(state, transitions, 20)
    print("Part 1:", sum(state))

    state = iterate(state, transitions, stable_generations - part1_generations)
    score = sum(state)
    delta = sum(iterate(state, transitions, 1)) - score
    print("Part 2:", score + delta * (part2_generations - stable_generations))


if __name__ == '__main__':
    main(sys.argv[1])
