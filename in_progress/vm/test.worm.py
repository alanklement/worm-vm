import unittest

import TestInstructions
import TestWorm
import TestProgramLoop

loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(TestInstructions)

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)