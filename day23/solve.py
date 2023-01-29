#! /usr/bin/python3
import re
import sys


def parse_input(path):
    pat = re.compile(r'pos=.(.+),(.+),(.+)., r=(.+)')
    bots = []
    for line in open(path):
        x, y, z, r = [int(x) for x in pat.match(line).groups()]
        bots.append(Bot((x, y, z), r))
    return bots


class Bot:
    def __init__(self, center, size):
        self.center = center # (x, y, z)
        self.size = size

    def in_range_of(self, point):
        ax, ay, az = self.center
        bx, by, bz = point
        return abs(ax - bx) + abs(ay - by) + abs(az - bz) <= self.size


def main(input_file):
    bots = parse_input(input_file)

    strongest = max(bots, key = lambda b: b.size)
    in_range = [other for other in bots if strongest.in_range_of(other.center)]
    print("Part 1:", len(in_range))

    # This is not a general solution but works for all inputs I've seen.
    # It assumes that all regions are in the same quadrant and that we
    # can find the overlap by reducing each bot to a 1D line based on
    # its closest/furthest manhattan distance to the origin. The solution
    # is the the point at which the greatest number of lines intersect.
    dists = []
    for bot in bots:
        (x, y, z), s = bot.center, bot.size
        c = abs(x) + abs(y) + abs(z)
        dists += [(c - s, 0), (c + s, 1)]

    count = best_count = best_dist = 0
    for (dist, is_end) in sorted(dists):
        if is_end:
            count -= 1
        else:
            count += 1
            if count > best_count:
                best_count = count
                best_dist = dist

    print("Part 2:", best_dist)


if __name__ == '__main__':
    main(sys.argv[1])
