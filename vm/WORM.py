from Program import Program
from DebugProgram import DebugProgram
from ArguementReader import ArguementReader

argparser = ArguementReader()
argparser.listenForArguements()

if argparser.debugLvl > 0:
	baseProgram = Program()
	program = DebugProgram(baseProgram)
	program.debugLvl = argparser.debugLvl
else:
	program = Program()	

program.byteCodes = argparser.file.read().splitlines()
program.execute()
