#! /usr/bin/python3
import operator
import sys


def parse_input(path):
    ip = None
    insns = []
    for line in open(path):
        spl = line.split()
        if not spl:
            continue
        op = spl[0]
        args = [int(x) for x in spl[1:]]
        if op == '#ip':
            ip = args[0]
        else:
            insns.append((op, args))
    return insns, ip


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


def run(insns, ip_reg, state):
    ops = make_ops()
    ip = 0
    while 0 <= ip < len(insns):
        op, args = insns[ip]
        state[ip_reg] = ip
        state = ops[op](state, *args)
        ip = state[ip_reg] + 1
    return state


def factors(n):
    for i in range(1, int(n ** .5) + 1):
        if n % i == 0:
            yield i
            yield n // i


def main(input_file):
    insns, ip = parse_input(input_file)

    # Analysing the program revealed it boiled down to:
    # R4 = <big number>
    # for a in range(1, R4 + 1):
    #   for b in range(1, R4 + 1):
    #     if a * b == R4:
    #       R0 += a
    # So we can just run it until it has finished calculating R4
    # and then calculate the sum of factors more efficiently
    insns[1] = ('seti', (1000, 0, ip))

    state = [0] * 6
    print("Part 1:", sum(factors(run(insns, ip, state)[4])))

    state[0] = 1
    print("Part 2:", sum(factors(run(insns, ip, state)[4])))


if __name__ == '__main__':
    main(sys.argv[1])
