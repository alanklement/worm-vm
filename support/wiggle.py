#!/usr/bin/python

import re
import struct
from wormassembly import *

class WiggleError(Exception):
    def __init__(self, line_num, line, msg=''):
        self.line_num = line_num
        self.line = line
        self.msg = msg

    def __str__(self):
        out = [
            'Error assembling worm bytecode on line %d:' % self.line_num,
            '\t%s' % self.line,
        ]
        if self.msg:
            out.append('\tError: %s' % self.msg)
        return '\n'.join(out)


def assemble(lines):
    out = []
    labels = {}

    label_re = re.compile(r'^ *L([0-9]+) *: *$')
    instruction_re = re.compile(r'^ *(%s)( .+)? *$' % '|'.join(Instructions.keys()))

    for line_num, line in enumerate(lines):
        # Strip out comments
        clean_line = line.strip().partition('#')[0]

        if clean_line:
            match = label_re.match(clean_line)
            if match:
                # Keep track of next instruction #.
                label_num = data(match.groups()[0])

                if label_num in labels:
                    raise WiggleError('Label L%s already defined earlier.' % match)

                labels[label_num] = len(out)
            else:
                match = instruction_re.match(clean_line)

                if not match:
                    raise WiggleError(line_num+1, line, 'invalid syntax')

                instruction = match.groups()[0]
                args = (match.groups()[1] or '').strip()

                instruction_code = Instructions[instruction]['code']
                arg_code = ''

                # If a regex is given for handling args, use it.
                arg_re = Instructions[instruction].get('re')
                if arg_re:
                    arg_match = arg_re.match(args)
                    if not arg_match:
                        raise WiggleError(line_num+1, line, 'invalid args')

                    # Build it if possible.
                    build_fn = Instructions[instruction].get('build')
                    if build_fn:
                        try:
                            arg_code = build_fn(*arg_match.groups())
                        except Exception, err:
                            raise WiggleError(line_num+1, line, 'error processing args: %s' % str(err))

                # pad args to flesh out 4 bytes (8 hex chars), minus the half byte
                # for the instruction
                arg_code += '0' * (7 - len(arg_code))

                out.append('%01X%s' % (instruction_code, arg_code))

    # Make another pass through bytecode to replace label IDs with
    # instruction locations.
    jmp_codes = [v['code'] for k, v in Instructions.iteritems() if k.startswith('JMP')]
    for i, instruction in enumerate(out):
        # unpack instruction
        code = int(instruction[0], 16)
        if code in jmp_codes:
            label = int(instruction[1:], 16)

            try:
                instruction_num = labels[label]
            except KeyError:
                raise WiggleError(0, '', 'Label L%d not found.' % label)

            # Rebuild instruction
            out[i] = '%1X%07X' % (code, instruction_num)

    return out


if __name__ == '__main__':
    import sys
    from optparse import OptionParser
    import os.path

    usage = 'Usage: %prog [options] src_file'
    parser = OptionParser(usage=usage)
    parser.add_option('-o', '--out', dest='out',
                      help='Output file. Defaults to same as src file with a .wormbc extension.')
    parser.add_option('', '--hex', dest='hex',
                      action='store_true', default=False,
                      help='Output instructions one per line in hex.')

    (options, args) = parser.parse_args()

    if len(args) < 1:
        sys.exit('Need to at least supply a source file.')

    # Try to fix up path and see if it exists.
    src_path = args[0]
    if src_path.startswith('~'):
        # Must do this first, or it won't expand it.
        src_path = os.path.expanduser(src_path)
    src_path = os.path.abspath(src_path)
    if not os.path.exists(src_path):
        sys.exit('Source file not found: %s' % args[0])

    out_path = options.out
    if not out_path:
        # Split up, so we can pick an outfile.
        src_dir, src_base = os.path.split(src_path)
        src_name = os.path.splitext(src_base)[0]
        out_path = os.path.join(src_dir, src_name + '.wormbc')

    assembly_code = open(src_path, 'r').readlines()

    try:
        bytecode = assemble(assembly_code)
    except WiggleError, err:
        sys.exit(err)

    if options.hex:
        bytecode = ['%s\n' % bc for bc in bytecode]
    else:
        bytecode = [struct.pack('>L', int(bc, 16)) for bc in bytecode]

    open(out_path, options.hex and 'w+' or 'w+b').writelines(bytecode)
