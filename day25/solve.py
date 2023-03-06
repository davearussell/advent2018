#! /usr/bin/python3
import sys


def main(input_file):
    points = [tuple([int(x) for x in line.split(',')]) for line in open(input_file)]

    def distance(a, b):
        a1, a2, a3, a4 = a
        b1, b2, b3, b4 = b
        return abs(a1 - b1) + abs(a2 - b2) + abs(a3 - b3) + abs(a4 - b4)

    groups = []
    ungrouped = set(points)
    while ungrouped:
        point = ungrouped.pop()
        group = {point}
        while True:
            matches = {u for u in ungrouped if any(distance(u, g) <= 3 for g in group)}
            if not matches:
                break
            group |= matches
            ungrouped -= matches
        groups.append(group)

    print("Part 1:", len(groups))


if __name__ == '__main__':
    main(sys.argv[1])
