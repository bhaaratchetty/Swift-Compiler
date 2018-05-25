class ASTNode:
	def __init__(self,Type,idNo):
		self.Type = Type
		self.idNo = idNo
		self.operation = None
	def __str__(self):
		if self.Type == 'function-defination' or self.Type == 'for-loop':
			output = ('Node ' + str(self.idNo) + '\n' + '\t\t---' + self.Type + '\n\t\t' + str(self.operation))
		elif self.Type == 'expression':
			output = ''.join('Node ' + str(self.idNo) + '\n' + '\t\t---' + self.Type + '\t\t' + str(self.operation))
		else:
			output = ('Node ' + str(self.idNo) + '\n' + '\t\t---' + self.Type + '\t\t' + str(self.operation))
		return output
	def addOperation(self,operation):
		self.operation = operation

class ASTAssignmentNode:
	def __init__(self,variable,assignValue):
		self.variable = variable
		self.assignValue = assignValue
	def __str__(self):
		return   self.variable + '     ' + str(self.assignValue)

class ASTExpressionNode:
	def __init__(self,l,r,o,idNo):
		self.l = l
		self.o = o
		self.r = r
		self.idNo = idNo
	def __str__(self):
		return "Node" + str(self.idNo) + " operation " + self.o  + " on " + "".join(str(self.l).split()[0:2]) + " " + "".join(str(self.r).split()[0:2]) + " " + str(" ".join(str(self.l).split()[2:])) + " " + str(" ".join(str(self.r).split()[2:]))

class ASTFunctionDefinationNode:
	def __init__(self,name,statements):
		self.name = name
		self.statements = statements
	def __str__(self):
		return " function " + self.name  + "\n" + "Beginning of Function\n" +  str(self.statements) + "End of Function"

class ASTForNode:
	def __init__(self, variable, ivalue, fvalue, statements):
		self.variable = variable
		self.ivalue = ivalue
		self.fvalue = fvalue
		self.statements = statements
	def __str__(self):
		return "For statement " + self.variable + " " + str(self.ivalue) + " " + str(self.fvalue) + "\nBeginning of For Loop\n" + str(self.statements) + "End of For statement"

class ASTFunctionCallNode:
	def __init__(self,fnName,arguments):
		self.fnName = fnName
		self.arguments = arguments
	def __str__(self):
		return "call " + self.fnName + " - Arguments: " + self.arguments
