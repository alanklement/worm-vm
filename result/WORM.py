def NOOP(arg):
	return "continue program"

def SET(arg):
	registers[int(arg[0:-6])] = int(arg[1:],16)
	return "continue program"

def MOVE(arg):
	dstRegister = arg[0:-6]
	targetRegister = arg[1:-5]
	return "continue program"

def READ(arg):
	registers[int(arg[0:-6])] = input
	return "continue program"

def ADD(arg):
	dstRegister = int(arg[0:-6])
	targetRegister = int(arg[1:-5])
	registers[dstRegister] = registers[dstRegister] + registers[targetRegister]
	return "continue program"

def WRITE(arg):
	print 'THUS SPAKE WORM VM:' , registers[0]
	return "continue program"

def JMP(arg):
	return int(arg,16) + 1

def JMP_NZ(arg):
	if registers[0] == 0:
		return "continue program"
	else:
		return int(arg,16) + 1

def extractBytecodesToList(fileToOpen):	
	with open(fileToOpen, 'r') as targetFile:
    		return targetFile.read().splitlines()

def execute(extractedListOfBytecodes):
	programCounter = 0;
	lastCommandInProgram = len(extractedListOfBytecodes)

	while programCounter != lastCommandInProgram:
		bytecode = extractedListOfBytecodes[programCounter]
		opcodeIDToExecute = bytecode[0:-7]	
		opcodeArguements = bytecode[1:8]
		
		continueOrJump = opcodes[opcodeIDToExecute](opcodeArguements)

		if continueOrJump == "continue program":
			programCounter = programCounter+1
		else:
			programCounter = continueOrJump

opcodes = {'0' : NOOP, '1' : SET, '2' : MOVE, '5' : READ, '7' : ADD, '6' : WRITE, 'B' : JMP, 'D' : JMP_NZ}
registers = {0:0,1:0,2:0,3:0,4:0}

### Go!


### ugly for now......
try:
	fileToOpen = raw_input("WORM VM needs a bytecode file: ")	
	extractBytecodesToList(fileToOpen)

	try:
		input = int(raw_input("WORM VM needs a number: "))
		execute(extractBytecodesToList(fileToOpen))
	except ValueError:
		print "Enter a *VALID* number son..."

except IOError:
	print "WORM VM didn't find that file or it was invalid..."









