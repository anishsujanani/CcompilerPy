from lexer import *

class parser:


	# Function creates internal lexer obj
	def __init__(self, filepath):
		self.lexer = lexer(filepath)
		self.cur_index = 0		
		self.parseStatus = False



	# Entry point parser control function
	def beginParse(self):
		self.symbol_table = self.getSymbolTable()
		#print self.symbol_table
		#self.tryGrammars();
		for i in self.symbol_table:
			print i


		self.parseProgram()
		if self.parseStatus == True:
			print 'Parse successful'
		else:
			print 'Parse failed'



	# Requests a token from the lexer
	def getSymbolTable(self):
		return self.lexer.tokenController()



	def parseProgram(self):
		print '\n\nBeginning parsing: \n\n'
		print 'Length of token stream: %s\n\n' % len(self.symbol_table)
		while(self.cur_index < len(self.symbol_table)-1):
			self.parseStatus = self.parseImports()

			'''if self.parseStatus == False:
										self.parseStatus = self.parseExternalDec()
										if self.parseStatus == False:
											self.parseMainFunc()'''
		return self.parseStatus

	#include< header_file > header | e
	def parseImports(self):
		print 'Current index: %s' % self.cur_index
		temp_index = self.cur_index	
		print 'Current', self.symbol_table[temp_index]
		if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '#':
			temp_index += 1
			if self.symbol_table[temp_index]['token_type'] == 'keyword' and self.symbol_table[temp_index]['value'] == 'include':
				print 'Current', self.symbol_table[temp_index]
				temp_index += 1
				if self.symbol_table[temp_index]['token_type'] == 'relop' and self.symbol_table[temp_index]['value'] == '<':
					print 'Current', self.symbol_table[temp_index]
					temp_index += 1
					if self.symbol_table[temp_index]['token_type'] == 'const' or self.symbol_table[temp_index]['token_type'] == 'identifier':
						print 'Current', self.symbol_table[temp_index]
						temp_index += 1
						if self.symbol_table[temp_index]['token_type'] == 'relop' and self.symbol_table[temp_index]['value'] == '>':
							print temp_index
							print 'Current', self.symbol_table[temp_index]
							temp_index += 1
							self.cur_index += temp_index
							print self.cur_index
							return True

		else:
			return False

