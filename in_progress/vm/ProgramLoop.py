from Instructions import Instructions

class ProgramLoop(object):
	
	def __init__(self):
		self.instructions = Instructions()
		self.programCounter = 0
		self.byteCodes = []

	# def execute(self):
	# 	while self.programHasInstructions():
	# 		self.runInstruction(self.getInstructionToRun())
	# 		self.programCounter += 1

	# def programHasInstructions(self):
	# 	return self.programCounter < len(self.byteCodes)

	# def getInstructionToRun(self):
	# 	bc = self.byteCodes[self.programCounter]
	# 	return bc[0:-7]

	# def runInstruction(self,instruction):
	# 	self.instructions.currentByteCode = self.byteCodes[self.programCounter]
	# 	x = self.instructions.opcodes[instruction]()

	def readOutPut(self, output):
		print output
