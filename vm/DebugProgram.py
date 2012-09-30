from Program import Program

class DebugProgram(Program):
	def __init__(self, arg):
		super(DebugProgram, self).__init__()
		self.debugLvl = 0

	def execute(self):

		print '\n\n****** WORM Is In Debug Mode*******\n\n'

		self.startUp()
		
		while self.hasCommandsLeft():
			self.debugStartLoop()
			self.doProgramLoop()			
			self.debug()
		
		self.shutDown()

	def debugStartLoop(self):
		if self.debugLvl >= 2 and self.hasCommandsLeft():
			print '>>starting loop:' , 'programCounter is:', self.programCounter, ' about to run:: ', self.currentByteCode, ' on ' , self.opcodes[self.getInstructionToRun()]
			print '      registers:', self.reg
			print '         memory:', self.mem	

	def debug(self):
		if self.debugLvl >= 1 and self.hasCommandsLeft():
				print "     >>just executed:", self.currentByteCode 
		if self.debugLvl >=2 and self.programCounter < len(self.byteCodes): 
				print '           registers:', self.reg
				print '              memory:', self.mem	

	def debugJMP(self):
		if self.debugLvl >=3 and self.hasCommandsLeft(): 
			print '\n jumping to command #: ' + str(self.get28BitShort(self.currentByteCode)) + '\n'

	def JMP(self):
		self.debugJMP()
		self.setProgramCounter(self.get28BitShort(self.currentByteCode))
		
