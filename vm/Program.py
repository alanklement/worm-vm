class Program(object):
	
	def __init__(self):
		self.reg = [0,0,0,0,0,0]
		self.programCounter = 0
		self.byteCodes = []
		self.mem = {}
		self.stdOut = ''
		self.currentByteCode = ""
		self.opcodes = {'0' : self.NOOP, 
						'1' : self.SET, 
						'2' : self.MOVE, 
						'3' : self.LOAD, 				
						'4' : self.STORE, 
						'5' : self.READ,
			 			'6' : self.WRITE, 
			 			'7' : self.ADD, 
			 			'8' : self.SUB, 
					 	'9' : self.MUL,
			 			'A' : self.DIV, 
			 			'B' : self.JMP, 
			 			'C' : self.JMP_Z, 
			 			'D' : self.JMP_NZ,
			 			'E' : self.JMP_GT,
			 			'F' : self.JMP_LT}

	def execute(self):

		self.startUp()
		
		while self.hasCommandsLeft():
			self.doProgramLoop()			

		self.shutDown()

	def startUp(self):
		self.currentByteCode = self.byteCodes[self.programCounter]

	def doProgramLoop(self):				
		jumpOrContinue=self.opcodes[self.getInstructionToRun()]()
		if jumpOrContinue=='continue':
			self.setProgramCounter(self.programCounter + 1)
		
		if self.hasCommandsLeft():
			self.currentByteCode = self.byteCodes[self.programCounter]	

	def shutDown(self):
		print 'WORM Is Done'

	def getInstructionToRun(self):
		bc = self.byteCodes[self.programCounter]
		return bc[0:-7]

	def hasCommandsLeft(self):
		return self.programCounter < len(self.byteCodes)

############instructions

	def NOOP(self):
		return 'continue'

	def SET(self):
		dst = self.getDstID(self.currentByteCode)
		self.reg[dst] = self.get24BitShort(self.currentByteCode)
		return 'continue'

	def MOVE(self):
		dst = self.getDstID(self.currentByteCode)
		src = self.getSrcID(self.currentByteCode)
		self.reg[dst] = self.reg[src]
		return 'continue'

	def LOAD(self):
		dst = self.getDstID(self.currentByteCode)
		pointer = self.getSrcID(self.currentByteCode)
		self.reg[dst] = self.getMemValFromPointer(pointer)		
		return 'continue'

	def STORE(self):
		dst = self.getDstID(self.currentByteCode)
		src = self.getSrcID(self.currentByteCode)
		stackPointerVal = self.reg[dst]		
		self.mem[stackPointerVal] = self.reg[src]
		return 'continue'

	def READ(self):
		self.reg[0] = int(raw_input("WORM VM needs a number: "))
		return 'continue'

	def WRITE(self):
		self.stdOut = str(self.reg[0])
		print 'Worm says: ' + self.stdOut
		return 'continue'

	def ADD(self):
		dst = self.getDstID(self.currentByteCode)
		src = self.getSrcID(self.currentByteCode)
		self.reg[dst] = self.reg[dst] + self.reg[src]
		return 'continue'

	def SUB(self):
		dst = self.getDstID(self.currentByteCode)
		src = self.getSrcID(self.currentByteCode)
		self.reg[dst] = self.reg[dst] - self.reg[src]
		return 'continue'

	def MUL(self):
		dst = self.getDstID(self.currentByteCode)
		src = self.getSrcID(self.currentByteCode)
		self.reg[dst] = self.reg[dst] * self.reg[src]
		return 'continue'

	def DIV(self):
		dst = self.getDstID(self.currentByteCode)
		src = self.getSrcID(self.currentByteCode)
		self.reg[dst] = self.reg[dst] / self.reg[src]
		return 'continue'

	def JMP(self):
		self.setProgramCounter(self.get28BitShort(self.currentByteCode))

	def JMP_Z(self):
		if self.reg[0] == 0:
			self.JMP()
		else:
			return 'continue'

	def JMP_NZ(self):
		if self.reg[0] != 0:
			self.JMP()
		else:
		 	return'continue'

	def JMP_GT(self):
		if self.reg[0] > 0:
			self.JMP()
		else:
			return 'continue'

	def JMP_LT(self):
		if self.reg[0] < 0:
			self.JMP()
		else: 
		 	return 'continue'

	def setProgramCounter(self, goToLine):
			self.programCounter = goToLine	

	def getMemValFromPointer(self, pointer):
		pointerVal = self.reg[pointer]
		return self.mem[pointerVal]

	def get24BitShort(self, arg):
		return int(arg[2:8],16)

	def get28BitShort(self, arg):
		return int(arg[1:8],16)

	def getDstID(self, arg):
		return int(arg[1:-6])

	def getSrcID(self, arg):
		return int(arg[2:-5])

