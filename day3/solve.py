#! /usr/bin/python3
import re
import sys


def main(input_file):
    pat = re.compile(r'.* @ (\d+),(\d+): (\d+)x(\d+)')
    claims = [[int(v) for v in pat.search(line).groups()] for line in open(input_file)]

    claimed = set()
    double_claimed = set()

    for x0, y0, w, h in claims:
        claim = {(x, y) for x in range(x0, x0 + w) for y in range(y0, y0 + h)}
        double_claimed |= (claimed & claim)
        claimed |= claim
    print("Part 1:", len(double_claimed))

    single_claimed = claimed - double_claimed
    for i, (x0, y0, w, h) in enumerate(claims):
        claim = {(x, y) for x in range(x0, x0 + w) for y in range(y0, y0 + h)}
        if claim <= single_claimed:
            print("Part 2:", i + 1)


if __name__ == '__main__':
    main(sys.argv[1])
