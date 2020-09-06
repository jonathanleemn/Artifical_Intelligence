from problem import Problem

class NQueens(Problem):
    '''
    State is represented as a series of numbers 0-(size-1).
    The index of the number indicates the row and the value represents the column.
    Initially, the list is empty. State changes by adding a number to the end
    of the list. The puzzle can be checked for correctness when the length
    of the list is "size."
    '''
    def __init__(self, size, pruning=False):
        Problem.__init__(self, [])
        self.size = size
        self.pruning = pruning

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

    def pretty_print(self, node):
        state = node.state
        print("Pretty Print ", state)
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



