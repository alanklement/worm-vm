import argparse

class ArguementReader(object):

	def listenForArguements(self):
		self.parser = argparse.ArgumentParser()
		self.addArguments()
		self.shareArguments()

	def addArguments(self):
		self.parser.add_argument("file",
		 					 help="WORM needs a bytecode file to execute",
		 					 type=file)
		self.parser.add_argument("-v", "--verbose",  action="count",default=0, help="Sets verbose level. Use 'vv' for extra info")
		
	def shareArguments(self):
		args = self.parser.parse_args()

		self.file = args.file
		self.verboseLevel = args.verbose


