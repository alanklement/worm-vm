from Program import Program
from ArguementReader import ArguementReader

argparser = ArguementReader()
argparser.listenForArguements()

program = Program()
program.byteCodes = argparser.file.read().splitlines()
program.execute()
