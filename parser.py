from lexer import *

class parser:

	# Function creates internal lexer obj
	def __init__(self, filepath):
		self.lexer = lexer(filepath)

	# Entry point parser control function
	def beginParse(self):
		self.getToken()

	# Requests a token from the lexer
	def getToken(self):
		current_token = self.lexer.genToken()
		print current_token

	