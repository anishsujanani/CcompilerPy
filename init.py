import sys
import argparse
from Lexer import *

class LanguageProcessor:
	def __init__(self, filepath):
		lexer = Lexer(filepath)
		#parser = Parser()



# entry point
def main():
	
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument('-f', help="Input file, must have a '.c' extension",
                    type=str, dest='FILEPATH', required=True)
	arg_parser.parse_args()
	args = arg_parser.parse_args()
	filepath = args.FILEPATH

	#print len(sys.argv), sys.argv
	#print filename

	lp = LanguageProcessor(filepath)
	exit(0)	




if __name__ == '__main__':
	main()
