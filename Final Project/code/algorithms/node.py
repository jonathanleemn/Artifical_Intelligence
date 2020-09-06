from copy import deepcopy
import math

# When the algorithm solves a given problem, it uses a node factory to node creation.
# This encapsulates the functionality and tracks node count for that call to solve()
class NodeFactory:
	def __init__(self, verbose=False, record_parent = False):
                # node_count is incremented at every node creation
                # options to track the path by having each node contain its parent
                # and option to print out information as the nodes are being created
		self.node_count = 0
		self.record_parent = record_parent
		self.verbose = verbose

	def make_node(self, state, parent=None, action=None):
		if self.verbose and 0 == (self.node_count % 100):
			print('node count: ', self.node_count)
		self.node_count += 1
		if self.record_parent:
        		return Node(state, action, parent)
		else:
                        return Node(state, action)

	def expand(self, node, problem):
                # a new child node is made for every possible action that can be applied to the given node.state
		return [self.make_child(node, problem, action) for action in problem.get_actions(node.state)]

	def make_child(self, node, problem, action):
		child_state = deepcopy(node.state)
		problem.apply_action(child_state, action)
		child_node = self.make_node(child_state, node, action)
		child_node.depth = node.depth+1
		return child_node

class Node:
	def __init__(self, state, action, parent=None):
		self.state = state
		self.action = action
		self.parent = parent
		self.key = None
		self.depth = 0
		self.value = math.inf

