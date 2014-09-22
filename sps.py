import sys
import re

# read from the file named on the command line.
# ex. python3 sps.py input-filename

# Sept 21, 2011 -- fixed the handling of }{ -- each brace should be a separate token
# A regular expression that matches postscript each different kind of postscript token
pattern = '/?[a-zA-Z][a-zA-Z0-9_]*|[-]?[0-9]+|[}{]|%.*|[^\t\n ]'

# A simple program
demoProg = '''
/fact {
   1 dict begin
   /x exch def
      x 0 eq
      {1}
      {x 1 sub fact x mul}
   ifelse
   end
} def
'''
# the operand stack
stack = []

# SPS dictionaries
dic = {}

# the dictionary stack
dstack = []

# Given a string, return the tokens it contains
def parse(s):
   tokens = re.findall(pattern, s)
   return tokens

# Given an open file, return the tokens it contains
def parseFile(f):
   tokens = parse(''.join(f.readlines()))
   return tokens

# Command line use: pass the filename as the first command-line argument
if __name__ == "__main__":
   fn = sys.argv[1]
   print (parseFile(open(fn,"r")))

# make the tokens become stack units, and push every unit into a list 
def makeList(input_list):
  counter = 0
  new_list = []
  for token in input_list:
    if token != '{' and token != '}' and counter == 0:
      new_list.append(token)
    if token == '}' and counter == 0:
      print("Error in makeList: start from }")
      sys.exit()
    if token == '{':
      counter = counter + 1

# push one value to the operand stack
def spush(value):
  stack.append(value)

# pop one value from the operand stack
def spop():
  if len(stack) < 1:
    print("Errorr in spop: empty stack")
    sys.exit()
  return stack.pop()

# push one dict to the dict stack
def dpush(dictz):
  dstack.append(dictz)

# pop one dict from the dict stack
def dpop():
  if len(dstack) < 1:
    print("Error in dpop: empty stack")
    sys.exit()
  return dstack.pop()

# postscript interpreter
def psinterp():
  return

# add,sub,mul,div,eq,lt,gt operators
def add():
  spush(spop()+spop())

def sub():
  secondOperand = spop()
  firstOperand = spop()
  spush(firstOperand-secondOperand)

def mul():
  spush(spop()*spop())

def div():
  secondOperand = spop()
  firstOperand = spop()
  spush(firstOperand/secondOperand)

def eq():
  spush(spop() == spop())

def lt():
  secondOperand = spop()
  firstOperand = spop()
  spush(firstOperand < secondOperand)
def gt():
  secondOperand = spop()
  firstOperand = spop()
  spush(firstOperand > secondOperand)

# built-in operators on boolean values: and,or,not
def andOp():
  spush(spop() and spop())

def orOp():
  spush(spop() or spop())

def notOp():
  spush(not spop())

# built-in sequencing operators: if, ifelse
def ifOp():
  codeArray = spop() # code array pop from top of stack
  bValue = spop() # boolean value of if statment
  if bValue == True:
    psinterp(codeArray) # interpret the code array

def ifelseOp():
  secondCode = spop()
  firstCode = spop()
  bValue = spop()
  if bValue == True:
    psinterp(firstCode) # if true interpret first code
  else:
    psinterp(secondCode) # otherwise interpret second code
  
# stack operators: dup, exch, pop
def dup():
  topValue = spop()
  spush(topValue)
  spush(topValue)

def exch():
  secondValue = spop()
  firstValue = spop()
  spush(secondValue)
  spush(firstValue)

def pop():
  spop()

# dictionary creation operator: dictz
def dictz():
  return {}

# dictionary stack manipulation operators:: begin, end
def begin():
  topValue = spop()
  if (type(topValue) is dict):
    dpush(topValue)
  else:
    print("Error in begin: no dict on the top of stack")
    sys.exit()

def end():
  dpop()

# name definition operator: def
def definition():
  value = spop()
  key = spop()
  if len(dstack) < 1:
    dic[key] = value  
  else:
    localDic = dpop()
    localDic[key] = value

# stack printing operator: stack
def printStack():
  for unit in stack:
    print(unit)

# top of stack printinig operator
def printTop():
  topValue = spop()
  spush(topValue)
  print(topValue)

