import unittest
import sys
from ProgramLoop import ProgramLoop
from Instructions import Instructions

class TestProgramLoop(unittest.TestCase):

	def setUp(self):
		self.loop = ProgramLoop()
		self.loop.programCounter = 0
		self.instructions = Instructions()
		self.loop.byteCodes = ['10000006', '11000003', 'A0100000', '11000005', '70100000', '60000000']
		
	# def test_increment_program_counter(self):
	# 	self.loop.programCounter = 0
	# 	self.loop.execute()
	# 	self.assertEquals(self.loop.programCounter, 6)
	
	# def test_current_instruction_code_to_run(self):
	# 	opcode = self.loop.getInstructionToRun()
	# 	self.assertEquals('1',opcode)

	def test_current_instruction_code_to_run_2(self):
		self.loop.programCounter = 2
		opcode = self.loop.getInstructionToRun()
		self.assertEquals('A',opcode)

	def test_run_instruction(self):
		self.loop.runInstruction('0')

	def test_run_program_one(self):
		self.loop.byteCodes = ['10000006', '11000003', 'A0100000', '11000005', '70100000', '60000000']
		self.loop.execute()	
		self.assertEquals(self.loop.instructions.stdOut,'7\n')

	def test_run_program_two(self):
		self.loop.byteCodes = ['10000010', '60000000']
		self.loop.execute()	
		self.assertEquals(self.loop.instructions.stdOut,'16\n')