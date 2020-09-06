from collections import deque
from copy import deepcopy
from node import Node, NodeFactory
from algorithm import Algorithm

# This version of CSP uses only the AC3 algorithm. This is an incomplete
# algorithm, meaning it might not be able to solve the problem. To be
# complete, it would need to be combined with search.
class CSP(Algorithm):
  def __init__(self, verbose=False):
    Algorithm.__init__(self, verbose)
    self.variables = None
    self.constraints = None

  def solve(self, problem, all_solutions=False):
    # The variables are being copied then modified so that the original
    # problem stays intact.
    self.reset()
    self.problem = problem
    self.variables = deepcopy(problem.variables)
    self.constraints = problem.all_constraints

    if self.verbose:
      print("Original Problem")
      print("variables ", self.variables)
      print("constraints ", self.constraints)
    
    # if AC3 fails, we will need to use a node factory for search
    # This will be for future implementations.
    # node_factory = NodeFactory(verbose=self.verbose, record_parent=False)

    # maintain a queue of constraints to check for consistency
    # The queue starts with all constraints, unary and binary
    # Neighbors of revised variables will be re-added to the queue.
    queue = deque()
    for c in self.constraints:
      queue.append(c)

    # Keep reducing domains based on consistency with domains.
    # Once the queue is empty, everything that can be infered has been
    while queue:
      # Doesn't matter which end to pop from. This should be more
      # efficient than popleft
      constraint = queue.pop()
      if constraint.is_unary:
        self.node_consistent(self.variables[constraint.vars[0]], constraint)
        continue;
      # Potentially modify only the first variable within the constraint
      variable = self.variables[constraint.vars[0]]
      if self.revise(variable, constraint):
        # Constraints cannot be satisfied. They are inconsistent. Return fail.
        if len(variable.domain) == 0:
          self.solution = None
          return self.solution
        # Something did get revised.
        # Reconsider the constraints involving that variable
        for n in variable.neighbors:
          queue.append(n)
    self.solution = self.variables
    return self.solution

  # Look at domain of variable and determine which domain values
  # are consistent with the constraint. A value is consistent if
  # there exists some value in the other variable's domain that
  # satisfies the constraint.
  def revise(self, variable, constraint):
    # keep track if anything changed in the domain
    revised = False
    # making a copy to both iterate and modify at the same time
    copy_domain = deepcopy(variable.domain)

    # check if some domain value is inconsistent

    if constraint.is_binary:
      for d1 in copy_domain:
        satisfied = False
        for d2 in self.variables[constraint.vars[1]].domain:
          if constraint.function(d1, d2):
            satisfied = True
            break;
        if not satisfied:
          variable.domain.remove(d1)
          revised = True

    else:
      for d1 in copy_domain:
        satisfied = False
        for d2 in self.variables[constraint.vars[1]].domain:
            for d3 in self.variables[constraint.vars[2]].domain:
              if constraint.function(d1, d2, d3):
                satisfied = True
                break;
        if not satisfied:
          variable.domain.remove(d1)
          revised = True
    return revised

  # Checks unary constraints to see if domain can be reduced
  def node_consistent(self, variable, constraint):
    copy_domain = deepcopy(variable.domain)
    for d in copy_domain:
      if not constraint.function(d):
        variable.domain.remove(d)

  def print_solution(self):
    if self.solution == None:
      print("No solution found.")
    else:
      self.problem.pretty_print(self.solution)
