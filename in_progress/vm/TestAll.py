import unittest

import TestInstructions
import TestWorm
import TestProgramLoop

loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(TestInstructions)
# suite.addTests(loader.loadTestsFromModule(TestWorm))
# suite.addTests(loader.loadTestsFromModule(TestProgramLoop))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)