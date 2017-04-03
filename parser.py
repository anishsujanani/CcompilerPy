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
		
		print 'Current', self.symbol_table[temp_index]
		if self.symbol_table[temp_index]['token_type'] == 'keyword':
			if self.symbol_table[temp_index]['value'] in self.datatypes:
				temp_index += 1
				print 'HERE 123'
				print 'Current', self.symbol_table[temp_index]
				if self.symbol_table[temp_index]['token_type'] == 'identifier':
					temp_index += 1
					print 'Current', self.symbol_table[temp_index]
					
					if self.symbol_table[temp_index]['token_type'] == 'asgnop':
						print '*******************Going to parseExpr()'
						temp_index += 1
						print 'Current', self.symbol_table[temp_index]
						self.cur_index += temp_index - self.cur_index
						expr_retval = self.parseExpr()
					
						if expr_retval == False:
							return False

						temp_index = self.cur_index
						print 'NEXT: ', self.symbol_table[temp_index]
						while self.symbol_table[temp_index]['value'] == ',':
							temp_index += 1
							expr_retval = self.parseExpr()

						if expr_retval == False:
							return False
					# while self.symbol_table[temp_index]['value'] == ',':
					# 	temp_index += 1
					# 	print 'Current', self.symbol_table[temp_index]
					# 	if self.symbol_table[temp_index]['token_type'] == 'identifier':
					# 			temp_index += 1
					# 	else:
					# 		print 'Expected indentifier after ,'
					# 		return False
					
					#self.cur_index += temp_index - self.cur_index
					return True
				else:
					print 'Expected identifer'
					return False
			else:
				print 'Expected keyword, datatype id'
				return False


	#parseAsgn -> identifier asgnop E
	def parseAssignment(self):
		temp_index = self.cur_index
		if self.symbol_table[temp_index]['token_type'] == 'identifier':
			temp_index += 1
			if self.symbol_table[temp_index]['token_type'] == 'asgnop':
				temp_index += 1
				self.cur_index += temp_index - self.cur_index
				print 'TRYING EXPR with: ', self.symbol_table[temp_index]
				expr_retval = self.parseExpr()
				if expr_retval == False:
					return False
				return True


	# condStat -> if(statment){statement}
	def parseCond(self):
		temp_index = self.cur_index
		print 'STARINT COND CURRENT: ', self.symbol_table[temp_index]
		if self.symbol_table[temp_index]['token_type'] == 'keyword' and self.symbol_table[temp_index]['value'] == 'if':
			temp_index += 1
			print 'CURRENT: ', self.symbol_table[temp_index]
			if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '(':
				# STATEMENTS
				temp_index += 1
				self.cur_index += temp_index - self.cur_index
				
				statement_retval = self.parseStatements()
				while statement_retval == True:
					statement_retval = self.parseStatements()

				temp_index = self.cur_index
				print 'CURRENT: ', self.symbol_table[temp_index]
				if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ')':
					temp_index += 1
					print 'CURRENT: ', self.symbol_table[temp_index]
					if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '{':
						temp_index += 1
						# STATEMENTS
						statement_retval = self.parseStatements()
						while statement_retval == True:
							statement_retval = self.parseStatements()

						temp_index = self.cur_index
						print 'NOW123: ', self.symbol_table[temp_index]
						if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '}':
							print 'NOW234: ', self.symbol_table[temp_index]
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

	# for(assignmentStatement, identifier relop E; identifier decop/incop)
	def parseFor(self):
		print '********** TRYING FOR STATEMENT ***********'
		temp_index = self.cur_index
		print 'parseFor(): ', self.symbol_table[temp_index]
		if self.symbol_table[temp_index]['token_type'] == 'keyword' and self.symbol_table[temp_index]['value'] == 'for':
			temp_index += 1
			if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '(':
				temp_index += 1
				self.cur_index += temp_index - self.cur_index
				asgn_retval = self.parseAssignment()
				if asgn_retval == True:
						temp_index = self.cur_index
						print 'RETURN ******Current', self.symbol_table[temp_index]
						if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ';':
							temp_index += 1
							self.cur_index += temp_index - self.cur_index
							print '*****Current', self.symbol_table[temp_index]
							if self.symbol_table[temp_index]['token_type'] == 'identifier':
								temp_index += 1
								print '*****Current', self.symbol_table[temp_index]
								if self.symbol_table[temp_index]['token_type'] == 'relop':
									temp_index += 1
									print '*****Current', self.symbol_table[temp_index]
									self.cur_index += temp_index - self.cur_index
									expr_retval = self.parseExpr()
									print expr_retval
									if expr_retval == True:
										temp_index = self.cur_index
										print '1234 RETURN ******Current', self.symbol_table[temp_index]
										if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ';':
											temp_index += 1
											self.cur_index += temp_index - self.cur_index
											#print 'WNENGTKLENSGLKSDNGSD', self.symbol_table[temp_index]
											print '*****Current', self.symbol_table[temp_index]
											if self.symbol_table[temp_index]['token_type'] == 'identifier':
												temp_index += 1
												print '*****Current', self.symbol_table[temp_index]
												if self.symbol_table[temp_index]['token_type'] == 'incop' or self.symbol_table[temp_index]['token_type'] == 'decop':
													temp_index += 1
													print '*****Current', self.symbol_table[temp_index]
													if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ')':
														temp_index += 1
														print '*****Current', self.symbol_table[temp_index]
														if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '{':
															temp_index += 1
															self.cur_index += temp_index - self.cur_index

															# STATEMENTS
															statement_retval = self.parseStatements()
															while statement_retval == True:
																statement_retval = self.parseStatements()



															temp_index = self.cur_index
															# statements
															print '*****Current', self.symbol_table[temp_index]
														if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == '}':
															self.cur_index += temp_index - self.cur_index
															return True
							
						else:
							print 'Expected ;'
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



	# statements:	declarationStatement ; | initializationStatement ; | assignmentStatement ; | conditionalStatement ; |
	#          for(initialization; assignment; expr) {statements}
	def parseStatements(self):
		temp_index = self.cur_index
		temp_index_copy = self.cur_index
		# FIRST TRY SINGLE OR MULTIPLE DECLARATION STATEMENTS
		print '******** TRYING DECSTAT ****'
		retval = self.parseDecStat()
		print retval
		if retval == True:
			temp_index = self.cur_index 
			print 'Current', self.symbol_table[temp_index]
			if self.symbol_table[temp_index]['token_type'] == 'punctuation' and self.symbol_table[temp_index]['value'] == ';':
				temp_index += 1
				self.cur_index += temp_index - self.cur_index
				return True
		else: # IF DECSTAT DOESN'T WORK, GO BACK TO OLD_INDEX AND TRY INITIALIZATION
			#	print 'Expected ;'
				print '******** TRYING INITSTAT ****'
				self.cur_index = temp_index_copy
				print 'TRY: ', self.symbol_table[self.cur_index]
				retval = self.parseInitialization()
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
						# INITSTAT DIDN'T WORK, TRY ASSIGNMENT
				else:
					self.cur_index = temp_index_copy
					print '*********** TRING ASGN STAT ***********'
					print 'TRY: ', self.symbol_table[temp_index]
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
						print 'ABOUT TO DO: ', self.symbol_table[self.cur_index]
						retval = self.parseFor()
						if retval == True:
							temp_index = self.cur_index
							return True
					# else: # ASSIGNMENT DIDNT WORK, TRY CONDITIONAL
					# 	self.cur_index = temp_index_copy
					# 	print '********** TRYING CONDSTAT **********'
					# 	print self.symbol_table[self.cur_index]
					# 	retval = self.parseCond()
					# 	if retval == True:
					# 		temp_index = self.cur_index
					# 	else:
					# 		return False
		


	def parseExpr(self):
		temp_index = self.cur_index
		# E->F E1
		e_retval = self.E()
		print 'parseExpr(): ', e_retval
		return e_retval

	def E(self):
		# E->F E1
		temp_index = self.cur_index
		# F-> G F1
		f_retval = self.F()
		if f_retval == True:
			temp_index = self.cur_index
			e1_retval = self.E1()
			print 'e1 retval from e: ', e1_retval
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
			print 'f1 retval forom f: ', f1_retval
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
			print 'g1 val from g: ', g1_retval
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
			print 'h1 val from h : ', h1_retval
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


		else:
			return True










