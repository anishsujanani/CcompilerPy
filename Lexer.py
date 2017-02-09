import os.path

class Lexer:
	filepath = ''
	fileobj = None
	filecontent = []

	def __init__(self, filepath):
		if not '.c' in filepath or len(filepath) <= 2:
			print 'Invalid file path entered, exitting now.'
			exit(1)
		self.filepath = filepath
		self.openFile()
		self.printFileContent()

	def openFile(self):
		if os.path.isfile(self.filepath):
			fileobj = open(self.filepath, 'r')
			
			for line in fileobj:
				if len(line.strip('\n')) > 0:
					self.filecontent.append(line.strip('\n'))
			
			fileobj.close()
	
		else:
			print 'ERROR: Could not find:  %s  , exitting now.' % self.filepath
			exit(1)

	def printFileContent(self):
		print ('').join(self.filecontent)