import operator

FNS = {
    'add': operator.add,
    'mul': operator.mul,
    'ban': operator.and_,
    'bor': operator.or_,
    'set': lambda a, b: a,
    'gt': lambda a, b: 1 if a > b else 0,
    'eq': lambda a, b: 1 if a == b else 0,
}


def parse_prog(path):
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


def analyse_prog(insns, ip_reg):
    symbols = {'gt': '>', 'eq': '==', 'add': '+', 'mul': '*', 'ban': '&', 'bor': '|'}
    lines = []
    for ip, (opcode, (a, b, out_reg)) in enumerate(insns):
        comment = '# %s (%d %d %d)' %  (opcode, a, b, out_reg)
        amode = bmode = 'r'
        if opcode.startswith('gt') or opcode.startswith('eq'):
            op, amode, bmode = opcode[:2], opcode[2], opcode[3]
        elif opcode.startswith('set'):
            op, amode = opcode[:-1], opcode[-1]
        else:
            op, bmode = opcode[:-1], opcode[-1]

        if amode == 'r':
            a = ip if a == ip_reg else 'R%d' % a
        if bmode == 'r':
            b = ip if b == ip_reg else 'R%d' % b

        lhs = 'JMP' if out_reg == ip_reg else 'R%d = ' % (out_reg,)
        if op == 'set':
            rhs = a
        elif isinstance(a, int) and isinstance(b, int):
            rhs = FNS[op](a, b)
        else:
            rhs = '%s %s %s' % (a, symbols[op], b)

        line = '% 3d: %s %s' % (ip, lhs, rhs)
        lines.append((line, comment))

    line_len = max(len(line) for line, _ in lines) + 3
    comment_len = max(len(comment) for _, comment in lines) + 3
    return ['%s%s%s%s' % (line, ' ' * (line_len - len(line)),
                          comment, ' ' * (comment_len - len(comment)))
            for line, comment in lines]


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
    ops = {}
    for name in ['add', 'mul', 'ban', 'bor']:
        for mode in ['r', 'i']:
            ops[name + mode] = make_op(FNS[name], 'r', mode)
    for name in ['gt', 'eq']:
        for mode in ['ir', 'ri', 'rr']:
                ops[name + mode] = make_op(FNS[name], mode[0], mode[1])
    for name in ['set']:
        for mode in ['r', 'i']:
                ops[name + mode] = make_op(FNS[name], mode, 'x')
    return ops
OPS = make_ops()


def run(insns, state=None, ip_reg=None, verbose=False):
    decodes = analyse_prog(insns, ip_reg)
    if state is None:
        state = [0, 0, 0, 0, 0, 0]
    ip = 0
    while 0 <= ip < len(insns):
        op, args = insns[ip]
        if ip_reg is not None:
            state[ip_reg] = ip
        new_state = OPS[op](state, *args)
        if verbose:
            print("%s %s -> %s" % (decodes[ip], state, new_state))
        state = new_state
        if ip_reg is not None:
            ip = state[ip_reg]
        ip += 1
    return state

