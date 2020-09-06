from problem import Problem


class TowersOfHanoi(Problem):
    '''
    State is represented as a list of 3 lists, each representing a peg.
    Discs are numbered 3,2,1 from largest to smallest
    The last number in a list indicates the top disc.
    The starting position is [[3,2,1],[],[]) for tower_size = 3
    '''

    def __init__(self, tower_size=3, pruning=False):
        self.tower_size = tower_size
        Problem.__init__(self, [list(range(self.tower_size,0,-1)),[],[]])
        self.pruning = pruning
        self.other_pegs = [[1,2],[0,2],[0,1]]   #list of pegs a disk in a peg of given index can be moved in


    def get_actions(self, state):
        actions = []
        # actions will be moving a disc from one peg to another
        # determine which pegs have a disc that can be moved
        has_discs = []
        for peg in range(3):
            if not state[peg] == []: has_discs.append(peg)
        for peg in has_discs:
            # investigate the other pegs to see their discs
            for destination in self.other_pegs[peg]:
                if destination in has_discs:
                    # make sure the top disc is larger than one moving
                    if state[destination][-1]>state[peg][-1]:
                        actions.append([peg,destination])
                else:
                    # the peg is empty so okay to move there
                    actions.append([peg, destination])
                         
        # no pruning to do for towers (that I can think of)
        return actions

    def apply_action(self, state, action):
        # **NOTE**: this is mutating state.
        # applying the action is moving the disc and recording the move
        disc = state[action[0]].pop()
        state[action[1]].append(disc)

    def is_goal(self, state):
        if len(state[2]) == self.tower_size:
            return True
        else:
            return False

    def pretty_print(self, node):
        # trace back through the parents to get the moves
        moves = []
        path_node = node
        while not path_node.parent==None:
            moves.append(path_node.action)
            path_node = path_node.parent
        # the list in reverse action order, so print from the end to the front
        while not moves==[]:
            print(moves.pop(),end=" ")
        print("")
            
                         
        




