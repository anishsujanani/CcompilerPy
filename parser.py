from lexer import *

class parser:

	# Function creates internal lexer obj
	def __init__(self, filepath):
		self.lexer = lexer(filepath)
		

	# Entry point parser control function
	def beginParse(self):
		self.symbol_table = self.getSymbolTable()
		#print self.symbol_table
		#self.tryGrammars();
		for i in self.symbol_table:
			print i
	# Requests a token from the lexer
	def getSymbolTable(self):
		return self.lexer.tokenController()
		
	