import os.path
import re

class lexer:


	# Function assigns param filepath to internal var, opens file
	# in read mode
	def __init__(self, filepath):
		self.filepath = filepath
		self.fileobj = open(filepath, 'r')
		self.filecontent = self.formatFile()
		self.setPatterns()
		self.setLexemePtrs()
		self.token_stream = []



	

	# Function that initialized patterns to look for as internal vars
	def setPatterns(self):
		self.keywords = ['auto', 'double', 'int', 'struct', 'break',	
						'else', 'long', 'switch', 'case', 'enum', 
						'register',	'typedef', 'char', 'extern', 'return',
						'union', 'const', 'float', 'short', 'unsigned',
						'continue', 'for', 'signed', 'void', 'default',	
						'goto', 'sizeof', 'volatile', 'do', 'if', 'static',	
						'while', '#include']

		self.punctuation = [',', '"', "'", ';', '.', '[', ']', '(', ')', '{', '}']

		self.arithop = ['+', '-', '*', '/']
		self.incop = ['++']
		self.decop = ['--']
		self.relop = ['<', '<=', '>', '>=', '!=', '==']
		self.asgnop = ['=']
		self.logop = ['!', '||', '&&']
		self.bitop = ['|', '&', '^']
		self.bitLopOps = ['!', '||', '&&', '|', '&', '^']




	# Function that initializes lexeme beign and forward pointers
	def setLexemePtrs(self):
		self.lexemeBegin, self.lexemeForward = 0,0





	# Function replaces all tabs and newlines with whitespace,returns string
	def formatFile(self):
		_filecontent = self.fileobj.read()
		_filecontent = self.removeComments(_filecontent).replace('\n', ' ').replace('\t', ' ')
		return _filecontent





	# Function that removes all single line and multi-line comments
	# and returns a string that contains the contents of the file.
	def removeComments(self, _filecontent) :
		def blotOutNonNewlines( strIn ) :  # Return a string containing only the newline chars contained in strIn
			return "" + ("\n" * strIn.count('\n'))

		def replacer(match) :
			s = match.group(0)
			if s.startswith('/'):  # Matched string is //...EOL or /*...*/  ==> Blot out all non-newline chars
				return blotOutNonNewlines(s)
			else:                  # Matched string is '...' or "..."  ==> Keep unchanged
				return s

		pattern = re.compile(
			r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
			re.DOTALL | re.MULTILINE
			)

		return re.sub(pattern, replacer, _filecontent)





	# Token controller, called by parser, calls getTokenStream, 
	# sends the tokenStream to the Tokenizer, which returns a symbol table
	# tokenController returns symbol table to parser
	# Format of this symbol table: all the tokens as they appeared in the code, repeats allowed
	# eg. int a; int b; : SYMBOL TABLE: int  a   ;   int    b  ;
	def tokenController(self):
		self.token_stream = self.getTokenStream()
		print self.filecontent
		#print '\n\nTOKEN STREAM GENERATED:', self.token_stream
		#print 'Now calling tokenizer'
		self.tokenizer = tokenizer()
		self.symbol_table = self.tokenizer.tokenize(self.token_stream)
		return self.symbol_table


	



	# Function generates tokens based on patterns and returns them to tokenController
	# using a lexeme begin and forward ptr
	# need to implement lookaheads and count number of characters matched,
	# return token of the one that got the most matched characters, add to token stream
	def getTokenStream(self):
		token_stream = []
		skip_count = 0
		for i in range(0, len(self.filecontent)):
			if(skip_count > 0):
				skip_count -= 1
				continue
			
			#print skip_count
			self.lexemeForward += 1
			current_string = self.filecontent[self.lexemeBegin:self.lexemeForward]
			current_char = current_string[-1:]
			#print current_string
			#print current_char

			# delimited by spaces		
			if self.filecontent[i] == ' ':
				self.lexemeBegin = self.lexemeForward
			
			# search for keywords
			if current_string in self.keywords:
				if self.filecontent[self.lexemeForward] == ' ':
					#print 'token keyword',current_string
					token_stream.append(current_string)
					self.lexemeBegin = self.lexemeForward

			elif current_string in self.punctuation:
				#print 'token ',current_string
				token_stream.append(current_string)
				self.lexemeBegin = self.lexemeForward
			
		

			elif current_string in self.arithop:

				if self.filecontent[self.lexemeBegin+1 : self.lexemeForward+1].replace(' ', '') == current_char:
					#print 'lookahead token: ', current_char + self.filecontent[self.lexemeBegin+1 : self.lexemeForward+1]
					token_stream.append(current_char + self.filecontent[self.lexemeBegin+1 : self.lexemeForward+1])
					skip_count = 1
					self.lexemeForward += 1
				else:
					#print 'token ',current_string
					token_stream.append(current_string)
				self.lexemeBegin = self.lexemeForward
			
			
			
			#lookahead
			elif current_string in self.relop:
				lookahead = i + 1
				lookahead_chars = 1
				while self.filecontent[lookahead] == ' ':
					lookahead += 1
					lookahead_chars += 1	
				#lookahead_chars = len(self.filecontent[self.lexemeBegin:lookahead + 1])
				temp = self.filecontent[self.lexemeBegin:lookahead + 1]
				lookahead_chars += temp.count(' ')
				#print 'Lookahead chars = ', lookahead_chars
				lookahead_string = temp.replace(' ', '')
				#print 'lookinghead to  %s' % lookahead_string 

				if lookahead_string in self.relop:
						#print 'Found lookahead token  %s' % lookahead_string
						token_stream.append(lookahead_string)
						#print 'skip %s' % self.filecontent[self.lexemeBegin:lookahead + 1]
						self.lexemeForward += lookahead_chars
						skip_count = lookahead_chars

				else:
						#print 'token ',current_string
						token_stream.append(current_string)

				self.lexemeBegin = self.lexemeForward

			elif current_string in self.asgnop:
				if self.filecontent[self.lexemeBegin+1 : self.lexemeForward+1].replace(' ', '') == current_char:
					#print 'lookahead token: ', current_char + self.filecontent[self.lexemeBegin+1 : self.lexemeForward+1]
					token_stream.append(current_char + self.filecontent[self.lexemeBegin+1 : self.lexemeForward+1])
					skip_count = 1
					self.lexemeForward += 1
				else:
					#print 'token ',current_string
					token_stream.append(current_string)
				self.lexemeBegin = self.lexemeForward
			
		

			elif current_string in self.bitLopOps:
				if self.filecontent[self.lexemeBegin+1 : self.lexemeForward+1].replace(' ', '') == current_char:
					#print 'lookahead token: ', current_char + self.filecontent[self.lexemeBegin+1 : self.lexemeForward+1]
					token_stream.append(current_char + self.filecontent[self.lexemeBegin+1 : self.lexemeForward+1])
					skip_count = 1
					self.lexemeForward += 1
				elif current_char == '!' and self.filecontent[self.lexemeBegin+1 : self.lexemeForward+1].replace(' ', '') == '=' :
					#print 'HERESDJGSDKGJSDLKJGLSDKNGLSDN'
					#print 'lookahead token: ', current_char + self.filecontent[self.lexemeBegin+1 : self.lexemeForward+1]
					token_stream.append('!=')
					skip_count = 1
					self.lexemeForward += 1
				else:
					#print 'token ',current_string
					token_stream.append(current_string)
				self.lexemeBegin = self.lexemeForward

			else:
				if (current_char.isalnum()) and self.filecontent[i + 1] == ' ':
					#print 'token: ', current_string
 					token_stream.append(current_string)
 					#print 'token: ', current_char
 					self.lexemeBegin = self.lexemeForward
				elif self.inPunctuation(current_char) or self.inArithop(current_char) or self.inRelop(current_char):
 					#print 'rem token: ', current_string[:-1]
 					token_stream.append(current_string[:-1])
 					
 					if self.inArithop(current_char):
 						#print 'LOOKAHEAD TO ', self.filecontent[self.lexemeBegin+1:self.lexemeForward+1]
 						temp_lookahead_string = self.filecontent[self.lexemeBegin+1:self.lexemeForward+1]
 						if  temp_lookahead_string in self.incop or temp_lookahead_string in self.decop:
 							#print 'lookahead token: ', temp_lookahead_string
 							token_stream.append(temp_lookahead_string)
 							self.lexemeForward += 1
 							skip_count = 1

 					else:	
 						#print 'rem token: ', current_char
 						token_stream.append(current_char)
 					self.lexemeBegin = self.lexemeForward
 				
				
		return token_stream
		
	


	# Utility functions, misc, to avoid really long lines of code above 
	def inPunctuation(self, current_string_char):
		return current_string_char in self.punctuation
	def inArithop(self, current_string_char):
		return current_string_char in self.arithop
	def inRelop(self, current_string_char):
		return current_string_char in self.relop




