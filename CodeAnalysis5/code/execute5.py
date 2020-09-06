import sys
sys.path.append('problems')
sys.path.append('algorithms')

from towers import TowersOfHanoi
from nqueens import NQueens

from search import ID_DFS

def test_iddfs():

    print("--- Solving NQueens with IDDFS Tree")
    nqueens = NQueens(5,pruning=True)
    iddfs_tree = ID_DFS(verbose=False, tree=True)
    solution = iddfs_tree.solve(nqueens)
    iddfs_tree.print_solution()

    print("")
    print("--- Solving Towers with IDDFS Graph")
    towers = TowersOfHanoi(tower_size=2)
    iddfs_graph = ID_DFS(verbose=False, tree=False)
    solution = iddfs_graph.solve(towers)
    iddfs_graph.print_solution()

test_iddfs()
