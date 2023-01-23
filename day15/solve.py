#! /usr/bin/python3
import sys


def parse_input(path):
    elves = {}
    goblins = {}
    walls = set()
    for y, line in enumerate(open(path)):
        for x, cell in enumerate(line):
            if cell == '#':
                walls.add((y, x))
            elif cell == 'E':
                elves[(y, x)] = 200
            elif cell == 'G':
                goblins[(y, x)] = 200
    return elves, goblins, walls


def choose_target(actor, allies, enemies, walls):
    enemies = set(enemies)
    visited = walls | set(allies)
    frontier = {actor}
    while frontier:
        new_frontier = set()
        for y, x in frontier:
            new_frontier |= {(y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)}
        visited |= frontier
        frontier = new_frontier - visited
        reached = enemies & frontier
        if reached:
            return sorted(reached)[0]
    return None


def move_towards(actor, target, unpathable):
    visited = set(unpathable) - {actor}
    frontier = {target}
    distances = {}
    distance = 0

    while actor not in distances:
        new_frontier = set()
        for y, x in frontier:
            distances[(y, x)] = distance
            new_frontier |= {(y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)}
        visited |= frontier
        frontier = new_frontier - visited
        distance += 1

    y, x = actor
    for neighbour in [(y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)]:
        if neighbour in distances:
            assert distances[neighbour] == distances[actor] - 1
            return neighbour
    assert 0, "unreachable"


def tick(elves, goblins, walls, ep, gp, verbose=False):
    dead = set()

    def label(thing):
        thing_is_elf = thing in elves
        prefix = 'E' if thing_is_elf else 'G'
        hp = (elves if thing_is_elf else goblins)[thing]
        return "%s%r<%d>" % (prefix, thing, hp)

    for actor in sorted(elves | goblins):
        if actor in dead:
            continue

        is_elf = actor in elves
        power = ep if is_elf else gp

        allies = elves if is_elf else goblins
        enemies = goblins if is_elf else elves
        if not enemies:
            if verbose:
                print("  %s has no enemies left" % (label(actor,)))
            return False
        y, x = actor
        in_range = [cell for cell in [(y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)]
                    if cell in enemies]
        if not in_range:
            target = choose_target(actor, allies, enemies, walls)
            if target:
                prev_pos = actor
                prev_label = label(actor)
                actor = move_towards(actor, target, walls | set(allies))
                allies[actor] = allies.pop(prev_pos)
                y, x = actor
                in_range = [cell for cell in [(y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)]
                            if cell in enemies]
                if verbose:
                    print("  %s moves to %r, targetting %s" % (prev_label, actor, label(target)))
            else:
                if verbose:
                    print("  %s has no target" % (label(actor),))

        if in_range:
            in_range.sort(key=enemies.get)
            target = in_range[0]
            if verbose:
                print("  %s attacks %s, HP now %d" % (label(actor), label(target), enemies[target] - power))
            enemies[target] -= power
            if enemies[target] < 0:
                if verbose:
                    print("  %s dies" % (label(target),))
                dead.add(target)
                del enemies[target]
    return True


def do_battle(elves, goblins, walls, ep, gp):
    elves = elves.copy()
    goblins = goblins.copy()
    n_elves = len(elves)
    rounds = 0
    while tick(elves, goblins, walls, ep, gp):
        rounds += 1
    hp = sum(elves.values()) + sum(goblins.values())
    dead_elves = n_elves - len(elves)
    return hp * rounds, dead_elves


def main(input_file):
    elves, goblins, walls = parse_input(input_file)
    print("Part 1:", do_battle(elves, goblins, walls, 3, 3)[0])

    elf_power = 3
    while True:
        hp, dead = do_battle(elves, goblins, walls, elf_power, 3)
        if not dead:
            print("Part 2:", hp)
            break
        elf_power += 1




if __name__ == '__main__':
    main(sys.argv[1])
