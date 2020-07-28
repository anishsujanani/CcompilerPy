from lexer import *

class parser:

	# Function creates internal lexer obj
	def __init__(self, filepath):
		self.lexer = lexer(filepath)
		self.cur_index = 0		
		self.parseStatus = False
		self.datatypes = ['int', 'float', 'char', 'double', 'void']
		self.stg_classes = ['auto', 'extern', 'register', 'static', 'volatile']


	# Entry point parser control function
	def beginParse(self):
		self.symbol_table = self.getSymbolTable()
		try:
			self.parseProgram()
			if self.parseStatus == True:
				print 'Parse successful'
			else:
				print 'Parse failed'
		except IndexError:
			print 'Bracket mismatch'


	# Requests a token from the lexer
	def getSymbolTable(self):
		return self.lexer.tokenController()

	def parseProgram(self):
		print '\n\nBeginning parsing: \n\n'
		print 'Length of token stream: %s\n\n' % len(self.symbol_table)

		while(self.cur_index < len(self.symbol_table)-1):
			self.parseStatus = self.parseImports()
			if self.parseStatus == False:
				self.parseStatus = self.parseExternalDec()
				while self.parseStatus == True:
					self.parseStatus = self.parseExternalDec()
				self.parseStatus = self.parseMainFunc()
				return self.parseStatus


	#include< header_file > header | e
	def parseImports(self):
		print '\n\n**** TRYING IMPORTS *******'
		temp_index = self.cur_index	
	
		if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '#':
			temp_index += 1
			
			if self.symbol_table[temp_index]['token_type'] == 'keyword' and self.symbol_table[temp_index]['value'] == 'include':
				temp_index += 1
				if self.symbol_table[temp_index]['token_type'] == 'relop' and self.symbol_table[temp_index]['value'] == '<':
					temp_index += 1
					
					if self.symbol_table[temp_index]['token_type'] == 'const' or self.symbol_table[temp_index]['token_type'] == 'identifier':
						temp_index += 1
						
						if self.symbol_table[temp_index]['token_type'] == 'relop' and self.symbol_table[temp_index]['value'] == '>':
							temp_index += 1
							self.cur_index += temp_index - self.cur_index
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
		print '\n\n**** TRYING EXTERNAL DECLARATIONS *******'
		temp_index = self.cur_index

		print 'Current', self.symbol_table[temp_index]
		if self.symbol_table[temp_index]['token_type'] == 'keyword' and self.symbol_table[temp_index]['value'] in self.stg_classes:
			temp_index += 1
			self.cur_index += temp_index - self.cur_index
			
			decStat_retval = self.parseDecStat()
			if decStat_retval == True:
				temp_index = self.cur_index
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
		print '\n\n**** TRYING DECLARATION STATEMENTS *******'
		temp_index = self.cur_index

		print 'Current', self.symbol_table[temp_index]
		if self.symbol_table[temp_index]['token_type'] == 'keyword':
			if self.symbol_table[temp_index]['value'] in self.datatypes:
				temp_index += 1

				if self.symbol_table[temp_index]['token_type'] == 'identifier':
					temp_index += 1
					while self.symbol_table[temp_index]['value'] == ',':
						temp_index += 1
						if self.symbol_table[temp_index]['token_type'] == 'identifier':
								temp_index += 1
						else:
							print 'Expected indentifier after ,'
							return False
					if self.symbol_table[temp_index]['value'] == '=':
						return False
					self.cur_index += temp_index - self.cur_index
					return True
				else:
					print 'Expected identifer'
					return False
			else:
				print 'Expected keyword, datatype id'
				return False
		

	#initializationStatement: dataType identifier assignmentOperator E 
	#                         | dataType multipleInitialization
    # multipleInitialization: identifier assignmentOperator E, multipleInitialization 
    #                         | identifier assignmentOperator E
	def parseInitialization(self):
		temp_index = self.cur_index
		print '\n\n**** TRYING INITIALIZATION *******'
		if self.symbol_table[temp_index]['token_type'] == 'keyword':
			if self.symbol_table[temp_index]['value'] in self.datatypes:
				temp_index += 1
				if self.symbol_table[temp_index]['token_type'] == 'identifier':
					temp_index += 1
					
					if self.symbol_table[temp_index]['token_type'] == 'asgnop':
						temp_index += 1
						self.cur_index += temp_index - self.cur_index
						expr_retval = self.parseExpr()
					
						if expr_retval == False:
							return False

						temp_index = self.cur_index
						while self.symbol_table[temp_index]['value'] == ',':
							temp_index += 1
							if self.symbol_table[temp_index]['token_type'] == 'identifier':
								temp_index += 1
								if self.symbol_table[temp_index]['token_type'] == 'asgnop':
									temp_index += 1
									self.cur_index += temp_index - self.cur_index
									expr_retval = self.parseExpr()
							
									if expr_retval == False:
										return False
				
					return True
				else:
					print 'Expected identifer'
					return False
			else:
				print 'Expected keyword, datatype id'
				return False


	#parseAsgn -> identifier asgnop E
	def parseAssignment(self):
		print '\n\n**** TRYING ASSIGNMENT *******'
		temp_index = self.cur_index
		if self.symbol_table[temp_index]['token_type'] == 'identifier':
			temp_index += 1
			if self.symbol_table[temp_index]['token_type'] == 'asgnop':
				temp_index += 1
				self.cur_index += temp_index - self.cur_index
				expr_retval = self.parseExpr()
				if expr_retval == False:
					return False
				return True


	# condStat -> if(statment){statement}
	def parseCond(self):
		print '\n\n**** TRYING CONDITIONAL *******'
		temp_index = self.cur_index
		if self.symbol_table[temp_index]['token_type'] == 'keyword' and self.symbol_table[temp_index]['value'] == 'if':
			temp_index += 1
			if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '(':
				# STATEMENTS
				temp_index += 1
				if self.symbol_table[temp_index]['token_type'] == 'identifier':
					temp_index += 1
					if self.symbol_table[temp_index]['token_type'] == 'relop':
						temp_index += 1
						# check for expr here
						self.cur_index += temp_index - self.cur_index
						expr_retval = self.parseExpr()
						if expr_retval == True:
							temp_index = self.cur_index
							if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ')':
								temp_index += 1
								if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '{':
									temp_index += 1
									self.cur_index += temp_index - self.cur_index
									# STATEMENTS
									statement_retval = self.parseStatements()
									while statement_retval == True:
										statement_retval = self.parseStatements()

									temp_index = self.cur_index
									if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '}':
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
							print 'Expression error'
							return False

					else:
						print 'Expected relop'
						return False
				else:
					print 'Expected identifier'
					return False
			else:
				print 'Expected ('
				return False
		else:
			return False


	# E1, E2 use this
	# can be blank, ie. next = ;, can be identifier alone, can be assignment, 
	# can be declaration, initialization. relop, inc/decop
	def parseForE1(self):
		temp_index = self.cur_index
		print ' ************ CHECKING FOR CONDITION: ******* ', self.symbol_table[temp_index]
		
		# blank, ie. ;
		if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ';':
			temp_index += 1
			self.cur_index += temp_index - self.cur_index
			return True		

		# assignment
		asgn_retval = self.parseAssignment()
		if asgn_retval == True:
			temp_index = self.cur_index
			if self.symbol_table[temp_index]['value'] == ';':
				temp_index += 1
				self.cur_index += temp_index - self.cur_index
				return True

		# declaration:
		decStat_retval = self.parseDecStat()
		if decStat_retval == True:
			temp_index = self.cur_index
			if self.symbol_table[temp_index]['value'] == ';':
				temp_index += 1
				self.cur_index += temp_index - self.cur_index
				return True

		# initialization
		init_retval = self.parseInitialization()
		if init_retval == True:
			temp_index = self.cur_index
			if self.symbol_table[temp_index]['value'] == ';':
				temp_index += 1
				self.cur_index += temp_index - self.cur_index
				return True

		# identifier
		if self.symbol_table[temp_index]['token_type'] == 'identifier':
			temp_index += 1
			#identifier alone
			if self.symbol_table[temp_index]['value'] == ';':
				temp_index += 1
				self.cur_index += temp_index - self.cur_index
				return True
			else:
				temp_index -= 1
		
		# id relop E
		if self.symbol_table[temp_index]['token_type'] == 'identifier':
			temp_index += 1
			if self.symbol_table[temp_index]['token_type'] == 'relop':
				temp_index += 1
				self.cur_index += temp_index - self.cur_index
				expr_retval = self.parseExpr()
				temp_index = self.cur_index
				if self.symbol_table[temp_index]['value'] == ';':
					temp_index += 1
					self.cur_index += temp_index - self.cur_index
					return True
			else:
				temp_index -= 1

		# identifier incop|decop
		if self.symbol_table[temp_index]['token_type'] == 'identifier':
			temp_index += 1
			#identifier alone
			if self.symbol_table[temp_index]['token_type'] in ['incop', 'decop']:
				temp_index += 1
				if self.symbol_table[temp_index]['value'] == ';':
					temp_index += 1
					self.cur_index += temp_index - self.cur_index
					return True
				else:
					return False
			else:
				temp_index -= 1

		#  incop|decop identifier
		if self.symbol_table[temp_index]['token_type'] in ['decop', 'incop']:
			temp_index += 1
			#identifier alone
			if self.symbol_table[temp_index]['token_type'] == 'identifier':
				temp_index += 1
				if self.symbol_table[temp_index]['value'] == ';':
					temp_index += 1
					self.cur_index += temp_index - self.cur_index
					return True
				else:
					return False
			else:
				temp_index -= 1
				return False

		return False

	

	# E3 Uses this
	# can be blank, ie. next = ), can be identifier alone, can be assignment, can be declaration
	def parseForE3(self):
		temp_index = self.cur_index
		print '*********** CHECKING FOR CONDITION: ******* ', self.symbol_table[temp_index]
		
		# blank, ie. ;
		if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ')':
			#temp_index += 1
			#self.cur_index += temp_index - self.cur_index
			return True		

		# assignment
		asgn_retval = self.parseAssignment()
		if asgn_retval == True:
			temp_index = self.cur_index
			return True

		# declaration:
		decStat_retval = self.parseDecStat()
		if decStat_retval == True:
			temp_index = self.cur_index
			return True

		# initialization
		init_retval = self.parseInitialization()
		if init_retval == True:
			temp_index = self.cur_index
			return True

		# identifier
		if self.symbol_table[temp_index]['token_type'] == 'identifier':
			temp_index += 1
			#identifier alone
			if self.symbol_table[temp_index]['value'] == ')':
				self.cur_index += temp_index - self.cur_index
				return True
			else:
				temp_index -= 1
	

		# id relop|logop E
		if self.symbol_table[temp_index]['token_type'] == 'identifier':
			temp_index += 1
			if self.symbol_table[temp_index]['token_type'] in ['relop', 'logop']:
				temp_index += 1
				self.cur_index += temp_index - self.cur_index
				expr_retval = self.parseExpr()
				return True
			else:
				temp_index -= 1

		# identifier incop|decop
		if self.symbol_table[temp_index]['token_type'] == 'identifier':
			temp_index += 1
			#identifier alone
			if self.symbol_table[temp_index]['token_type'] in ['incop', 'decop']:
				temp_index += 1
				if self.symbol_table[temp_index]['value'] == ')':
					#temp_index += 1
					self.cur_index += temp_index - self.cur_index
					return True
				else:
					return False
			else:
				temp_index -= 1

		#  incop|decop identifier
		if self.symbol_table[temp_index]['token_type'] in ['decop', 'incop']:
			temp_index += 1
			#identifier alone
			if self.symbol_table[temp_index]['token_type'] == 'identifier':
				temp_index += 1
				if self.symbol_table[temp_index]['value'] == ')':
					#temp_index += 1
					self.cur_index += temp_index - self.cur_index
					return True
				else:
					return False
			else:
				temp_index -= 1
				return False

		return False





	# for(assignmentStatement, identifier relop E; identifier decop/incop)
	# for(E1, E2; E3)
	def parseFor(self):
		print '********** TRYING FOR STATEMENT ***********'
		temp_index = self.cur_index
		if self.symbol_table[temp_index]['token_type'] == 'keyword' and self.symbol_table[temp_index]['value'] == 'for':
			temp_index += 1
			if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '(':
				temp_index += 1
			
				self.cur_index += temp_index - self.cur_index

				forcond = self.parseForE1()
				if forcond == True:
					forcond = self.parseForE1()
					if forcond == True:
						forcond = self.parseForE3()
				
				if forcond == False:
					return False

				temp_index = self.cur_index 

				if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ')':
					temp_index += 1
					if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '{':
						temp_index += 1
						self.cur_index += temp_index - self.cur_index
						
						# STATEMENTS
						statement_retval = self.parseStatements()
						while statement_retval == True:
							statement_retval = self.parseStatements()

						if statement_retval == False and self.symbol_table[self.cur_index]['value'] == '}':
							print 'Parse failed'
							exit(0);


						temp_index = self.cur_index															# statements
				 		if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '}':
							temp_index += 1
							self.cur_index += temp_index - self.cur_index
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
			return False


	# main: int main(){statements} | int main(int argc, char *argv[]){statements}
	def parseMainFunc(self):
		print '\n\n**** TRYING MAIN FUNCTION *******'
		temp_index = self.cur_index	
	
		if self.symbol_table[temp_index]['token_type'] == 'keyword' and self.symbol_table[temp_index]['value'] in self.datatypes:
			temp_index += 1
			
			if self.symbol_table[temp_index]['token_type'] == 'identifier' and self.symbol_table[temp_index]['value'] == 'main':
				temp_index += 1
				if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '(':
					temp_index += 1
					
					if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ')':
						temp_index += 1
						
						if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '{':
							temp_index += 1
							self.cur_index += temp_index - self.cur_index


							print '\n\n**** TRYING STATEMENTS *******'
							# STATEMENTS
							statement_retval = self.parseStatements()
							while statement_retval == True:
								statement_retval = self.parseStatements()



							temp_index = self.cur_index
							if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '}':
								temp_index += 1
								self.cur_index += temp_index - self.cur_index
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


	# return -> return E | return id
	def parseReturn(self):
		print '\n\n**** TRYING RETURN *******'
		temp_index = self.cur_index
		if self.symbol_table[temp_index]['token_type'] == 'keyword' and self.symbol_table[temp_index]['value'] == 'return':
			temp_index += 1
			# return
			if self.symbol_table[temp_index]['value'] == ';':
				self.cur_index += temp_index - self.cur_index
				return True
			# return EXPR
			else:
				self.cur_index += temp_index - self.cur_index	
				expr_retval = self.parseExpr();
				temp_index = self.cur_index
				if expr_retval == True:
					temp_index = self.cur_index
					return True
				# return a; return 'a';
				elif expr_retval == False:
					if self.symbol_table[temp_index]['token_type'] in ['identifier', 'const']:
						temp_index += 1
						self.cur_index += temp_index - self.cur_index
						return True


	# spfunc -> printf(const, E|id)
	def parseSPFunc(self):
		print '\n\n**** TRYING SPECIAL FUNCTIONS *******'
		temp_index = self.cur_index
		if self.symbol_table[temp_index]['token_type'] == 'spfuncs':
			temp_index += 1
			if self.symbol_table[temp_index]['value'] == '(':
				temp_index += 1
				if self.symbol_table[temp_index]['value'] == '"':
					temp_index += 1
					if self.symbol_table[temp_index]['token_type'] == 'const':
						temp_index += 1
						if self.symbol_table[temp_index]['value'] == '"':
							temp_index += 1
							if self.symbol_table[temp_index]['value'] == ')':
								temp_index += 1
								self.cur_index += temp_index - self.cur_index
								return True
						else:
							print 'Expected closing "'
							return False
							
							

						if self.symbol_table[temp_index]['value'] == ',':
							temp_index += 1
							if self.symbol_table[temp_index]['token_type'] == 'identifier':
								temp_index += 1
								while self.symbol_table[temp_index]['value'] == ',':
									temp_index += 1
									if self.symbol_table[temp_index]['token_type'] == 'identifier':
										temp_index += 1
									else:
										print 'Expected indentifier after ,'
										return False
							else:
								self.cur_index += temp_index - self.cur_index
								expr_retval = self.parseExpr()
								temp_index = self.cur_index
								if expr_retval == False or expr_retval == None:
									return False
								while self.symbol_table[temp_index]['value'] == ',':
									temp_index += 1
									self.cur_index += temp_index - self.cur_index
									expr_retval = self.parseExpr()
									temp_index = self.cur_index
									#temp_index += 1
									if expr_retval == False or expr_retval == None:
										return False

						else:
							print 'Expected parameter after ,'
							return False

					if self.symbol_table[temp_index]['value'] == ')':
							temp_index += 1
							self.cur_index += temp_index - self.cur_index
							return True
					else:
						print 'Expected )'
						return False
				else:
					print 'Expected opening "'
					return False
			else:
				print 'Expected opening ('
				return False


	# statements:	declarationStatement ; | initializationStatement ; | assignmentStatement ; | conditionalStatement ; |
	#          for(initialization; assignment; expr) {statements}
	def parseStatements(self):
		temp_index = self.cur_index
		temp_index_copy = self.cur_index
		# FIRST TRY SINGLE OR MULTIPLE DECLARATION STATEMENTS
		retval = self.parseDecStat()
		if retval == True:
			temp_index = self.cur_index 
			if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ';':
				temp_index += 1
				self.cur_index += temp_index - self.cur_index
				return True
		else: # IF DECSTAT DOESN'T WORK, GO BACK TO OLD_INDEX AND TRY INITIALIZATION
			#	print 'Expected ;'
				self.cur_index = temp_index_copy
				retval = self.parseInitialization()
				if retval == True:
					temp_index = self.cur_index 
					if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ';':
						temp_index += 1
						self.cur_index += temp_index - self.cur_index
						return True
					else:
						print 'Expected ;'
						return False
						# INITSTAT DIDN'T WORK, TRY ASSIGNMENT
				else:
					self.cur_index = temp_index_copy
					retval = self.parseAssignment()
					if retval == True:
						temp_index = self.cur_index
						print 'RETURN ******Current', self.symbol_table[temp_index]
						if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ';':
							temp_index += 1
							self.cur_index += temp_index - self.cur_index
							return True
						else:
							print 'Expected ;'
							return False
					else: # ASGNSTAT DIDN:T WORK, TRY FOR LOOP
						self.cur_index = temp_index_copy
						retval = self.parseFor()
						if retval == True:
							temp_index = self.cur_index
							return True
						else: # try conditional
							self.cur_index = temp_index_copy
							retval = self.parseCond()
							if retval == True:
								temp_index = self.cur_index
								return True
							else: # Try return statement
								self.cur_index = temp_index_copy
								print '*********** TRYING RETURN ********'
								retval = self.parseReturn()
								if retval == True:
									temp_index = self.cur_index
									if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ';':
										temp_index += 1
										self.cur_index += temp_index - self.cur_index
										return True
								else: #try printf()
									print '*********** TRYING SP FUNCTIONS ********'
									self.cur_index = temp_index_copy
									retval = self.parseSPFunc()
									if retval == True:
										temp_index = self.cur_index
										if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ';':
											temp_index += 1
											self.cur_index += temp_index - self.cur_index
											return True 
										else:
											print 'Coudn\'t match construct, going back'
											return False

					# else: # ASSIGNMENT DIDNT WORK, TRY CONDITIONAL
					# 	self.cur_index = temp_index_copy
					# 	print '********** TRYING CONDSTAT **********'
					# 	retval = self.parseCond()
					# 	if retval == True:
					# 		temp_index = self.cur_index
					# 	else:
					# 		return False
		


	def parseExpr(self):
		temp_index = self.cur_index
		# E->F E1
		e_retval = self.E()
		return e_retval

	def E(self):
		# E->F E1
		temp_index = self.cur_index
		# F-> G F1
		f_retval = self.F()
		if f_retval == True:
			temp_index = self.cur_index
			e1_retval = self.E1()
			return e1_retval
		else:
			return False

	def F(self):
		temp_index = self.cur_index
		# F-> G F1
		g_retval = self.G()
		if g_retval == True:
			temp_index = self.cur_index
			f1_retval = self.F1()
			return f1_retval
		else:
			return False
	def G(self):
		temp_index = self.cur_index
		# G-> H G1
		h_retval = self.H()
		if h_retval == True:
			temp_index = self.cur_index
			g1_retval = self.G1()
			return g1_retval
		else:
			return False

	def H(self):
		temp_index = self.cur_index
		# H-> I H1
		i_retval = self.I()
		if i_retval == True:
			temp_index = self.cur_index
			h1_retval = self.H1()
			return h1_retval
		else:
		 return False

	def I(self):
		temp_index = self.cur_index
		# I-> - I | identifier | number
		if self.symbol_table[temp_index]['token_type'] == 'arithop' and self.symbol_table[temp_index]['value'] == '-':
			temp_index += 1
			self.cur_index += temp_index - self.cur_index
			i_retval = self.I()
			return i_retval

		elif self.symbol_table[temp_index]['token_type'] == 'identifier':
			temp_index += 1
			self.cur_index += temp_index - self.cur_index
			return True
		elif self.symbol_table[temp_index]['token_type'] == 'const':
			temp_index += 1
			self.cur_index += temp_index - self.cur_index
			return True
		else:
			return False

	def H1(self):
		# H1: / I H1 | e
		temp_index = self.cur_index
		if self.symbol_table[temp_index]['token_type'] == 'arithop' and self.symbol_table[temp_index]['value'] == '/':
			temp_index += 1
			self.cur_index += temp_index - self.cur_index
			i_retval = self.I()
			if i_retval == True:
				temp_index = self.cur_index
				h1_retval = self.H1()
				return h1_retval
		else:
			return True

	
	def G1(self):
		# G1 -> * H G1 | e
		temp_index = self.cur_index
		if self.symbol_table[temp_index]['token_type'] == 'arithop' and self.symbol_table[temp_index]['value'] == '*':
			temp_index += 1
			self.cur_index += temp_index - self.cur_index
			h_retval = self.H()
			if h_retval == True:
				temp_index = self.cur_index
				g1_retval = self.G1()
				return g1_retval
		else:
			return True

	def F1(self):
		# F1: - G F1 | e
		temp_index = self.cur_index
		if self.symbol_table[temp_index]['token_type'] == 'arithop' and self.symbol_table[temp_index]['value'] == '-':
			temp_index += 1
			self.cur_index += temp_index - self.cur_index
			g_retval = self.G()
			if g_retval == True:
				temp_index = self.cur_index
				f1_retval = self.F1()
				return f1_retval
		else:
			return True

	def E1(self):
		# E1: + F E1 | e
		temp_index = self.cur_index
		if self.symbol_table[temp_index]['token_type'] == 'arithop' and self.symbol_table[temp_index]['value'] == '+':
			temp_index += 1
			self.cur_index += temp_index - self.cur_index
			f_retval = self.F()
			if f_retval == True:
				temp_index = self.cur_index
				e1_retval = self.E1()
				return e1_retval


		else:
			return True



