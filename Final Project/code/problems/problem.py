
# abstract class to template a specific problem to be solved.
# define a Problem class (e.g. Sudoku) that derives from this class.

class Problem:
    def __init__(self, initial, goals=[]):
        self.initial_state = initial
        self.goal_states = goals

    def get_actions(self, state):
        # return a list of viable actions given 'state'
        return []

    def apply_action(self, state, action):
        # return the new state when 'action' is applied to 'state'
        return None

    def is_goal(self, state):
        # test whether 'state' is a solution/goal state
        # some problems will have defined states that are goals (e.g. sliding puzzle)
        # some problems have rules/constraints that define a goal state (e.g. sudoku)
        return False

    def pretty_print(self, state):
        print(state)
