#	PythonicaCore.py
#

import math
from types import *
from tostr import *

gSymTable = {}
gInList = []
gOutList = []


def DataEval(data):
	# return an evaluated copy of the data
	return map(lambda d:d.Eval(), data)

def StoreInOut( indata, outdata ):
	global gInList, gOutList
	gInList.append(indata)
	gOutList.append(outdata)

#----------------------------------------------------------------------
#----------------------------------------------------------------------
class Expr:
	def __init__(self,data=None,head=None):
		t = type(data)
		if not data: self.data = []
		elif t == TupleType: self.data = list(data)
		elif t == ListType: self.data = data
		else: self.data = [data]
		if head: self.head = head
		for d in self.data:
			if type(d) != InstanceType:
				# hmm... if it's a number, maybe we should just
				# replace it with the appropriate ExprNumber?
				raise "Bug", "Invalid data passed to Expr()!"
		
	def __str__(self):
		return str(self.Head()) + '[' + \
			string.join(map(lambda x:str(x),self.data), ',') + ']'
	
	def Head(self):
		try: return self.head
		except: return None
	
	def __cmp__(self,other):
		if self.Head() == other.Head() and self.data == other.data:
			return 0
		else: return 1
		
	def Eval(self):
		return self
	
	def Simplify(self):
		return self

#----------------------------------------------------------------------
class ExprNumber(Expr):
	def __init__(self,data=0):
		self.data = data
		
	def __str__(self):
		if self.data == int(self.data): return str(int(self.data))
		return str(self.data)

	def Head(self):
		return 'Number'
	
	def Eval(self):
		return self

#----------------------------------------------------------------------
class ExprSymbol(Expr):
	def __init__(self,data=''):
		self.data = data
		
	def __str__(self):	
		return str(self.data)
	
	def Head(self):
		return 'Symbol'

	def Eval(self):
		global gSymTable
		if self.data in gSymTable.keys():
			# warning: this could cause recursion!
#			print self.data, "defined as", str(gSymTable[self.data]),
			out = gSymTable[self.data].Eval()
#			print "-->", repr(out)
			return out
		return self

# global predefined symbols
True = ExprSymbol('True')
False = ExprSymbol('False')

#----------------------------------------------------------------------
class ExprRule(Expr):
	def Head(self):
		return 'Rule'

#----------------------------------------------------------------------
class ExprReplaceAll(Expr):
	def Head(self):
		return 'ReplaceAll'

	def Eval(self):
		global gSymTable
		if len(self.data) != 2:
			raise "ReplaceAll::argrx", "ReplaceAll called with " + str(len(self.data)) \
					+ " arguments; 2 arguments are expected."
		# to do the substitution, temporarily replace
		# the given symbol with the given value
		if self.data[1].__class__ != ExprRule:
			raise "ReplaceAll::argrx", "Replace all called with " + \
					str(self.data[1].__class__) + "; ExprRule expected."
		symname = self.data[1].data[0].data
		if symname in gSymTable.keys(): oldval = gSymTable[symname]
		else: oldval = None
		gSymTable[symname] = self.data[1].data[1]
		out = self.data[0].Eval()
		if oldval: gSymTable[symname] = oldval
		else: del gSymTable[symname]
		return out

#----------------------------------------------------------------------
class ExprPlus(Expr):

	def Head(self):	return 'Plus'
	
	def Eval(self):
		data = DataEval(self.data)
		num = 0
		extras = []
		for d in data:
			if d.Head() == 'Number':
				num = num + d.data
			else:
				extras.append(d)
		if extras:
			# we partially reduced it...
			if num: extras.append(ExprNumber(num))
			elif len(extras) == 1:
				return extras[0].Eval()
			return ExprPlus(extras)
		else:
			# we completely reduced this to a Number
			return ExprNumber(num)

	def Simplify(self):
		# if any of our operands are the same, use a Times
		coeff = map(lambda x:1, self.data)
		data = []
		data[:] = self.data
		# convert expressions of the form '3x'
		for i in range(0,len(self.data)):
			data[i] = data[i].Simplify()
			if data[i].__class__ == ExprTimes and \
					data[i].data[0].__class__ == ExprNumber:
				coeff[i] = data[i].data[0].data
				if len(data[i].data) == 2:
					data[i] = data[i].data[1]
				else:
					data[i] = ExprTimes(data[i].data[1:])
		# now, combine terms additively
		for i in range(0,len(data)):
			if coeff[i]:
				for j in range(i+1,len(data)):
					if data[i] == data[j]:
						coeff[i] = coeff[i]+coeff[j]
						coeff[j] = 0
		# now we have coefficients, make the new list
		repl = []
		for i in range(0,len(coeff)):
			if coeff[i] == 1:
				repl.append( data[i] )
			elif coeff[i]:
				repl.append( ExprTimes([ExprNumber(coeff[i]),data[i]]) )
		if len(repl) == 1:
			return repl[0]
		elif len(repl) == 0: return ExprNumber(0)
		else:
			return ExprPlus(repl)
		
