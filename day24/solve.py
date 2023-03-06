#! /usr/bin/python3
import re
import sys

class Group:
    def __init__(self, side, n, hp, attrs, dmg, dmg_type, init):
        self.side = side
        self.n = n
        self.hp = hp
        self.attrs = attrs
        self.dmg = dmg
        self.dmg_type = dmg_type
        self.initiative = init

    @property
    def power(self):
        return self.n * self.dmg


def parse_attrs(attr_text):
    if not attr_text:
        return {}
    attrs = {}
    for clause in attr_text.split(';'):
        words = clause.split(None, 2)
        assert len(words) == 3 and words[1] == 'to', attr_text
        for dmg_type in words[2].split(', '):
            attrs[dmg_type] = words[0]
    return attrs


def parse_input(path):
    pat = re.compile(r"(\d+) units each with (\d+) hit points (?:[(](.+)[)] )?"
                    "with an attack that does (\d+) (.+) damage at initiative (\d+)")
    groups = []
    side = None
    for line in open(path):
        if line.endswith(':\n'):
            side = line[:-2]
        elif line.strip():
            x = pat.match(line)
            assert x, line
            count, hp, attrs, dmg, dmg_type, init = x.groups()
            groups.append(Group(
                side,
                int(count),
                int(hp),
                parse_attrs(attrs),
                int(dmg),
                dmg_type,
                int(init)
            ))
    return groups


def fight_round(groups):
    def target_prio(group): return (-group.power, -group.initiative)
    def attack_prio(group): return -group.initiative

    untargeted = {}
    for side in {group.side for group in groups}:
        untargeted[side] = {group for group in groups if group.side != side}

    targets = {}
    for g in sorted(groups, key=target_prio):
        candidates = [t for t in untargeted[g.side] if t.attrs.get(g.dmg_type) == 'weak']
        if not candidates:
            candidates = [t for t in untargeted[g.side] if t.attrs.get(g.dmg_type) is None]
        if not candidates:
            continue
        target = min(candidates, key=target_prio)
        targets[g] = target
        untargeted[g.side].remove(target)

    any_kills = False
    for attacker in sorted(targets, key=attack_prio):
        defender = targets[attacker]
        dmg = attacker.power
        if defender.attrs.get(attacker.dmg_type) == 'weak':
            dmg *= 2
        kills = min(defender.n, dmg // defender.hp)
        any_kills |= bool(kills)
        defender.n -= kills
        if not defender.n:
            groups.remove(defender)

    if not any_kills:
        return "deadlock"
    sides = {g.side for g in groups}
    if len(sides) == 1:
        return sides.pop()


def fight(path, boost=0):
    groups = parse_input(path)
    for group in groups:
        if group.side == 'Immune System':
            group.dmg += boost
    while not (winner := fight_round(groups)):
        pass
    n = sum(g.n for g in groups)
    return winner, n


def main(input_file):
    winner, n = fight(input_file)
    assert winner == 'Infection'
    print("Part 1:", n)

    lower_bound = 1
    boost = 1
    while True:
        winner, n = fight(input_file, boost)
        if winner == 'Immune System':
            upper_bound = boost
            break
        boost *= 2
    while lower_bound < upper_bound:
        candidate = (lower_bound + upper_bound) // 2
        winner, _ = fight(input_file, candidate)
        if winner == 'Immune System':
            upper_bound = candidate
        elif candidate == lower_bound:
            lower_bound = upper_bound
        else:
            lower_bound = candidate
    print("Part 2:", fight(input_file, lower_bound)[1])


if __name__ == '__main__':
    main(sys.argv[1])
