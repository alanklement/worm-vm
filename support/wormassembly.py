import re

Registers = [
    'A',  # used for branching & io
    'B',
    'C',
    'D',

    'E',  # 1 if (E)nd of readable input, otherwise 0
    'S',  # (S)tack pointer
]

def register_num(letter):
    try:
        return (''.join(Registers)).index(letter)
    except ValueError:
        raise Exception('invalid register: %s' % letter)

def data(value):
    value = int(value)
    if value < 0 or value > 0xFFFFFF:
        raise ValueError('value %d is out of range 0-%d' % (value, 0xFFFFFF))
    return value

def instruction_num(value):
    value = int(value)
    if value < 0 or value > 0xFFFFFFF:
        raise ValueError('instruction %d is out of range 0-%d' % (value, 0xFFFFFFF))
    return value

build_2_registers = lambda a, b: '%01X%01X' % (register_num(a), register_num(b))

# Index in this array is the opcode.
Instructions = {
    'NOOP': {
        'code': 0x00,
    },

    # Register Stuff
    'SET': {
        'code': 0x01,
        're': re.compile(r'%([A-Z]), +[$](0|[1-9][0-9]*)'),
        'build': lambda a, b: '%01X%06X' % (register_num(a), data(b)),
    },
    'MOVE': {
        'code': 0x02,
        're': re.compile(r'%([A-Z]), +%([A-Z])'),
        'build': build_2_registers,
    },
    'LOAD': {
        'code': 0x03,
        're': re.compile(r'%([A-Z]), +@([A-Z])'),
        'build': build_2_registers,
    },
    'STORE': {
        'code': 0x04,
        're': re.compile(r'@([A-Z]), +%([A-Z])'),
        'build': build_2_registers,
    },

    # I/O
    'READ': {
        'code': 0x05,
    },
    'WRITE': {
        'code': 0x06,
    },

    # Math
    'ADD': {
        'code': 0x07,
        're': re.compile(r'%([A-Z]), +%([A-Z])'),
        'build': build_2_registers,
    },
    'SUB': {
        'code': 0x08,
        're': re.compile(r'%([A-Z]), +%([A-Z])'),
        'build': build_2_registers,
    },
    'MUL': {
        'code': 0x09,
        're': re.compile(r'%([A-Z]), +%([A-Z])'),
        'build': build_2_registers,
    },
    'DIV': {
        'code': 0x0A,
        're': re.compile(r'%([A-Z]), +%([A-Z])'),
        'build': build_2_registers,
    },

    # Branching
    # First pass through assembly, the arg to the jump contains the label
    # ID. The second pass replaces them with instruction #s.
    'JMP': {
        'code': 0x0B,
        're': re.compile(r'L([0-9]+)'),
        'build': lambda l: '%07X' % data(l),
    },
    'JMP_Z': {
        'code': 0x0C,
        're': re.compile(r'L([0-9]+)'),
        'build': lambda l: '%07X' % data(l),
    },
    'JMP_NZ': {
        'code': 0x0D,
        're': re.compile(r'L([0-9]+)'),
        'build': lambda l: '%07X' % data(l),
    },
    'JMP_GT': {
        'code': 0x0E,
        're': re.compile(r'L([0-9]+)'),
        'build': lambda l: '%07X' % data(l),
    },
    'JMP_LT': {
        'code': 0x0F,
        're': re.compile(r'L([0-9]+)'),
        'build': lambda l: '%07X' % data(l),
    },
}

