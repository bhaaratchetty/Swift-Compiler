from collections import defaultdict
import sys

inputFile = open('tac.s','r')
outputFile = open('optimizedTac.s','w+')
outputFile2 = open('optimizedTac2.s','w+')

outputFile2.write(inputFile.read())
outputFile2.seek(0)

#Constant Folding optimisation
def constantFolding():
	outputFile.seek(0)
	outputFile.truncate()
	outputFile2.seek(0)
	for line in outputFile2:
		if '=' in line and 'goto' not in line:
			lhs = line.split('=')[0].strip()
			print( lhs + ' = ',file=outputFile,end='')
			exp = line.split('=')[1].strip()
			try:
				rhs = eval(exp)
				print(rhs,file=outputFile)
			except:
				print(exp,file=outputFile)
		else:
			print(line,file=outputFile,end='')

dictionary = defaultdict(lambda: None)

#Constant Propagation optimisation
def constantPropagation():
	outputFile.seek(0)
	outputFile2.seek(0)
	outputFile2.truncate()
	for line in outputFile:
		if "=" in line and "goto" not in line:
			lhs = line.split('=')[0].strip()
			rhs = line.split('=')[1].strip()
			if "+" not in line and "-" not in line and "*" not in line and "/" not in line:
				if "." in rhs:
					rhsValue = float(rhs)
					dictionary[lhs] = rhsValue
					print(line,end='',file=outputFile2)
				else:
					try:
						rhsValue = int(rhs)
						dictionary[lhs] = rhsValue
						print(line,end='',file=outputFile2)
					except:
						if(dictionary[rhs] != None):
							print(lhs , '=' , dictionary[rhs],file=outputFile2)
						else:
							print(line,end='',file=outputFile2)
			else:
				oper = rhs.split()[1]
				terms = rhs.split(oper)
				print(lhs , '= ' , end='',file=outputFile2)
				t1 = terms[0].strip()
				t2 = terms[1].strip()
				if(dictionary[t1] != None):
					print(dictionary[t1],end='',file=outputFile2)
				else:
					print(t1,end='',file=outputFile2)
				print(' ' + oper + ' ',end='',file=outputFile2)
				if(dictionary[t2] != None):
					print(dictionary[t2],file=outputFile2)
				else:
					print(t2,file=outputFile2)
		else:
			print(line,end='',file=outputFile2)
	outputFile.seek(0)

try:
	for i in range(int(sys.argv[1])):
		constantFolding()
		constantPropagation()
except: # if argv[1] is not provided
	prev = None
	curr = outputFile2.read()
	outputFile2.seek(0)
	i = 0
	while(prev!=curr):
		i += 1
		prev = outputFile2.read()
		constantFolding()
		constantPropagation()
		outputFile2.seek(0)
		curr = outputFile2.read()
		outputFile2.seek(0)
	print('Number of folding-propagation performed: ' , i )
	print('Number of times that guarantees optimized code: ',i-1)
