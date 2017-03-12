from lexer import *

class parser:


	# Function creates internal lexer obj
	def __init__(self, filepath):
		self.lexer = lexer(filepath)
		self.cur_index = 0		

	# Entry point parser control function
	def beginParse(self):
		self.symbol_table = self.getSymbolTable()
		#print self.symbol_table
		#self.tryGrammars();
		for i in self.symbol_table:
			print i

		# E -> TE'
		# E' -> +TE' | EPSILON
		# for now, let t = id

		print self.E()

	def E(self):
		print 'calling t'
		if self.T() == True:
			print 'calling edash'
			if self.Edash() == True:
				return 'parsed'


	def T(self):
		if self.symbol_table[self.cur_index]['token_type'] == 'const' or self.symbol_table[self.cur_index]['token_type'] == 'identifier':
			self.cur_index += 1
			return True
		else:
			return False

	def Edash(self):
		if self.symbol_table[self.cur_index]['value'] == '+':
			self.cur_index += 1
			if self.symbol_table[self.cur_index]['token_type'] == 'const' or self.symbol_table[self.cur_index]['token_type'] == 'identifier':
				return True
		else:
			return False

	
	# Requests a token from the lexer
	def getSymbolTable(self):
		return self.lexer.tokenController()
		
	