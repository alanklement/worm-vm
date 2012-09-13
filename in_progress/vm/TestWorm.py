import unittest
from OpCodes import OpCodes

class TestWorm(unittest.TestCase):
	
	def setUp(self):
		self.opCodes = OpCodes()

	def test_main(self):
		print 'testing main'
