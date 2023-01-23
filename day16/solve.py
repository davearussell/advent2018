#! /usr/bin/python3
import json
import operator
import sys


def parse_input(path):
    data = open(path).read()
    sample_text, prog_text = data.split('\n\n\n\n')
    samples = []
    for sample in sample_text.split('\n\n'):
        lines = sample.split('\n')
        samples.append({
            'before': json.loads(lines[0].split(':')[1]),
            'insn': [int(x) for x in lines[1].split()],
            'after': json.loads(lines[2].split(':')[1]),
        })
    prog = [[int(x) for x in line.split()] for line in prog_text.split('\n') if line.strip()]
    return samples, prog


def make_op(op, lhs_type, rhs_type):
    def fn(state, a, b, c):
        if lhs_type == 'r':
            a = state[a]
        if rhs_type == 'r':
            b = state[b]
        state = state.copy()
        state[c] = op(a, b)
        return state
    return fn


def make_ops():
    fns = {
        'add': operator.add,
        'mul': operator.mul,
        'ban': operator.and_,
        'bor': operator.or_,
        'set': lambda a, b: a,
        'gt': lambda a, b: 1 if a > b else 0,
        'eq': lambda a, b: 1 if a == b else 0,
    }
    ops = {}
    for name in ['add', 'mul', 'ban', 'bor']:
        for mode in ['r', 'i']:
            ops[name + mode] = make_op(fns[name], 'r', mode)
    for name in ['gt', 'eq']:
        for mode in ['ir', 'ri', 'rr']:
                ops[name + mode] = make_op(fns[name], mode[0], mode[1])
    for name in ['set']:
        for mode in ['r', 'i']:
                ops[name + mode] = make_op(fns[name], mode, 'x')
    return ops


def main(input_file):
    samples, prog = parse_input(input_file)
    ops_by_name = make_ops()

    p1_count = 0
    candidates = {}
    for i, sample in enumerate(samples):
        opcode, a, b, c = sample['insn']
        matches = {name for (name, op) in ops_by_name.items()
                   if op(sample['before'], a, b, c) == sample['after']}
        if len(matches) >= 3:
            p1_count += 1
        if opcode not in candidates:
            candidates[opcode] = matches
        candidates[opcode] &= matches
    print("Part 1:", p1_count)

    ops = {}
    while candidates:
        for opcode, names in candidates.items():
            if len(names) == 1:
                del candidates[opcode]
                name = names.pop()
                ops[opcode] = ops_by_name[name]
                for _names in candidates.values():
                    _names -= {name}
                break

    state = [0, 0, 0, 0]
    for opcode, a, b, c in prog:
        state = ops[opcode](state, a, b, c)
    print("Part 2:", state[0])


if __name__ == '__main__':
    main(sys.argv[1])
