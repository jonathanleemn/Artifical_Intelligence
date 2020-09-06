'''
The intent with this search function is to create a generic framework
that can be applied to any problem. It should be configured so that you
can use this search and the Node class for any problem constructed using
the Problem class.
'''

from collections import deque
from node import Node, NodeFactory
from algorithm import Algorithm
from copy import deepcopy

# Specific search algorithm classes are defined below, all derived from Search.
# These include BFS_Tree, BFS_Graph, DFS_Tree, DFS_Graph
# The default Search method is a BFS tree search.

class Search(Algorithm):
    # BFS Tree Search is the default
    def __init__(self, strategy="BFS", tree=True, verbose=False, depth_limit=3):
        Algorithm.__init__(self, verbose)
        self.depth_limit = depth_limit
        self.visited = []   # visited/explored list for Graph Search
        self.solution = []  # list of solutions (only 1 if all_solutions=False)
        self.tree = tree    # True for tree search, False for Graph search
        if not strategy == "BFS" and not strategy == "DFS":
            return 'ERROR: strategy must be "DFS" or "BFS" (case sensitive)'
        else:
            self.strategy = strategy


    # expands the node to create all children. If in Graph Search, remove all
    # child nodes with states that have been previously visited
    def valid_children(self, node, problem, node_factory):
        children = node_factory.expand(node, problem)
        children_copy = deepcopy(children)
        if self.tree:
            return children
        else:
            for child in children:
                parent = child.parent
                while parent != None:
                    if child.state == parent.state:
                        children_copy.remove(child)
                        break
                    parent = parent.parent
            return children_copy

    # The primary function to solve any problem with the instantiated search algorithm.
    # path=True indicates path is part of the solution.
    # Can choose to find 1 solution (if it exists) or all solutions.
    def solve(self, problem, path=True, all_solutions=False):
        self.reset()
        self.problem = problem

        # Generate the initial (root) node
        node_factory = NodeFactory(verbose=self.verbose, record_parent=path)
        self.max_frontier_node_count = 0
        node = node_factory.make_node( problem.initial_state )

        # For efficiency, check if node is goal state BEFORE putting on Q
        if problem.is_goal( node.state ):
            self.solution.append(node)
            self.total_node_count = 1
            if not all_solutions:
                return self.solution

        # Start the frontier Q by adding the root
        frontier=deque()
        frontier.append(node)
        self.visited.append(node.state)

        # Select a node from the frontier (using the  til nothing left to explore (i.e. frontier is empty)
        # OR a solution is found
        while len(frontier) > 0:
            if self.strategy == "BFS":
                node = frontier.popleft()
            elif self.strategy == "DFS":
                node = frontier.pop()
            if node.depth == self.depth_limit:
                continue;
            for child in self.valid_children(node, problem, node_factory):
                if child.depth > self.max_depth:
                    self.max_depth = child.depth
                if problem.is_goal( child.state ):
                    if self.verbose:
                        print("Max Frontier Count: ", self.max_frontier_node_count)
                    self.solution.append(child)
                    self.total_node_count = node_factory.node_count
                    if not all_solutions:
                        return child
                frontier.append(child)
                if len(frontier) > self.max_frontier_node_count:
                    self.max_frontier_node_count = len(frontier)
        self.total_node_count = node_factory.node_count
        if self.solution==[]:
            self.solution = None
        return self.solution

#####################################################################################################
# These are variations of Search that were created to make it more user friendly.
# You can instantiate Search directly and set appropriate parameters to achieve the same results.

class ID_DFS(Search):
    def __init__(self, verbose=False, tree=True):
        self.solution = []
        self.verbose = verbose
        self.tree = tree
        self.problem = None
        Search.__init__(self)

    def solve(self, problem):
        self.problem = problem
        depth = 1
        solution_found = False
        node_count = 0
        while not solution_found:
            algo = DL_DFS(verbose=self.verbose, depth_limit=depth, tree=self.tree)
            solution = algo.solve(problem)
            node_count += algo.total_node_count
            max_frontier = algo.max_frontier_node_count
            self.save_stats(depth, node_count, max_frontier)
            if solution != None:
                self.solution.append(solution)
                return solution
            depth += 1

    def save_stats(self, depth, node_count, max_frontier):
        print('Depth:', depth)
        print('Node Count', node_count)
        print('Max Frontier Count:', max_frontier)
        print('-----------------------------')


class DL_DFS(Search):
    def __init__(self, verbose=False, depth_limit=5, tree=True):
        Search.__init__(self, strategy="DFS", tree=tree, depth_limit=depth_limit, verbose=verbose)


class BFS_Tree(Search):
    def __init__(self, verbose=False):
        Search.__init__(self, strategy="BFS", tree=True, verbose=verbose, depth_limit=5)

class BFS_Graph(Search):
    def __init__(self, verbose=False):
        Search.__init__(self, strategy="BFS", tree=False, verbose=verbose, depth_limit=5)

class DFS_Tree(Search):
    def __init__(self, verbose=False):
        Search.__init__(self, strategy="DFS", tree=True, verbose=verbose, depth_limit=5)

class DFS_Graph(Search):
    def __init__(self, verbose=False):
        Search.__init__(self, strategy="DFS", tree=False, verbose=verbose, depth_limit=5)



