from ArguementReader import ArguementReader

def NOOP(arg):
	return "continue program"

def SET(arg):
	registers[int(arg[0:-6])] = int(arg[1:],16)
	return "continue program"

def MOVE(arg):
	dstRegister = arg[0:-6]
	targetRegister = arg[1:-5]
	return "continue program"

def LOAD(arg):
	dstRegister = int(arg[0:-6])
	stackPointer = int(arg[1:-5])
	try:
		registers[dstRegister] = memory[registers[stackPointer]]
	except Exception:
		print "Invalid Memory Access (memory address may not exist)"
	return "continue program"

def STORE(arg):
	stackPointer = int(arg[0:-6])
	srcRegister = int(arg[1:-5])
	memory[stackPointer] = registers[srcRegister]
	return "continue program"

def READ(arg):
	registers[int(arg[0:-6])] = int(raw_input("WORM VM needs a number: "))
	return "continue program"

def ADD(arg):
	dstRegister = int(arg[0:-6])
	targetRegister = int(arg[1:-5])
	registers[dstRegister] = registers[dstRegister] + registers[targetRegister]
	return "continue program"

def SUB(arg):
	dstRegister = int(arg[0:-6])
	targetRegister = int(arg[1:-5])
	registers[dstRegister] = registers[dstRegister] - registers[targetRegister]
	return "continue program"

def MUL(arg):
	dstRegister = int(arg[0:-6])
	targetRegister = int(arg[1:-5])
	registers[dstRegister] = registers[dstRegister] * registers[targetRegister]
	return "continue program"

def DIV(arg):
	dstRegister = int(arg[0:-6])
	targetRegister = int(arg[1:-5])
	registers[dstRegister] = registers[dstRegister] / registers[targetRegister]
	return "continue program"

def WRITE(arg):
	print 'THUS SPAKE WORM VM:' , registers[0]
	return "continue program"

def JMP(arg):
	return int(arg,16)

def JMP_NZ(arg):
	if registers[0] != 0:
		return int(arg,16)
	else:
		return "continue program"

def JMP_GT(arg):
	if registers[0] > 0:
		return "continue program"
	else:
		return int(arg,16)

# def printDebugInfoIfInVerboseMode(bc,function,pc):
# 	if app_args.verbose >= 1:
# 		print "**just executed bytecode:", bc , ",", function, ", at program line:" , str(pc)
# 	if app_args.verbose >=2: 
# 		print '>> registers: ', registers
# 		print '>> memory:    ', memory	


def execute():

	argparser = ArguementReader()
	argparser.listenForArguements()

	bytecodes = argparser.file.read().splitlines()
	programCounter = 0
	incrementInstuction = 1
	lastCommandInProgram = len(bytecodes)

	while programCounter < lastCommandInProgram:
		
		bytecode = bytecodes[programCounter]
		opcodeIDToExecute = bytecode[0:-7]	
		print opcodeIDToExecute
		opcodeArguements = bytecode[1:8]		
		continueOrJump = opcodes[opcodeIDToExecute](opcodeArguements)

		# printDebugInfoIfInVerboseMode(bytecode,opcodes[opcodeIDToExecute],programCounter+1)
		
		# if app_args.verbose >=3:
		# 	cont = raw_input("continue? Type: 'y' or 'n'")
		# 	if cont == 'y':
		# 		pass
		# 	elif cont == 'n':
		# 		break

		if continueOrJump == "continue program":
			programCounter = programCounter+incrementInstuction
		else:
			programCounter = continueOrJump

opcodes = {		'0' : NOOP, 
				'1' : SET, 
				'2' : MOVE, 
				'3' : LOAD, 				
				'4' : STORE, 
				'5' : READ,
			 	'6' : WRITE, 
			 	'7' : ADD, 
			 	'8' : SUB, 
			 	'9' : MUL,
			 	'A' : DIV, 
			 	'B' : JMP, 
			 	'D' : JMP_NZ,
			 	'E' : JMP_GT}

registers = {0:0,1:0,2:0,3:0,4:0,5:0}
memory = {}
## GO
execute()