#----------------------------------------------------------------------
class ExprTimes(Expr):

	def Head(self): return 'Times'
	
	def Eval(self):
		data = DataEval(self.data)
		num = 1
		extras = []
		for d in data:
			if d.Head() == 'Number':
				num = num * d.data
			else:
				extras.append(d)
		if extras and num != 0:
			# we partially reduced it...
			if num != 1: extras = [ExprNumber(num)] + extras
			elif len(extras) == 1:
				return extras[1].Eval()
			return ExprTimes(extras)
		else:
			# we completely reduced this to a Number
			return ExprNumber(num)

	def Simplify(self):
		data = []
		data[:] = self.data
		
		# first, try flattening -- if an argument is a Times,
		# absorb its arguments into our own
		for i in range(0,len(data)):
			if data[i].Head() == 'Times':
				data[i:i+1] = data[i].data
		
		
		# if any of our operands are the same, use a Power
		# build a list of terms, each stored as [coeff, base, power]
		terms = map(lambda x:[1,x.Simplify(),1], data)
		coeff = 1
		for i in range(0,len(terms)):
			# if it's a ExprNumber, collect separately
			if terms[i][1].__class__ == ExprNumber:
				coeff = coeff * terms[i][1].data
				terms[i][0] = 0
			# if it's a ExprTimes, grab the coefficient
			if terms[i][1].__class__ == ExprTimes and \
					terms[i][1].data[0].__class__ == ExprNumber:
				terms[i][0] = terms[i][1].data[0].data
				if len(terms[i][1].data) == 2:
					terms[i][1] = terms[i][1].data[1]
				else:
					terms[i][1] = ExprTimes(terms[i][1].data[1:])
			# if it's an ExprPower, grab the power
			if terms[i][1].__class__ == ExprPower and \
					terms[i][1].data[1].__class__ == ExprNumber:
				terms[i][2] = terms[i][1].data[1].data
				terms[i][1] = terms[i][1].data[0]
		# now, combine terms additively
		for i in range(0,len(terms)):
			if terms[i][0]:
				for j in range(i+1,len(terms)):
					if terms[i][1] == terms[j][1]:
						terms[i][0] = terms[i][0] * terms[j][0]
						terms[i][2] = terms[i][2] + terms[j][2]
						terms[j][0] = 0
		# now we have powers, make the new list
		repl = []
		for i in range(0,len(terms)):
			if terms[i][2] != 0:
				if terms[i][2] != 1:
					e = ExprPower( [terms[i][1], ExprNumber(terms[i][2])] )
				else: e = terms[i][1]
				if terms[i][0] == 1:
					repl.append( e )
				elif terms[i][0]:
					repl.append( ExprTimes([ExprNumber(terms[i][0]),e]) )
		# put the global coefficient on the front
		if coeff != 1:
			repl = [ExprNumber(coeff)] + repl
		if len(repl) == 1:
			return repl[0]
		elif not repl: return ExprNumber(1)
		return ExprTimes(repl)

#----------------------------------------------------------------------
class ExprMinus(Expr):
	# NOTE: this differs from Mathematica's Minus[] function,
	# which takes only one argument and returns its negative.
	# This takes one or two arguments, which makes parsing
	# much easier.

	def Head(self): return 'Minus'
	
	def Eval(self):
		data = DataEval(self.data)
		if len(data) < 2:
			if data[0].Head() != "Number":
				return ExprTimes( [ExprNumber(-1),self.data[0]] )
			return ExprNumber( -self.data[0].data )
		elif len(data) == 2:
			if data[1].Head() == "Number":
				e = ExprNumber( -self.data[1].data )
			else: e = ExprTimes( [ExprNumber(-1),self.data[1]] )
			e2 = ExprPlus( [self.data[0],e] )
			return e2.Eval()
		else:
			raise "Minus::argrx", "Minus called with " + str(len(data)) \
					+ " arguments; 1 or 2 arguments are expected."
		
