import os.path
import re

class lexer:


	# Function assigns param filepath to internal var, opens file
	# in read mode
	def __init__(self, filepath):
		self.filepath = filepath
		self.fileobj = open(filepath, 'r')
		self.filecontent = self.formatFile()
		self.setRegexes()
		self.setLexemePtrs()


	# Function that initialized patterns to look for as internal vars
	def setRegexes(self):
		self.keywords = ['auto', 'double', 'int', 'struct', 'break',	
						'else', 'long', 'switch', 'case', 'enum', 
						'register',	'typedef', 'char', 'extern', 'return',
						'union', 'const', 'float', 'short', 'unsigned',
						'continue', 'for', 'signed', 'void', 'default',	
						'goto', 'sizeof', 'volatile', 'do', 'if', 'static',	
						'while', '#include']

		self.punctuation = [',', '"', "'", ';', '.', '[', ']', '(', ')']

		self.arithop = ['+', '-', '*', '/']
		self.incop = ['++']
		self.decop = ['--']
		self.relop = ['<', '<=', '>', '>=', '!=', '==']
		self.asgnop = ['=']
		self.logop = ['!', '||', '&&']
		self.bitop = ['|', '&', '^']



	# Function that initializes lexeme beign and forward pointers
	def setLexemePtrs(self):
		self.lexemeBegin, self.lexemeForward = 0,0


	# Function replaces all tabs and newlines with whitespace,returns string
	def formatFile(self):
		_filecontent = self.fileobj.read().replace('\n', ' ').replace('\t', ' ')
		return _filecontent



	# Function generates tokens based on RegEx and returns them to parser
	# using a lexeme begin and forward ptr
	# need to implement lookaheads and count number of characters matched,
	# return token of the one that got the most matched characters
	def genToken(self):
		for i in range(0, len(self.filecontent)):
		
			self.lexemeForward += 1
			current_string = self.filecontent[self.lexemeBegin:self.lexemeForward]
			current_char = current_string[-1:]
			
			# delimited by spaces		
			if self.filecontent[i] == ' ':
				self.lexemeBegin = self.lexemeForward
			
			# search for keywords
			if current_string in self.keywords:
				print 'token ',current_string
				self.lexemeBegin = self.lexemeForward

			elif current_string in self.punctuation:
				print 'token ',current_string
				self.lexemeBegin = self.lexemeForward
			
			elif current_string in self.arithop:
				print 'token ',current_string
				self.lexemeBegin = self.lexemeForward
			
			#lookahead
			elif current_string in self.incop:
				lookahead = i + 1
				while self.filecontent[lookahead] == ' ':
					lookahead += 1
				
				print 'lookinghead to  %s' % self.filecontent[self.lexemeBegin:lookahead+1]
				
				if self.filecontent[self.lexemeBegin:lookahead + 1] in self.relop:
					print 'Found lookahead token  %s' % self.filecontent[self.lexemeBegin:lookahead+1]

				else:
					print 'token ',current_string

				self.lexemeBegin = self.lexemeForward
			
			#lookahead
			elif current_string in self.decop:
				lookahead = i + 1
				while self.filecontent[lookahead] == ' ':
					lookahead += 1
				
				print 'lookinghead to  %s' % self.filecontent[self.lexemeBegin:lookahead+1]
				
				if self.filecontent[self.lexemeBegin:lookahead + 1] in self.relop:
					print 'Found lookahead token  %s' % self.filecontent[self.lexemeBegin:lookahead+1]
				else:
					print 'token ',current_string

				self.lexemeBegin = self.lexemeForward
			
			#lookahead
			elif current_string in self.relop:
				lookahead = i + 1
				while self.filecontent[lookahead] == ' ':
					lookahead += 1
					
				lookahead_chars = len(self.filecontent[self.lexemeBegin:lookahead + 1])
				temp = self.filecontent[self.lexemeBegin:lookahead + 1]
				lookahead_string = temp.replace(' ', '')
				print 'lookinghead to  %s' % lookahead_string

				if lookahead_string in self.relop:
						print 'Found lookahead token  %s' % lookahead_string
						print 'skip %s' % self.filecontent[self.lexemeBegin:lookahead + 1]
						self.lexemeForward += lookahead_chars - 1

				else:
						print 'token ',current_string

				self.lexemeBegin = self.lexemeForward

			elif current_string in self.asgnop:
				print 'token ',current_string
				self.lexemeBegin = self.lexemeForward
			
			elif current_string in self.logop:
				print 'token ',current_string
				self.lexemeBegin = self.lexemeForward
			
			elif current_string in self.bitop:
				print 'token ',current_string
				self.lexemeBegin = self.lexemeForward

			else:
				if self.inPunctuation(current_char) or self.inArithop(current_char) or self.inRelop(current_char):
 					print 'token: ', current_string[:-1]
 					print 'token: ', current_char
 					self.lexemeBegin = self.lexemeForward
 				if(current_string[-1:] in self.keywords):
 					print 'token: ', current_string[-1:]
 					self.lexemeBegin = self.lexemeForward
				
		return self.filecontent					
		#return self.filecontent

	def inPunctuation(self, current_string_char):
		return current_string_char in self.punctuation
	def inArithop(self, current_string_char):
		return current_string_char in self.arithop
	def inRelop(self, current_string_char):
		return current_string_char in self.relop