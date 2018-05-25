from collections import defaultdict

astFileText = list(filter(None,open('swift.ast','r').read().split('\n')))
length = len(astFileText) 
tempCount = 0
i = 0
labelCount = -1
dictionary = defaultdict(lambda: None)
line = astFileText[i]
f = open('tac.s','w+')
forloopStack = []

def generateCodeForBasicStatement(line):
	global tempCount,i
	lhsvar = line.split()[1]
	if(line.split()[2] != 'Node'):
		rhs = line.split()[2]
		print(lhsvar + ' = ' + rhs,file=f)
		i += 1
	else:
		expressions = str(" ".join(astFileText[i+1].split())).split('---expression')[1:]
		expressions = expressions[::-1]
		iterationCount = 0
		for exp in expressions:
			iterationCount += 1
			e = exp.split()
			lhs = e[0]
			op = e[2]
			op1 = e[4]
			op2 = e[5]
			if(iterationCount == len(expressions)):
				if(op1.startswith('Node')):
					op1 = dictionary[op1]
				if(op2.startswith('Node')):
					op2 = dictionary[op2]				
				print('t' + str(tempCount) + ' = ' + str(op1) + " " + op + " " + str(op2),file=f)
				dictionary[lhs] = 't' +str(tempCount)
				print(lhsvar + ' = ' + 't' + str(tempCount) ,file=f)
				tempCount += 1
				break
			if(not(op1.startswith('Node')) and not(op2.startswith('Node'))):
				print('t' + str(tempCount) + ' = ' + op1 + " " + op + " " + op2,file=f)
				dictionary[lhs] = 't' + str(tempCount)
				tempCount += 1
			else:
				if(op1.startswith('Node')):
					op1 = dictionary[op1]
				if(op2.startswith('Node')):
					op2 = dictionary[op2]				
				print('t' + str(tempCount) + ' = ' + str(op1) + " " + op + " " + str(op2),file=f)
				dictionary[lhs] = 't' + str(tempCount)
				tempCount += 1
		i += 2

def generateCodeForForLoop(line):
	global tempCount,i,labelCount,forloopStack
	var =  astFileText[i+1].split()[2]
	initial = astFileText[i+1].split()[3]
	final = astFileText[i+1].split()[4]
	print(var + ' = ' + initial,file=f)
	labelCount += 1
	print("L" + str(labelCount) + ":",file=f)
	forloopStack.append(labelCount)
	i += 4
	l = astFileText[i]
	while(1):
		generateCode(astFileText[i])
		l = astFileText[i]
		if(l == 'End of For statement'):
			break
		i += 1 
		l = astFileText[i]
	i += 1
	print('t' + str(tempCount) + ' = ' + var + ' + 1',file=f)
	print(var + ' = ' + 't' + str(tempCount),file=f) 
	tempCount += 1 
	print('if ' + var + ' <= ' + final + ' goto L' + str(forloopStack[len(forloopStack)-1]),file=f)
	del forloopStack[len(forloopStack)-1]

def generateCodeForFunctionDefination(line):
	global tempCount,i,labelCount
	name = astFileText[i+1].split()[1]
	print('func begin ' + name,file = f)
	i = i + 4
	while(1):
		generateCode(astFileText[i])
		l = astFileText[i]
		if(l == 'End of Function'):
			break
		i += 1 
		l = astFileText[i]
	print('func end',file = f)
	i += 1

def generateCodeForFunctionCall(line):
	global i
	arguments = line.split('Arguments:')[1].strip().split('&')
	for arg in arguments:
		print('param ' + arg,file = f)
	print('call ' + astFileText[i].split()[2] + ' , ' + str(len(arguments)),file = f)
	i += 1

def generateCode(line):
	if(line.split()[0]=="---assign"):
		generateCodeForBasicStatement(line)
	elif(line.split()[0]=='---for-loop'):
		generateCodeForForLoop(line)
	elif(line.split()[0]=='---function-defination'):
		generateCodeForFunctionDefination(line)
	elif(line.split()[0]=='---function-call'):
		generateCodeForFunctionCall(line)

while(1):
	if(line.startswith("Node")):
		i += 1
		line = astFileText[i]
		generateCode(line)
		if(i>=length):
			break
		line = astFileText[i]
		
			

