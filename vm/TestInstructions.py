import unittest
from Program import Program

class TestInstructions(unittest.TestCase):
	
	def setUp(self):
		self.program = Program()

	def test_SET_Register_A_TO_20(self):
		r = self.program.reg
		self.program.currentByteCode = "10000014"
		self.program.SET()
		for i, val in enumerate(r):
					self.assertEquals(r[i],20) if (i == 0) else self.assertEquals(r[i],0)	

	def test_MOVE_Value_Of_B_To_D(self):
		r = self.program.reg = [0,11,0,33,0,0]
		self.program.currentByteCode = "23100000"
		self.program.MOVE()

		self.assertEquals(r[3],11)
		self.assertEquals(r[3],r[1])
		
		for i, val in enumerate(r):
	    		if r[i] != 11: 
	    			self.assertEquals(r[i],0)
	    			self.assertNotEqual(r[i],33)

	def test_get_Destination_Register_ID_From_Instruction(self):
		id = self.program.getDstID("12345678")
		self.assertEquals(id,2)

	def test_get_Source_Register_ID_From_Instruction(self):
		id = self.program.getSrcID("12345678")
		self.assertEquals(id,3)

	def test_Get_Memory_Val_From_Pointer(self):
		self.program.reg = [0,11,22,33,44,55]
		self.program.mem = [43,11,22,33,44]
		pointer = self.program.reg[0]

		value = self.program.getMemValFromPointer(pointer)
		self.assertEquals(value,43)

	def test_LOAD_From_Memory_To_Register(self):
		r = self.program.reg = [8,11,0,33,0,0]
		self.program.mem = [0,1,2,3,4,5,6,7,43]
		self.program.currentByteCode = "32000000"
		self.program.LOAD()

		self.assertEquals(r[2],43)

	def test_STORE_From_Register_To_Memory(self):
		self.program.reg = [99,0,22,33,1,55]
		m = self.program.mem = [0]
		self.program.currentByteCode = "41400000"
		self.program.STORE()
		self.assertEquals(m[0],1)

	def test_WRITE_Regsiter_A_To_stdout(self):
		r = self.program.reg = [39,11,22,33,44,55]
		self.program.WRITE()
		self.assertEquals("39",self.program.stdOut)

	def test_ADD_Reg_D_B_Put_Sum_In_D(self):
		r = self.program.reg = [0,-19,0,39,0,0]
		self.program.currentByteCode = "73100000"
		self.program.ADD()
		self.assertEquals(20,r[3])

	def test_SUB_D_B_Put_Difference_In_D(self):
		r = self.program.reg = [0,19,0,20,0,0]
		self.program.currentByteCode = "83100000"
		self.program.SUB()
		self.assertEquals( 1,r[3])

	def test_SUB_Minus_Values(self):
		r = self.program.reg = [0,20,0,19,0,0]
		self.program.currentByteCode = "83100000"
		self.program.SUB()
		self.assertEquals( -1,r[3])

	def test_MUL_Reg_D_B_Put_Product_In_D(self):
		r = self.program.reg = [0,13,0,3,0,0]
		self.program.currentByteCode = "93100000"
		self.program.MUL()
		self.assertEquals( 39,r[3])

	def test_DIV_Reg_D_B_Put_Quotient_In_D(self):
		r = self.program.reg = [0,2,0,3,0,0]
		self.program.currentByteCode = "A3100000"
		self.program.DIV()
		self.assertEquals( 1, r[3])

	def test_JMP_Z_Return_Continue(self):
		self.program.reg = [1,2,0,3,0,0]
		self.program.currentByteCode = "C0000001"
		r = self.program.JMP_Z()		
		self.assertEquals(r,'continue')

	def test_JMP_NZ_Return_Continue(self):
		self.program.reg = [0,2,0,3,0,0]
		self.program.currentByteCode = "D0000001"
		r = self.program.JMP_NZ()		
		self.assertEquals(r,'continue')

	def test_JMP_GT_Return_Continue(self):
		self.program.reg = [0,2,0,3,0,0]
		self.program.currentByteCode = "E0000001"
		r = self.program.JMP_GT()		
		self.assertEquals(r,"continue")

	def test_JMP_LT_Return_Continue(self):
		self.program.reg = [0,2,0,3,0,0]
		self.program.currentByteCode = "F0000001"
		r = self.program.JMP_LT()		
		self.assertEquals(r,'continue')

	def test_increment_program_counter(self):
		self.program.programCounter = 0
		self.program.byteCodes = ['10000006', '11000003', 'A0100000', '11000005', '70100000', '60000000']
		self.program.execute()
		self.assertEquals(self.program.programCounter, 6)

	def test_current_instruction_code_to_run(self):
		self.program.byteCodes = ['10000006', '11000003', 'A0100000', '11000005', '70100000', '60000000']
		opcode = self.program.getInstructionToRun()
		self.assertEquals('1',opcode)

	def test_current_instruction_code_to_run_2(self):
		self.program.programCounter = 2
		self.program.byteCodes = ['10000006', '11000003', 'A0100000', '11000005', '70100000', '60000000']
		opcode = self.program.getInstructionToRun()
		self.assertEquals('A',opcode)

	def test_run_program_one(self):
		self.program.byteCodes = ['10000006', '11000003', 'A0100000', '11000005', '70100000', '60000000']
		self.program.execute()	
		self.assertEquals(self.program.stdOut,'7')

	def test_run_program_two(self):
		self.program.byteCodes = ['10000010', '60000000']
		self.program.execute()	
		self.assertEquals(self.program.stdOut,'16')

	def test_run_program_with_write(self):
		self.program.byteCodes = ['10000065', '60000000']
		self.program.execute()
		self.assertEquals('101',self.program.stdOut)	

	def test_run_program_with_JMP(self):
		# x0000099 = 153
		self.program.byteCodes = ['00000000','10000099','B0000004','11000001','70100000','60000000']
		self.program.execute()
		self.assertEquals('153',self.program.stdOut)	

	def test_run_program_with_JMP_Z(self):
		self.program.byteCodes = ['10000000','C0000003','10000014','60000000']
		self.program.execute()
		self.assertEquals('0',self.program.stdOut)	

	def test_run_program_with_JMP_Z_no_jump(self):
		self.program.byteCodes = ['10000001','C0000003','10000014','60000000']
		self.program.execute()
		self.assertEquals('20',self.program.stdOut)	

	def test_run_program_with_JMP_NZ(self):
		self.program.byteCodes = ['10000015','D0000003','10000014','60000000']
		self.program.execute()
		self.assertEquals('21',self.program.stdOut)	

	def test_run_program_with_JMP_NZ_no_jump(self):
		self.program.byteCodes = ['10000000','D0000003','10000014','60000000']
		self.program.execute()
		self.assertEquals('20',self.program.stdOut)	

	def test_run_program_with_JMP_GT(self):
		self.program.byteCodes = ['10000001','E0000003','10000014','60000000']
		self.program.execute()
		self.assertEquals('1',self.program.stdOut)	

	def test_run_program_with_JMP_GT_no_jump(self):
		self.program.byteCodes = ['10000001','11000005','80100000','E0000005','10000014','60000000']
		self.program.execute()
		self.assertEquals('20',self.program.stdOut)	

	def test_run_program_with_JMP_LT(self):
		self.program.byteCodes = ['10000001','11000005','80100000','F0000005','10000014','60000000']
		self.program.execute()
		self.assertEquals('-4',self.program.stdOut)	

	def test_run_program_with_JMP_LT_no_jump(self):
		self.program.byteCodes = ['10000001','11000005','F0000004','10000014','60000000']
		self.program.execute()
		self.assertEquals('20',self.program.stdOut)	

	def test_run_program_store_memory(self):
		self.program.byteCodes = ['10000008','11000001','14000005','41400000']
		self.program.execute()
		self.assertEquals(5,self.program.mem[1])			

	def test_run_program_print_expression(self):
		self.program.byteCodes = ['10000006','11000003','A0100000','11000005','70100000','60000000']
		self.program.execute()
		self.assertEquals('7',self.program.stdOut)			

	def test_run_program_input_plus_one(self):
		# replace user input command 4 (50000000) with put '1' into A
		# also fix error @line 7 to (B0000001)
		self.program.byteCodes = ['20400000','D0000007','11000001','10000001','70100000','60000000','B0000001','00000000']
		self.program.execute()
		self.assertEquals('2',self.program.stdOut)			

	def test_run_program_sum_of_input(self):
		# replace user input command 10 (50000000) with put '3000' into A
		self.program.byteCodes = ['15000000','10000000','45000000','20400000','D000000E','110003E8','30500000','80100000','E000000E','31500000','10000BB8','70100000','45000000','B0000003','30500000','60000000']
		self.program.execute()
		self.assertEquals('3000',self.program.stdOut)			

