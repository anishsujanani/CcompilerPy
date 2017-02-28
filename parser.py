from lexer import *

class parser:

	# Function creates internal lexer obj
	def __init__(self, filepath):
		self.lexer = lexer(filepath)

	# Entry point parser control function
	def beginParse(self):
		self.getSymbolTable()

	# Requests a token from the lexer
	def getSymbolTable(self):
		self.symbol_table = self.lexer.tokenController()
		print 'Symbol table returned to parser: ', self.symbol_table

	