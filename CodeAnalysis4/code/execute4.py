import sys
sys.path.append('problems')
sys.path.append('algorithms')

from csp import CSP
from kenken import KenKen
from logic import Logic
from crossmath import Crossmath

puzzle_constraints1 = [
    ['-', 2, ['A1','A2']],
    ['==',2,['A3']],
    ['/',2,['B1','C1']],
    ['/',3,['B2','B3']],
    ['-',1,['C2','C3']]
    ]

## NOTE !!!! There are no ternary constraints listed, even though
## there is one in this puzzle. It seems to still be solvable.
puzzle_constraints2 = [
    ['-', 2, ['A1','B1']],
    ['/', 2, ['A2','A3']],
    ['-', 1, ['A4','A5']],
    ['==', 1, ['B2']],
    ['-', 2, ['B3','B4']],
    ['*', 6, ['C1','C2']],
    ['==', 4, ['C3']],
    ['+', 3, ['C4','D4']],
    ['-', 3, ['D1','E1']],
    ['*', 15, ['D2','D3']],
    ['+', 9, ['E2','E3']],
    ['-', 1, ['E4','E5']]
    ]

logic_constraints = []

cross_constraints =[
    ['+','+',15,['A1','A2','A3']],
    ['+','*',24,['B1','B2','B3']],
    ['+','-',14,['C1','C2','C3']],
    ['+','-',3,['A1','B1','C1']],
    ['*','-',12,['A2','B2','C2']],
    ['/','/',4,['A3','B3','C3']]
]


# pretty-print is quite minimal
# you might want to make a nice looking grid to see results -- but not necessary!

def run_example(size, puzzle):
  kenken = KenKen(size, puzzle)
  kenken.pretty_print(kenken.variables)
  csp = CSP()
  csp.solve(kenken)
  csp.print_solution()

def run_logic(constraints):
    logic = Logic(logic_constraints)
    csp = CSP()
    csp.solve(logic)
    csp.print_solution()

def run_crossmath(size, constraints):
    crossmath = Crossmath(size, constraints)
    crossmath.pretty_print(crossmath.variables)
    csp = CSP()
    csp.solve(crossmath)
    csp.print_solution()


#run_logic(logic_constraints)
#run_example(3, puzzle_constraints1)
#run_example(5, puzzle_constraints2)
run_crossmath(3, cross_constraints)






