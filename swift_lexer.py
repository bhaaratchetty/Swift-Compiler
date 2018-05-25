import ply.lex as lex

tokens = ['NUMBER','ID','WHITESPACE','ENTER','EQ','COL',
'PLUS','MINUS','TIMES','DIVIDE','LPAREN','RPAREN','LBRACE','RBRACE','ARROW','COMMA','TRIPLEDOT']

reserved = { 'var': 'VAR' ,'Int': 'TYPE', 'Float': 'TYPE' ,'Double':'TYPE','func':'FUNC','in':'IN','for':'FOR'}

tokens = tokens + list(reserved.values())

t_WHITESPACE = r'\ +'
t_ENTER = r'\n'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_EQ = r'='
t_COL = r':'
t_TYPE = r'Int|Float|Double'
t_ARROW = r'->'
t_COMMA = r','
t_TRIPLEDOT = r'\.\.\.'

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_ID(t):
	r'[a-z|A-Z][a-z|A-Z|0-9]*'
	t.type = reserved.get(t.value,'ID')
	return t

def t_singleLine(t):
	r'//.*\n'

def t_multiLine(t):
	r'/\*[^(*/)]*\*/\n'

lexer = lex.lex(debug=1)

if(__name__ == "__main__"):
	lex.runmain()
