import unittest

import TestInstructions

loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(TestInstructions)

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)