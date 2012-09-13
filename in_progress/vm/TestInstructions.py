import unittest
from Program import Program

class TestInstructions(unittest.TestCase):
	
	def setUp(self):
		self.opCodes = Program()

	def test_SET_Register_A_TO_20(self):
		r = self.opCodes.reg
		self.opCodes.currentByteCode = "10000014"
		self.opCodes.SET()
		for i, val in enumerate(r):
					self.assertEquals(r[i],20) if (i == 0) else self.assertEquals(r[i],0)	

	def test_MOVE_Value_Of_B_To_D(self):
		r = self.opCodes.reg = [0,11,0,33,0,0]
		self.opCodes.currentByteCode = "23100000"
		self.opCodes.MOVE()

		self.assertEquals(r[3],11)
		self.assertEquals(r[3],r[1])
		
		for i, val in enumerate(r):
	    		if r[i] != 11: 
	    			self.assertEquals(r[i],0)
	    			self.assertNotEqual(r[i],33)

	def test_get_Destination_Register_ID_From_Instruction(self):
		id = self.opCodes.getDstID("12345678")
		self.assertEquals(id,2)

	def test_get_Source_Register_ID_From_Instruction(self):
		id = self.opCodes.getSrcID("12345678")
		self.assertEquals(id,3)

	def test_Get_Memory_Val_From_Pointer(self):
		self.opCodes.reg = [0,11,22,33,44,55]
		self.opCodes.mem = [43,11,22,33,44]
		pointer = self.opCodes.reg[0]

		value = self.opCodes.getMemValFromPointer(pointer)
		self.assertEquals(value,43)

	def test_LOAD_From_Memory_To_Register(self):
		r = self.opCodes.reg = [8,11,0,33,0,0]
		self.opCodes.mem = [0,1,2,3,4,5,6,7,43]
		self.opCodes.currentByteCode = "32000000"
		self.opCodes.LOAD()

		self.assertEquals(r[2],43)

	def test_STORE_From_Register_To_Memory(self):
		self.opCodes.reg = [99,0,22,33,1,55]
		m = self.opCodes.mem = [0]
		self.opCodes.currentByteCode = "41400000"
		self.opCodes.STORE()
		self.assertEquals(m[0],1)

	# def test_Get_Next_Standard_Input(self):
	# 	self.opCodes.stdOut = 55
	# 	input = self.opCodes.getNextStandardInput()
	# 	self.assertEquals(input,55)

	# def test_READ_Next_Standard_Input_Put_In_Reg_A(self):
	# 	r = self.opCodes.reg = [0,11,22,33,44,55]
	# 	self.opCodes.stdOut = 99
	# 	self.opCodes.READ()
	# 	self.assertEquals(99,r[0])

	def test_WRITE_Regsiter_A_To_stdout(self):
		r = self.opCodes.reg = [39,11,22,33,44,55]
		self.opCodes.WRITE()
		self.assertEquals("39",self.opCodes.stdOut)

	def test_ADD_Reg_D_B_Put_Sum_In_D(self):
		r = self.opCodes.reg = [0,-19,0,39,0,0]
		self.opCodes.currentByteCode = "73100000"
		self.opCodes.ADD()
		self.assertEquals(20,r[3])

	def test_SUB_D_B_Put_Difference_In_D(self):
		r = self.opCodes.reg = [0,19,0,20,0,0]
		self.opCodes.currentByteCode = "83100000"
		self.opCodes.SUB()
		self.assertEquals( 1,r[3])

	def test_SUB_Minus_Values(self):
		r = self.opCodes.reg = [0,20,0,19,0,0]
		self.opCodes.currentByteCode = "83100000"
		self.opCodes.SUB()
		self.assertEquals( -1,r[3])

	def test_MUL_Reg_D_B_Put_Product_In_D(self):
		r = self.opCodes.reg = [0,13,0,3,0,0]
		self.opCodes.currentByteCode = "93100000"
		self.opCodes.MUL()
		self.assertEquals( 39,r[3])

	def test_DIV_Reg_D_B_Put_Quotient_In_D(self):
		r = self.opCodes.reg = [0,2,0,3,0,0]
		self.opCodes.currentByteCode = "A3100000"
		self.opCodes.DIV()
		self.assertEquals( 1, r[3])

	def test_JMP_Z_Return_Continue(self):
		self.opCodes.reg = [1,2,0,3,0,0]
		self.opCodes.currentByteCode = "C0000001"
		r = self.opCodes.JMP_Z()		
		self.assertEquals(r,'continue')

	# def test_JMP_Z_advance_program_counter(self):
	# 	self.opCodes.reg = [0,1,0,3,0,0]
	# 	self.opCodes.currentByteCode = "C0000001"
	# 	self.opCodes.JMP_Z()		
	# 	self.assertEquals(1,self.opCodes.programCounter)

	def test_JMP_NZ_Return_Continue(self):
		self.opCodes.reg = [0,2,0,3,0,0]
		self.opCodes.currentByteCode = "D0000001"
		r = self.opCodes.JMP_NZ()		
		self.assertEquals(r,'continue')

	def test_JMP_GT_Return_Continue(self):
		self.opCodes.reg = [0,2,0,3,0,0]
		self.opCodes.currentByteCode = "E0000001"
		r = self.opCodes.JMP_GT()		
		self.assertEquals(r,"continue")

	def test_JMP_LT_Return_Continue(self):
		self.opCodes.reg = [0,2,0,3,0,0]
		self.opCodes.currentByteCode = "F0000001"
		r = self.opCodes.JMP_LT()		
		self.assertEquals(r,'continue')

	def test_increment_program_counter(self):
		self.opCodes.programCounter = 0
		self.opCodes.byteCodes = ['10000006', '11000003', 'A0100000', '11000005', '70100000', '60000000']
		self.opCodes.execute()
		self.assertEquals(self.opCodes.programCounter, 6)

	def test_current_instruction_code_to_run(self):
		self.opCodes.byteCodes = ['10000006', '11000003', 'A0100000', '11000005', '70100000', '60000000']
		opcode = self.opCodes.getInstructionToRun()
		self.assertEquals('1',opcode)

	def test_current_instruction_code_to_run_2(self):
		self.opCodes.programCounter = 2
		self.opCodes.byteCodes = ['10000006', '11000003', 'A0100000', '11000005', '70100000', '60000000']
		opcode = self.opCodes.getInstructionToRun()
		self.assertEquals('A',opcode)

	def test_run_program_one(self):
		self.opCodes.byteCodes = ['10000006', '11000003', 'A0100000', '11000005', '70100000', '60000000']
		self.opCodes.execute()	
		self.assertEquals(self.opCodes.stdOut,'7')

	def test_run_program_two(self):
		self.opCodes.byteCodes = ['10000010', '60000000']
		self.opCodes.execute()	
		self.assertEquals(self.opCodes.stdOut,'16')

	def test_run_program_with_write(self):
		self.opCodes.byteCodes = ['10000065', '60000000']
		self.opCodes.execute()
		self.assertEquals('101',self.opCodes.stdOut)	

	def test_run_program_with_JMP(self):
		# x0000099 = 153
		self.opCodes.byteCodes = ['00000000','10000099','B0000004','11000001','70100000','60000000']
		self.opCodes.execute()
		self.assertEquals('153',self.opCodes.stdOut)	

	def test_run_program_with_JMP_Z(self):
		self.opCodes.byteCodes = ['10000000','C0000003','10000014','60000000']
		self.opCodes.execute()
		self.assertEquals('0',self.opCodes.stdOut)	

	def test_run_program_with_JMP_Z_no_jump(self):
		self.opCodes.byteCodes = ['10000001','C0000003','10000014','60000000']
		self.opCodes.execute()
		self.assertEquals('20',self.opCodes.stdOut)	

	def test_run_program_with_JMP_NZ(self):
		self.opCodes.byteCodes = ['10000015','D0000003','10000014','60000000']
		self.opCodes.execute()
		self.assertEquals('21',self.opCodes.stdOut)	

	def test_run_program_with_JMP_NZ_no_jump(self):
		self.opCodes.byteCodes = ['10000000','D0000003','10000014','60000000']
		self.opCodes.execute()
		self.assertEquals('20',self.opCodes.stdOut)	

	def test_run_program_with_JMP_GT(self):
		self.opCodes.byteCodes = ['10000001','E0000003','10000014','60000000']
		self.opCodes.execute()
		self.assertEquals('1',self.opCodes.stdOut)	

	def test_run_program_with_JMP_GT_no_jump(self):
		self.opCodes.byteCodes = ['10000001','11000005','80100000','E0000005','10000014','60000000']
		self.opCodes.execute()
		self.assertEquals('20',self.opCodes.stdOut)	

	def test_run_program_with_JMP_LT(self):
		self.opCodes.byteCodes = ['10000001','11000005','80100000','F0000005','10000014','60000000']
		self.opCodes.execute()
		self.assertEquals('-4',self.opCodes.stdOut)	

	def test_run_program_with_JMP_LT_no_jump(self):
		self.opCodes.byteCodes = ['10000001','11000005','F0000004','10000014','60000000']
		self.opCodes.execute()
		self.assertEquals('20',self.opCodes.stdOut)	

	def test_run_program_store_memory(self):
		elf.opCodes.byteCodes = ['10000008']

