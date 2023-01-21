#! /usr/bin/python3
import re
import sys

import numpy


def display(positions, max_msg_size):
    minx = int(min(pos[0] for pos in positions))
    maxx = int(max(pos[0] for pos in positions))
    miny = int(min(pos[1] for pos in positions))
    maxy = int(max(pos[1] for pos in positions))
    max_range = max(maxx - minx, maxy - miny)
    scale = min(max_msg_size / max_range, 1)
    scaled = {(int(x * scale), int(y * scale)) for (x, y) in positions}
    s = ''
    for y in range(int(miny * scale), int(maxy * scale) + 1):
        for x in range(int(minx * scale), int(maxx * scale) + 1):
            s += '#' if (x, y) in scaled else '.'
        s += '\n'
    print(s.rstrip('\n'))
    print("Scale:", scale)


def parse_input(path):
    pat = re.compile(r"position=<(.+), (.+)> velocity=<(.+), (.+)>")
    lines = open(path).read().strip().split('\n')
    positions = numpy.zeros([len(lines), 2], dtype=numpy.int64)
    velocities = numpy.zeros([len(lines), 2], dtype=numpy.int64)
    for i, line in enumerate(lines):
        x, y, vx, vy = [int(x) for x in pat.match(line).groups()]
        positions[i] = (x, y)
        velocities[i] = (vx, vy)
    return positions, velocities


def main(input_file):
    positions, velocities = parse_input(input_file)
    max_msg_size = 100
    for i in range(len(positions)):
        if velocities[i][0]:
            skip = max(0, int(positions[i][0] / -velocities[i][0]) - max_msg_size)
            break
    positions += velocities * skip
    i = skip
    while True:
        print("Iteration %d:" % (i,))
        i += 1
        display(positions, max_msg_size)
        input()
        positions += velocities


if __name__ == '__main__':
    main(sys.argv[1])
