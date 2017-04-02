from lexer import *

class parser:


	# Function creates internal lexer obj
	def __init__(self, filepath):
		self.lexer = lexer(filepath)
		self.cur_index = 0		
		self.parseStatus = False
		self.datatypes = ['int', 'float', 'char', 'double', 'void']
		self.stg_classes = ['auto', 'extern', 'register', 'static']


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
			if self.parseStatus == False:
				print 'PARSE EXT SADFISDJGSNDGLSFNG'
				self.parseStatus = self.parseExternalDec()
				while self.parseStatus == True:
					self.parseStatus = self.parseExternalDec()
				print 'PARSE MAIN SADFISDJGSNDGLSFNG'
				self.parseStatus = self.parseMainFunc()
				return self.parseStatus


	#include< header_file > header | e
	def parseImports(self):
		print 'Current index: %s' % self.cur_index
		temp_index = self.cur_index	
	
		print 'Current', self.symbol_table[temp_index]
		if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '#':
			temp_index += 1
			
			print 'Current', self.symbol_table[temp_index]
			if self.symbol_table[temp_index]['token_type'] == 'keyword' and self.symbol_table[temp_index]['value'] == 'include':
				temp_index += 1
				print 'Current', self.symbol_table[temp_index]
				if self.symbol_table[temp_index]['token_type'] == 'relop' and self.symbol_table[temp_index]['value'] == '<':
					temp_index += 1
					
					print 'Current', self.symbol_table[temp_index]
					if self.symbol_table[temp_index]['token_type'] == 'const' or self.symbol_table[temp_index]['token_type'] == 'identifier':
						temp_index += 1
						
						print 'Current', self.symbol_table[temp_index]
						if self.symbol_table[temp_index]['token_type'] == 'relop' and self.symbol_table[temp_index]['value'] == '>':
							temp_index += 1
							self.cur_index += temp_index - self.cur_index
							print 'Current idex: ', self.cur_index
							return True

						else:
							print 'Expected >'
							return False
					else:
						print 'Expected a constant'
						return False
				else:
						print 'Expected <'
						return False
			else:
				print 'Expected include'
				return False
			
		else:
			print 'Expected #'
			return False


	# externalDec: extern|auto decStat ;
	def parseExternalDec(self):
		temp_index = self.cur_index

		print 'Current', self.symbol_table[temp_index]
		if self.symbol_table[temp_index]['token_type'] == 'keyword' and self.symbol_table[temp_index]['value'] in self.stg_classes:
			temp_index += 1
			self.cur_index += temp_index - self.cur_index
			
			decStat_retval = self.parseDecStat()
			if decStat_retval == True:
				temp_index = self.cur_index
				print 'Current', self.symbol_table[temp_index]
				if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ';':
					temp_index += 1
					self.cur_index = temp_index
					return True
				else:
					print 'Expected ; or ,'
					return False
			else:
				return False

	

	# decStat: dataType identifier | dataType multipleDeclaration
	def parseDecStat(self):
		temp_index = self.cur_index

		print 'Current', self.symbol_table[temp_index]
		if self.symbol_table[temp_index]['token_type'] == 'keyword':
			if self.symbol_table[temp_index]['value'] in self.datatypes:
				temp_index += 1

				print 'Current', self.symbol_table[temp_index]
				if self.symbol_table[temp_index]['token_type'] == 'identifier':
					temp_index += 1
					print 'Current', self.symbol_table[temp_index]
					while self.symbol_table[temp_index]['value'] == ',':
						temp_index += 1
						print 'Current', self.symbol_table[temp_index]
						if self.symbol_table[temp_index]['token_type'] == 'identifier':
								temp_index += 1
						else:
							print 'Expected indentifier after ,'
							return False
					
					self.cur_index += temp_index - self.cur_index
					return True
				else:
					print 'Expected identifer'
					return False
			else:
				print 'Expected keyword, datatype id'
				return False
		



	# main: int main(){statements} | int main(int argc, char *argv[]){statements}
	def parseMainFunc(self):
		print 'Current index: %s' % self.cur_index
		temp_index = self.cur_index	
	
		print 'Current', self.symbol_table[temp_index]
		if self.symbol_table[temp_index]['token_type'] == 'keyword' and self.symbol_table[temp_index]['value'] in self.datatypes:
			print 'TRYING:',self.symbol_table[temp_index]
			temp_index += 1
			
			print 'Current', self.symbol_table[temp_index]
			if self.symbol_table[temp_index]['token_type'] == 'identifier' and self.symbol_table[temp_index]['value'] == 'main':
				temp_index += 1
				print 'Current', self.symbol_table[temp_index]
				if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '(':
					temp_index += 1
					
					print 'Current', self.symbol_table[temp_index]
					if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ')':
						temp_index += 1
						
						print 'Current', self.symbol_table[temp_index]
						if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '{':
							temp_index += 1
							self.cur_index += temp_index - self.cur_index

							# STATEMENTS
							# statements:	declarationStatement ; | initializationStatement ; | assignmentStatement ; | conditionalStatement ; |
							#do{statements} while(condition);
							statement_retval = self.parseStatements()
							while statement_retval == True:
								statement_retval = self.parseStatements()

							temp_index = self.cur_index
							print 'Current', self.symbol_table[temp_index]
							if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '}':
								temp_index += 1
							
								self.cur_index += temp_index - self.cur_index
								print 'Current idex: ', self.cur_index
								return True

							else:
								print 'Expected }'
								return False
						else:
							print 'Expected {'
							return False
					else:
						print 'Expected )'
						return False
				else:
					print 'Expected ('
					return False
			
		else:
			print 'Expected int'
			return False


	def parseStatements(self):
		retval = self.parseDecStat()
		if retval == True:
			temp_index = self.cur_index 
			print 'Current', self.symbol_table[temp_index]
			if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ';':
				temp_index += 1
				self.cur_index += temp_index - self.cur_index
				return True
			else:
				print 'Expected ;'
				return False
		else:
			return False