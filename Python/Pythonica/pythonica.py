"""	Pythonica.py

This module does input and output parsing.  All the real work is done
by PythonicaCore.
"""

import string
import regex
from pythonicacore import *

gEntryNum = 1
gSymToName = {}
gNameToSym = {}
gNameToPrec = {}
gNonchainable = ('ReplaceAll','Rule','Power','Minus')
# note: instead of just "nonchainable", we should note whether
# each function groups left, groups right, or chains
# (compare -> and /. in Mathematica; right and left, resp.)

#----------------------------------------------------------------------
def buildOperTables():
	global gSymToName, gNameToPrec
	ops = ( '/.',	'ReplaceAll',
			'->',	'Rule',
			'==',	'Equal',
			'=',	'Set',
			'=.',	'Unset',
			'+',	'Plus',
			'-',	'Minus',
			'*',	'Times',
			'/',	'Divide',
			'^',	'Power')
	for i in range(0,len(ops)/2):
		gSymToName[ops[i*2]] = ops[i*2+1]
		gNameToSym[ops[i*2+1]] = ops[i*2]
		gNameToPrec[ops[i*2+1]] = i
buildOperTables()

#----------------------------------------------------------------------
def endOfExpr(s):
	# return the position at which this token ends
	# it may be delimited by a delimiter, or the end of the string
#	print "endOfExpr(" + s + ")"
	p = 0
	maxp = len(s)
	while 1:
		# check for end of line
		if p == maxp: return p
		# check for one-char opers
		if s[p] == ',' or s[p] in gSymToName.keys():
			if p>0: return p
		# check for two-char opers
		if p < maxp-1 and s[p:p+2] in gSymToName.keys(): return p

		# check for groupings...
		if s[p] == '[':					# if we start a '[...]',
			nest = 1
			while nest:					# ...finish it
				p = p + 1
				if s[p] == '[': nest = nest + 1
				if s[p] == ']': nest = nest - 1
		if s[p] == '(':					# if we start a '(...)',
			nest = 1
			while nest:					# ...finish it
				p = p + 1
				if s[p] == '(': nest = nest + 1
				if s[p] == ')': nest = nest - 1
		p = p + 1
	
#----------------------------------------------------------------------
def splitExprs(s):
	# split on delimiters, ignoring those nested in '[...]' or '(...)'
	outexpr = []
	outdelim = []
	while s:
		end = endOfExpr(s)
		outexpr.append(s[:end])
		if end >= len(s)-1: outdelim.append('')
		elif end < len(s)-1 and \
				s[end:end+2] in gSymToName.keys():
			outdelim.append(s[end:end+2])
		else:
			outdelim.append(s[end])
		s = s[end+len(outdelim[-1]):]
	return outexpr,outdelim

#----------------------------------------------------------------------
def subPercent(s):
	"""subPercent(s): replace one '%' with Out[-1],
	'%%' with the Out[-2], etc., and %n (where n is
	an integer) with the Out[n]."""
	while 1:
		l = len(s)
		pos = string.find(s,'%')
		if pos < 0: return s
		cnt = 1
		while pos+cnt < l and s[pos+cnt] in '%0123456789':
			cnt = cnt+1
		substr = s[pos:pos+cnt]
		if len(substr) > 1 and substr[1] != '%':
			rep = 'Out[' + substr[1:] + ']'
		else:
			rep = 'Out[-' + str(len(substr)) + ']'
		s = s[:pos] + rep + s[pos+cnt:]

#----------------------------------------------------------------------
def stripSpaces(s):
	"""stripSpaces(s): strip all spaces from the input string,
	except that if a space occurs between any combination of
	numbers and symbols, convert it to '*'."""
	
	out = ''
	hadsym = 0		# flag: did we just have a symbol or number?
	hadspace = 1	# flag: did we just have some whitespace?
	symchars = string.letters + string.digits
	for c in s:
		if c != ' ':
			if hadspace:
				# we just had a space...
				if c in symchars:
					# and now we see a symbol
					# if we had a symbol before that, throw in a '*'
					if hadsym: out = out + '*'
			hadsym = (c in symchars)
			out = out + c
			hadspace = 0
		else:
			hadspace = 1
	return out

#----------------------------------------------------------------------
def parseOneExpr(s):
	"""parseOneExpr(s): build one token from the string s.
	This string should immediately be a token, and contain no
	paretheses, operators, etc., except within arguments."""
	
	wip = []
	# get first token
	delim = regex.search('[\[, ]', s)
	if string.find(s,']') < delim:
		delim = string.find(s,']')	# why can't we do this w/ regex?
	if delim < 0:
		token = s
		delimchar = '\n'
	else:
		token = s[:delim]
		delimchar = s[delim]
	expr = None

	# do we have a FullForm expression (e.g., Head[args])?
	if delimchar == '[':
		# check for a built-in symbol; otherwise, use ExprSymbol
		try: expr = eval('Expr' + token + '()' )
		except: expr = Expr([],token)
		# ...find all the elements for this expression
		estr = s[:endOfExpr(s)+1]
		estr = estr[delim+1:-1]
		estrlist,delimlist = splitExprs(estr)
#		print "args:", estrlist
		expr.data = map(lambda x:parse(x), estrlist)

	# if not, then do we have a number?
	elif token[0] in '0123456789' or (len(token)>1 and \
		 token[0] == '-' and token[1] in '0123456789'):
		# a Number...
		expr = ExprNumber(string.atof(token))

	# if neither of those, then it must be a symbol
	else:
		# a Symbol...
		expr = ExprSymbol(token)
	return expr

