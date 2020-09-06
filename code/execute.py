import sys
sys.path.append('problems')
sys.path.append('algorithms')

from towers import TowersOfHanoi
from nqueens import NQueens
from search import BFS_Tree, BFS_Graph
from search import DFS_Tree, DFS_Graph

# You can try different algorithms with different problems
# path=True indicates that the path is part of the solution
# FYI: tree searches for Towers take a loooooong time.

if __name__ == "__main__":
    towers = TowersOfHanoi(tower_size=4)
    #nqueens = NQueens(5,pruning=False)

    search = BFS_Tree(verbose=False)
    #search = DFS_Graph()

    search.solve(towers, path=True)
    #search.solve(nqueens, path=False, all_solutions=False)

    search.print_solution()
    search.print_stats()