# class that creates the symbol table from the tokens
# do I need to take care of escape sequences?
class tokenizer:
	def __init__(self):
		self.token_stream = []
		self.symbol_table = []
		self.keywords = ['auto', 'double', 'int', 'struct', 'break',	
						'else', 'long', 'switch', 'case', 'enum', 
						'register',	'typedef', 'char', 'extern', 'return',
						'union', 'const', 'float', 'short', 'unsigned',
						'continue', 'for', 'signed', 'void', 'default',	
						'goto', 'sizeof', 'volatile', 'do', 'if', 'static',	
						'while', '#include']

		self.punctuation = [',', '"', "'", ';', '.', '[', ']', '(', ')', '{', '}']

		self.arithop = ['+', '-', '*', '/']
		self.incop = ['++']
		self.decop = ['--']
		self.relop = ['<', '<=', '>', '>=', '!=', '==']
		self.asgnop = ['=']
		self.logop = ['!', '||', '&&']
		self.bitop = ['|', '&', '^']

	

	def tokenize(self, token_stream):
		string_state = False
		self.token_stream = token_stream
		buf = ''
		print self.token_stream
		for i in self.token_stream:
			
			if i == '"' and string_state == False:
				string_state = True
				self.symbol_table.append({'token_type': 'punctuation', 'value': '"'})
				continue
			elif i == '"' and string_state == True:
				# create " token and add 'buf' as string literal token
				string_state = False
				#print buf
				self.symbol_table.append({'token_type': 'const', 'value': buf})
				self.symbol_table.append({'token_type': 'punctuation', 'value': '"'})
				buf = ''
				continue

			if string_state == True:
				buf += i

			elif i in self.keywords:
				self.symbol_table.append( {'token_type': 'keyword', 'value': i} )

			elif i in self.punctuation:
				self.symbol_table.append({'token_type': 'punctuation', 'value': i})

			elif i in self.incop:
				self.symbol_table.append({'token_type': 'incop', 'value': i})

			elif i in self.decop:
				self.symbol_table.append({'token_type': 'decop', 'value': i})

			elif i in self.arithop:
				self.symbol_table.append({'token_type': 'arithop', 'value': i})

			elif i in self.relop:
				self.symbol_table.append({'token_type': 'relop', 'value': i})

			elif i in self.asgnop:
				self.symbol_table.append({'token_type': 'asgnop', 'value': i})

			elif i in self.logop:
				self.symbol_table.append({'token_type': 'logop', 'value': i})

			elif i in self.bitop:
				self.symbol_table.append({'token_type': 'bitop', 'value': i})

			else:
				try: # check for number
					float(i)
					self.symbol_table.append({'token_type': 'const', 'value': i})				
				except ValueError: # else identifier
					self.symbol_table.append({'token_type': 'identifier', 'value': i})	
								

		#self.symbol_table.append(token_stream)
		return self.symbol_table	