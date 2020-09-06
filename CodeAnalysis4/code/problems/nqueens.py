import random

from problem import Problem

class NQueens(Problem):
    '''
    State is represented as a series of numbers 0-(size-1).
    The index of the number indicates the row and the value represents the column.
    
    Search:
    Initially, the list is empty. State changes by adding a number to the end
    of the list. The puzzle can be checked for correctness when the length
    of the list is "size."
    
    Hill Climbing:
    New states are created in 2 ways: permutation (a set) or random list (not a set)
    Neighbors can be generated in a variety of ways (stored in a
    dictionary of function pointers. The variations are for experimenting with parameters.
    There are a variety of objective functions (stored as a dictionary of function pointers.
    If you want to try other methods for neighbors or evaluation, add to the appropriate dictionary
    at the bottom of this file.
    '''
    def __init__(self, size, pruning=False,
                 neighbor_selection="swap", objective_fn="all", start_fn="permute",
                 start_state=None):
        Problem.__init__(self, [])
        self.size = size
        self.pruning = pruning
        self.neighbor_selection = neighbor_selection
        self.objective_fn = objective_fn
        self.start_fn = start_fn
        self.start_state = start_state
        self.initialize_neighbor_selection_dict()
        self.initialize_objective_fn_dict()

    # --------------------     THESE ARE FOR SEARCH -------------------------
    def get_actions(self, state):
        # All queens have been placed. No more actions to perform.
        if len(state)==self.size:
            return []
        # Eiminate those actions that violate one or more of the constraints.
        if self.pruning:
            return self.prune(state)
        # Without pruning, possible actions are always values 0-(size-1)
        else:
            return range(self.size)

    def prune(self, state):
        # check only for duplicates in a given column
        actions = list(range(self.size))
        for column in state:
            actions.remove(column)
        return actions

    def apply_action(self, state, action):
        # **NOTE**: this is mutating state.
        # applying the action is filling in the "next" empty box with "action"
        state.append(action)

    def is_goal(self, state):
        if len(state) < self.size:
            return False

        # rows are guaranteed unique due to the representation of problem
        # check columns
        if not all_unique(state):
            return False

        # check diagonals in rows below the current value
        for row in range(self.size-1):
            column = state[row]
            # check diagonals to the right of each queen
            # Consider the x-y (i.e. row-column) coordinates of a queen that violates this constraint.
            # If a queen is at x-y, then a queen at (x+i,y+i) for all i will be in its diagonal.
            # In this state representation,
            # - "x/row" is the index of the value (because it is zero-based indexing)
            # - "y" is the value
            # - for example, if the state is 3021,
            # -   value 0 means that there is a queen at row 1 and column 0 (zero-based indexing)
            # -   value 1 means that there is a queen at row 3 and column 1
            for next_row in range(1, self.size-column):
                if not row+next_row > self.size-1:
                    if state[row+next_row] == column+next_row:
                        return False
    
            # check diagonals to the left of each queen
            # Consider the x-y coordinates of a queen that violates this constraint.
            # If a queen is at x-y, then a queen at (x-i,y-i) for all i will be in its diagonal.
            for next_row in range(1, column+1):
                if not row+next_row > self.size-1:
                    if state[row+next_row] == column-next_row:
                        return False
        # all passed
        return True


    # --------------------     THESE ARE FOR HILL CLIMBING -------------------------
    def random_solution_state(self):
        # Currently, two ways to generate a random solution
        # Since, only the 2, no need for a dictionary
        # "permute": random permutation of [0,self.size-1] (a set)
        # "random": randomly generated list of self.size numbers (not a set)
        if self.start_fn == "permute":
            state = [i for i in range(self.size)]
            # shuffle seems to do a better job of mixing after multple calls
            random.shuffle(state)
            random.shuffle(state)
            random.shuffle(state)
            return state
        else:
            state = [random.randint(0,self.size-1) for i in range(self.size)]
            return state

    def get_initial_state(self):
        if not self.start_fn == "given":
            return self.random_solution_state()
        else:
            return self.start_state

    def get_random_neighbor(self, state):
        # There are different approaches to selecting a random neighbor.
        # "swap": swap 2 numbers within the list
        # "slide": randomly modify one number to slide a queen to a new pos
        # "new": generate entirely new state by calling random_solution_state
        return self.selection_for_neighbor[self.neighbor_selection](state)

    def swap_for_neighbor(self,state):
        index1, index2 = 0,0
        while index1==index2:
            index1 = random.randint(0, self.size-1)
            index2 = random.randint(0, self.size-1)
        value1 = state[index1]
        state[index1] = state[index2]
        state[index2] = value1
        return state

    def slide_for_neighbor(self, state):
        index = 0
        value = state[index]
        while value == state[index]:
            index = random.randint(0, self.size-1)
            value = random.randint(0, self.size-1)
        state[index] = value
        return state

    def new_for_neighbor(self, state):
        return self.random_solution_state()

    def apply_objective_function(self, state):
        # There are several objective functions with which to experiment:
        # "column": count only attacks in a column, ignoring diagonal
        # "diagonal": count only diagonal attacks, ignoring column
        # "any": 0/1 value indicating no attacks (0) or some attach (1)
        # "all": count both column and diagonal attacks.
        return self.functions_for_evaluation[self.objective_fn](state)

    def column_attacks(self, state):
        copy_state = list(state)
        attacks = 0
        for s in state:
            if s in copy_state[1:len(copy_state)]:
                attacks += len(copy_state) - len(set(copy_state))
            copy_state.remove(s)
        return attacks

    def diagonal_attacks(self, state):
        # determine number of column attacks
        # If the initial state is a random permutation of numbers, and
        # a neighbor is a swap of numbers, there should be no attacking
        # queens along columns and rows.
        # If a neighbor is a random change of one number or the initial state,
        # is not a set, then there could be attaching queens along a column.

        attacks = 0
        # determine number of diagonal attacks.
        # check diagonals in rows below the current value
        for row in range(self.size-1):
            column = state[row]
            # check diagonals to the right of each queen
            # Consider the x-y (i.e. row-column) coordinates of a queen that violates this constraint.
            # If a queen is at x-y, then a queen at (x+i,y+i) for all i will be in its diagonal.
            # In this state representation,
            # - "x/row" is the index of the value (because it is zero-based indexing)
            # - "y" is the value
            # - for example, if the state is 3021,
            # -   value 0 means that there is a queen at row 1 and column 0 (zero-based indexing)
            # -   value 1 means that there is a queen at row 3 and column 1
            for next_row in range(1, self.size-column):
                if not row+next_row > self.size-1:
                    if state[row+next_row] == column+next_row:
                        attacks += 1
            # check diagonals to the left of each queen
            # Consider the x-y coordinates of a queen that violates this constraint.
            # If a queen is at x-y, then a queen at (x-i,y-i) for all i will be in its diagonal.
            for next_row in range(1, column+1):
                if not row+next_row > self.size-1:
                    if state[row+next_row] == column-next_row:
                        attacks += 1
        return attacks

    def any_attacks(self, state):
        if self.column_attacks(state) > 0 or self.diagonal_attacks(state) > 0:
            return 1
        else:
            return 0

    def all_attacks(self, state):
        return self.column_attacks(state)+self.diagonal_attacks(state)

    def initialize_neighbor_selection_dict(self):
        self.selection_for_neighbor = {
            "swap": self.swap_for_neighbor,
            "slide": self.slide_for_neighbor,
            "new": self.new_for_neighbor
        }

    def initialize_objective_fn_dict(self):
        self.functions_for_evaluation = {
            "column": self.column_attacks,
            "diagonal": self.diagonal_attacks,
            "any": self.any_attacks,
            "all": self.all_attacks
        }


    def pretty_print(self, node):
        state = node.state
        print("Pretty Print ", state)
        print("Value ", self.apply_objective_function(node.state))
        if self.size > 30:
            print("Puzzle too large to pretty print.")
            return
        print_puzzle = []
        for row in range(self.size):
            string = ''
            for col in range(self.size):
                if state[row] == col:
                    string = string+'| Q '
                else:
                    string = string+'| _ '
            print_puzzle.append(string+'|')
        for row in range(self.size):
            print(print_puzzle[row])

def all_unique(elements):
    try:
        answer = len(set(elements)) == len(elements)
    except:
        print('FAIL ',elements)
        return True
    return answer