#----------------------------------------------------------------------
def parse(s):
	global gSymToName, gNameToPrec, gNonchainable
	# split into tokens...
	estrlist,delimlist = splitExprs(s)
	# crawl through tokens, combining where operators are found
	wip = []			# stack of expressions
#	print "estrlist:", estrlist
#	print "delimlist:", delimlist
	
	# evaluate each token, considering its following delimiter
	for i in range(0,len(estrlist)):
		if estrlist[i]:
			if estrlist[i][0] == '(':
				# if we have parentheses, parse their contents!
				expr = parse(estrlist[i][1:-1])
			else:
				# otherwise, load a single expression
				expr = parseOneExpr(estrlist[i])
		else: expr = None

		if delimlist[i] in gSymToName.keys():
			# we have an operator...
			opername = gSymToName[delimlist[i]]
			operclass = eval('Expr' + opername)
			if not operclass: raise "Bug", "Undefined operator " + opername

			if not wip:
				# first expression we've seen; throw it on the stack
				wip.append(operclass(expr))

			elif not wip[-1].Head():
				# current expression is headless -- make it us
				wip[-1].head = opername
				if expr: wip[-1].data.append(expr)

			elif wip[-1].Head() == opername and opername not in gNonchainable:
				# same operator; append to previous data
				wip[-1].data.append(expr)

			else:
				# figure out where to stuff token,
				# according to precedence rules
				myPrecedence = gNameToPrec[opername]
				curPrecedence = gNameToPrec[wip[-1].Head()]
				if curPrecedence < myPrecedence:
					# current head has lower precedence... start a new level
#					print opername, "higher than", wip[-1].Head()
					wip.append(operclass(expr))
					wip[-2].data.append(wip[-1])
				else:
					# current head has higher precedence...
					# add expr to current, then move it within us
#					print opername, "lower than", wip[-1].Head()
					if expr: wip[-1].data.append(expr)
					which = -1
					while which != -len(wip):
						if gNameToPrec[ wip[which].Head() ] > myPrecedence:
#							print "...lower than", wip[which].Head()
							pass
						else:
#							print "...but not lower than", wip[which].Head()
							break
						which = which-1
#					print "Stuffing around wip", which
					if wip[which].Head() != opername or \
							opername in gNonchainable:
						if which == -len(wip):
							wip[0] = operclass(wip[0])
							if len(wip) > 1: del wip[1:]
						else:
							wip[which-1].data[-1] = operclass(wip[which-1].data[-1])
							wip[-1] = wip[which-1].data[-1]
		elif delimlist[i] == '':
			if not wip:
				wip.append(expr)
			else:
				wip[-1].data.append(expr)
#		print "wip:", tostr(wip)
	return wip[0]

#----------------------------------------------------------------------
def unparse(expr, leftprec=-1, rightprec=-1):
	# is this expression something we have an operator for?
	head = expr.Head()
	if head not in gNameToPrec.keys():
		# nope, no operator... just print normally
		out = str(expr)
		return out
	# yep, we have an operator... get it, and its precedence
	prec = gNameToPrec[head]
	# (for readability, we'll code a couple of formatting hacks)
	op = gNameToSym[head]
	if op == '*': op = ' '
	elif op != '^': op = ' ' + op + ' '
	# combine data using operator -- pass precedence info
	out = ''
	# leftmost argument gets has our left, and us for the right
	if len(expr.data) > 0:
		if len(expr.data) == 1: r = rightprec
		else: r = prec
		out = unparse(expr.data[0],leftprec,r)
	# middle arguments have us on both left and right
	if len(expr.data) > 2:
		out = out + op + \
		  string.join(map(lambda x,p=prec:unparse(x,p,p),expr.data[1:-1]), \
		 		 op)
	# last argument has our right, and us for the left
	if len(expr.data) > 1:
		out = out + op + \
				unparse(expr.data[-1],prec,rightprec)
	# use parenthesis if we're lower precedence than our neighbors
	if prec < leftprec or prec < rightprec:
		out = '(' + out + ')'
	return out

#----------------------------------------------------------------------
def handleInput(s, surpressOutput=0):
	"""handleInput(s, surpressOutput=0): handle the given input,
	generating output if the second parameter is 0.  Return a
	tuple of (input-expr, output-expr)."""
	
	s = stripSpaces(subPercent(s))
	if s:
		inexp = parse(s)
		eval = inexp.Eval()
		if surpressOutput:
			simp = eval.Simplify()
			while simp != eval:
				eval = simp
				simp = eval.Simplify()
		else:
			print
			print "in FullForm:", inexp
			print "evaluates to:", eval
			# now simplify
			simp = eval.Simplify()
			while simp != eval:
				print "simplifies to:", simp
				eval = simp
				simp = eval.Simplify()
	return inexp,simp

#----------------------------------------------------------------------
def mainLoop():
	global gEntryNum
	s = 'foo'
	while s:
		numstr = '[' + str(gEntryNum) + ']'
		s = raw_input("In" + numstr + " :=   ")
		# break on ';' and surpress output for all but the last
		commands = string.split(s,";")
		for c in commands[:-1]:
			inexp,outexp = handleInput(c,1)
		# on the last one, don't surpress output
		if commands[-1]:
			inexp,outexp = handleInput(commands[-1])
			print
			print "Out" + numstr, "=  ", unparse(outexp)
		print
		# store the in/out data for future reference
		StoreInOut( inexp,outexp )
		gEntryNum = gEntryNum + 1

#----------------------------------------------------------------------

mainLoop()
raw_input("Press Return.")
