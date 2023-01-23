#! /usr/bin/python3
import sys


def main(magic_number):
    score_from = int(magic_number)
    pattern = [int(c) for c in magic_number]
    recipes = [3, 7]
    e1, e2 = 0, 1

    part1 = part2 = False

    while not (part1 and part2):
        r1, r2 = recipes[e1], recipes[e2]
        rx = r1 + r2
        if rx >= 10:
            recipes.append(1)
            rx -= 10
            if not part2:
                if recipes[-len(pattern):] == pattern:
                    part2 = True
                    print("Part 2:", len(recipes) - len(pattern))

        recipes.append(rx)
        if not part2:
            if recipes[-len(pattern):] == pattern:
                part2 = True
                print("Part 2:", len(recipes) - len(pattern))

        o1, o2 = e1, e2
        e1 = (e1 + r1 + 1) % len(recipes)
        e2 = (e2 + r2 + 1) % len(recipes)

        if not part1 and len(recipes) >= score_from + 10:
            score = recipes[score_from: score_from + 10]
            print("Part 1:", ''.join(map(str, score)))
            part1 = True


if __name__ == '__main__':
    main(sys.argv[1])
