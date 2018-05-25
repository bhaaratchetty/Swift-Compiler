import ply.yacc as yacc
import random
from ast import *

import sys
from swift_lexer import tokens
from collections import defaultdict

symbol_table = defaultdict(lambda: None)
astFile = open('swift.ast','w')

def uniqueid():
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1

unique_sequence = uniqueid()

def p_start(p):
	'''start : statements
			| empty'''
	print(p[1],file=astFile)
	print(symbol_table)

def p_empty(p):
	'empty :'
	p[0] = ''

def p_statements(p):
	'statements : statement ENTER next_statement'
	p[0] = str(p[1]) + '\n' + str(p[3])

def p_next_statement(p):
	'''next_statement : statement ENTER next_statement
					| empty'''
	if(len(p)==2):
		p[0] = ''
	else:
		p[0] = str(p[1]) + '\n' + str(p[3])


def p_statement(p):
	'''statement : assignment_statement
				| declaration_statement
				| function_defination
				| for_loop
				| function_call'''
	p[0] = p[1]

def p_assignment_statement(p):
	'assignment_statement : ID WHITESPACE EQ WHITESPACE expression'
	if(symbol_table[p[1]] != None):
		node = ASTNode("assign",next(unique_sequence))
		assignNode = ASTAssignmentNode(p[1],p[5])
		node.addOperation(assignNode)
		symbol_table[p[1]]["value"] = "initialized"
		p[0] = node
	else:
		print("Error: Variable not declared")


def p_declaration_statement(p):
	'''declaration_statement : VAR WHITESPACE ID COL WHITESPACE TYPE
							| VAR WHITESPACE ID COL WHITESPACE TYPE WHITESPACE EQ WHITESPACE expression
							| VAR WHITESPACE ID WHITESPACE EQ WHITESPACE expression '''
	if(symbol_table[p[3]]!=None):
		print('Error: Variable already declared')
	elif(len(p)==7):
		symbol_table[p[3]] = {}
		symbol_table[p[3]]["type"] = p[6]
		symbol_table[p[3]]["value"] = "uninitialised"
	elif(len(p)==11):
		symbol_table[p[3]] = {}
		symbol_table[p[3]]["type"] = p[6]
		symbol_table[p[3]]["value"] = "initialized"
		if(p[6]=="Int"):
			symbol_table[p[3]]["storage"] = 4
		elif(p[6]=="Float"):
			symbol_table[p[3]]["storage"] = 8
		else:
			print('Error: No such type ' , p[6])
			symbol_table[p[3]]["storage"] = 4
		node = ASTNode("assign",next(unique_sequence))
		assignNode = ASTAssignmentNode(p[3],p[10])
		node.addOperation(assignNode)
		p[0] = node
	else:
		symbol_table[p[3]] = {}
		symbol_table[p[3]]["value"] = "initialized"
		symbol_table[p[3]]["type"] = "Int"
		node = ASTNode("assign",next(unique_sequence))
		assignNode = ASTAssignmentNode(p[3],p[7])
		node.addOperation(assignNode)
		p[0] = node

def p_expression(p):
	'''expression : expression PLUS term
				| expression MINUS term
				| term
				'''
	if(len(p)==4):
		idNo = next(unique_sequence)
		node = ASTNode("expression",idNo)
		exprNode = ASTExpressionNode(p[1],p[3],p[2],idNo)
		node.addOperation(exprNode)
		p[0] = str(node)
	else:
		p[0] = p[1]

def p_term(p):
	'''term : term TIMES factor
			| term DIVIDE factor
			| factor
	'''
	if(len(p)==4):
		idNo = next(unique_sequence)
		node = ASTNode("expression",idNo)
		exprNode = ASTExpressionNode(p[1],p[3],p[2],idNo)
		node.addOperation(exprNode)
		p[0] = str(node)
	else:
		p[0] = p[1]

def p_factor(p):
	'''factor : ID
			| NUMBER
	'''
	p[0] = p[1]

def p_function_defination(p):
	'function_defination : FUNC WHITESPACE ID LPAREN optional_parameters RPAREN WHITESPACE optional_return_type WHITESPACE LBRACE ENTER statements RBRACE'
	node = ASTNode('function-defination',next(unique_sequence))
	funNode = ASTFunctionDefinationNode(p[3],p[12])
	node.addOperation(funNode)
	p[0] = node

def p_optional_parameters(p):
	'''optional_parameters : has_parameter
						| empty'''

def p_has_parameter(p):
	'''has_parameter : has_parameter COMMA has_parameter
						| ID COL WHITESPACE TYPE'''

def p_optional_return_type(p):
	'optional_return_type : ARROW WHITESPACE TYPE'

def p_for_loop(p):
    'for_loop : FOR WHITESPACE ID WHITESPACE IN WHITESPACE NUMBER TRIPLEDOT NUMBER WHITESPACE LBRACE ENTER statements RBRACE'
    node = ASTNode('for-loop', next(uniqueid()))
    forNode = ASTForNode(p[3],p[7],p[9],p[13])
    node.addOperation(forNode)
    p[0] = node

def p_optional_ids(p):
	'''optional_ids : empty
		| has_id'''
	p[0] = p[1]

def p_has_id(p):
	'''has_id : ID COMMA has_id
		| ID '''
	if(len(p)==2):
		p[0] = p[1]
	else:
		p[0] = p[1] + ' & ' + p[3]


def p_function_call(p):
	''' function_call : ID LPAREN optional_ids RPAREN'''
		#| VAR WHITESPACE ID WHITESPACE EQ WHITESPACE ID LPAREN optional_ids RPAREN
		#| ID WHITESPACE EQ WHITESPACE ID LPAREN optional_ids RPAREN '''
	node = ASTNode('function-call',next(unique_sequence))
	funNode = ASTFunctionCallNode(p[1],p[3])
	node.addOperation(funNode)
	p[0] = node

parser = yacc.yacc()


f = open(sys.argv[1],'r')
parser.parse(f.read())
