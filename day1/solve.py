#! /usr/bin/python3
import sys


def main(input_file):
    values = [int(x) for x in open(input_file).read().split()]
    print("Part 1:", sum(values))

    value = 0
    seen = set()
    i = 0
    while True:
        if value in seen:
            print("Part 2:", value)
            break
        seen.add(value)
        value += values[i % len(values)]
        i += 1


if __name__ == '__main__':
    main(sys.argv[1])
