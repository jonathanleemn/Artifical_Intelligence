import re
import operator
from problem import Problem


class ConstraintProblem(Problem):
  # Thanks StackOverflow:
  # http://stackoverflow.com/questions/1740726/python-turn-string-into-operator
  operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '==': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
    'abs': operator.abs,
    '^': operator.pow
  }

  def __init__(self, variables={}, constraints=[]):
    self.variables = variables
    self.all_constraints = constraints
    self.unary_constraints = []
    self.binary_constraints = []

  class Variable:
    def __init__(self, name, domain):
      self.name = name
      self.domain = list(domain)
      self.neighbors = []
      
  class Constraint:
    # passing in variables and op for easier reference and debugging
    def __init__(self, variables, op, function):
      self.vars = variables
      self.function = function
      self.operator = op
      self.is_unary = (len(variables) == 1)
      self.is_binary = (len(variables) == 2)


  def sort_constraints(self):
    for c in self.all_constraints:
      if c.is_unary:
        self.unary_constraints.append(c)
      elif c.is_binary:
        self.binary_constraints.append(c)
      else:
        self.ternary_constraints.append(c)

  def create_all_unique_constraints(self, variables):
    # generate a list of constraints that implement the all-different constraint
    # for all variable combinations in variables
    for var1 in variables:
        for var2 in variables:
            if ( not var1 == var2 ) :
                c = self.Constraint([var1, var2], "not ==", lambda x,y: not x==y)
                self.all_constraints.append(c)
                self.add_neighbor(var2, c)

  def add_neighbor(self, variable, constraint):
    self.variables[variable].neighbors.append(constraint)

    