#----------------------------------------------------------------------
class ExprDivide(Expr):

	def Head(self): return 'Divide'
	
	def Eval(self):
		data = DataEval(self.data)
		if len(data) != 2:
			raise "Divide::argrx", "Divide called with " + str(len(data)) \
					+ " arguments; 2 arguments are expected."
		if data[0].__class__ == ExprNumber and \
			data[1].__class__ == ExprNumber:
			return ExprNumber( data[0].data / data[1].data )
		else: return self

	def Simplify(self):
		# replace Divide with Power, where possible
		if self.data[1].Head() == 'Number':
			return ExprTimes( [ExprNumber(1/self.data[1].data),self.data[0]])
		e = ExprPower( [self.data[1],ExprNumber(-1)] )
		if self.data[0].Head() == 'Number' and self.data[0].data == 1:
			return e
		return ExprTimes( [self.data[0],e] )
		
#----------------------------------------------------------------------
class ExprSet(Expr):

	def Head(self): return 'Set'

	def Eval(self):
		global gSymTable
		if len(self.data) < 2:
			raise "Set::argrx", "Set called with " + str(len(data)) \
					+ " arguments; at least 2 arguments are expected."
		data = [self.data[0]] + DataEval(self.data[1:])
		for d in data[:-1]:
			if d.Head() != "Symbol":
				raise "Set::ParamError", \
						"First parameters of Set must be a Symbol, not " \
						+ d.Head()
			gSymTable[d.data] = data[-1]
		return data[-1]

#----------------------------------------------------------------------
class ExprUnset(Expr):

	def Head(self): return 'Unset'

	def Eval(self):
		global gSymTable
		if len(self.data) < 1:
			raise "Unset::argrx", "Unset called with 0" \
					+ " arguments; at least 1 argument is expected."
		for d in self.data:
			if d.Head() != "Symbol":
				raise "Set::ParamError", \
						"Parameters of Unset must be Symbol, not " \
						+ d.Head()
			if d.data in gSymTable.keys():
				del gSymTable[d.data]
		return ExprSymbol("OK")

#----------------------------------------------------------------------
class ExprPower(Expr):

	def Head(self): return 'Power'

	def Eval(self):
		data = DataEval(self.data)
		if len(data) != 2:
			raise "Power::argrx", "Power called with " + str(len(data)) \
					+ " arguments; 2 arguments are expected."
		if data[0].__class__ != ExprNumber or data[1].__class__ != ExprNumber:
			return self
		return ExprNumber( math.pow(data[0].data, data[1].data) )

#----------------------------------------------------------------------
class ExprEqual(Expr):

	def Head(self): return 'Equal'

	def Eval(self):
		if len (self.data) < 2: return True
		data = DataEval(self.data)
		if data[0].__class__ != ExprNumber: return self
		val = data[0].data
		for d in data[1:]:
			if d.__class__ != ExprNumber: return self
			if d.data != val: return False
		return True

#----------------------------------------------------------------------
class ExprIn(Expr):

	def Head(self): return 'In'

	def Eval(self):
		data = DataEval(self.data)
		if len(data) != 1:
			raise "In::argrx", "In called with " + str(len(data)) \
					+ " arguments; 1 argument is expected."
		if data[0].__class__ != ExprNumber:
			return self
		idx = int(data[0].data)
		# make positive numbers 1-indexed, to match Mathematica
		if idx > 0: idx = idx - 1
		try: return gInList[idx]
		except: return self

#----------------------------------------------------------------------
class ExprOut(Expr):

	def Head(self): return 'Out'

	def Eval(self):
		data = DataEval(self.data)
		if len(data) != 1:
			raise "Out::argrx", "Out called with " + str(len(data)) \
					+ " arguments; 1 argument is expected."
		if data[0].__class__ != ExprNumber:
			return self
		idx = int(data[0].data)
		# make positive numbers 1-indexed, to match Mathematica
		if idx > 0: idx = idx - 1
		try: return gOutList[idx].Eval()
		except: return self
		
#----------------------------------------------------------------------
# end of PythonicaCore.py
#----------------------------------------------------------------------

