#! /usr/bin/python3
import sys


def analyze_points(points, max_dist):
    x0 = min(x for x, y in points)
    x1 = max(x for x, y in points)
    y0 = min(y for x, y in points)
    y1 = max(y for x, y in points)
    closest = {}
    region_size = 0
    infinite = set()
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            distances = [(abs(px - x) + abs(py - y), (px, py)) for (px, py) in points]
            distances.sort()
            if distances[0][0] < distances[1][0]:
                cx, cy = distances[0][1]
                if (x, y) in [(x0, cy), (x1, cy), (cx, y0), (cx, y1)]:
                    infinite.add((cx, cy))
                closest[(cx, cy)] = closest.get((cx, cy), 0) + 1
            if sum(x[0] for x in distances) < max_dist:
                region_size += 1
    return {k: v for k, v in closest.items() if k not in infinite}, region_size


def main(input_file):
    points = [tuple(int(x) for x in line.split(','))
              for line in open(input_file) if line.strip()]
    closest, region_size = analyze_points(points, 10000)
    print("Part 1:", max(closest.values()))
    print("Part 2:", region_size)


if __name__ == '__main__':
    main(sys.argv[1])
