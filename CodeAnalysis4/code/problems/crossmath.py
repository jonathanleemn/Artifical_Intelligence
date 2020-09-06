import functools
from functools import reduce
from csp_problem import ConstraintProblem

class Crossmath(ConstraintProblem):
    # Input is the size of the puzzle and user-friendly constraints
    def __init__(self, size, constraints):
        ConstraintProblem.__init__(self)
        self.size = size
        self.row_labels = []
        self.column_labels = []
        # Create the "A1", "A2", ... variables
        # Each variable has a name and domain. It's stored in a dictionary indexed by the name (e.g. "A1")
        self.construct_variables()
        # Construct the constraints to ensure unique column and row values
        self.construct_all_unique()
        # Convert the user-friendly constraints to formally defined ones.
        self.construct_user_constraints(constraints)

    def construct_variables(self):
        # creating labels 'A1' 'A2' ... 'B1' 'B2' ...
        A_ascii = ord('A')
        self.row_labels = [chr(i + A_ascii) for i in range(0, self.size)]
        self.column_labels = [str(i) for i in range(1, self.size + 1)]
        for row in self.row_labels:
            for col in self.column_labels:
                # Make it and store in the dictionary of variables.
                # We need a domain of 1 to n^2 for crossmath
                self.variables[row + col] = self.Variable(row + col, [d for d in range(1, (self.size**2) + 1)])

    def construct_all_unique(self):
        #deleted row and column unique constraints because everything needs to be unique
        if self.row_labels == [] or self.column_labels == []:
            # This is not a graceful exit.
            print('You must first call construct_variables() before constructing constraints')
            exit()
        labels = []
        for row in self.row_labels:
            for col in self.column_labels:
                labels.append(row + col)
        # Creates binary "not ==" constraints for all pair combinations in the list
        self.create_all_unique_constraints(labels)

    def construct_user_constraints(self, user_friendly_constraints):

        def make_lambda(opchar1, opchar2, value, order):

            if order == 1:
                return (lambda x, y, z:
                        (value == ConstraintProblem.operators[opchar2](ConstraintProblem.operators[opchar1](x, y), z)))
            elif order == 2:
                return (lambda y, x, z:
                        (value == ConstraintProblem.operators[opchar2](ConstraintProblem.operators[opchar1](x, y), z)))
            elif order == 3:
                return (lambda z, y, x:
                        (value == ConstraintProblem.operators[opchar2](ConstraintProblem.operators[opchar1](x, y), z)))

        for ufc in user_friendly_constraints:
            vars1 = ufc[3]
            vars2 = [ufc[3][1], ufc[3][0], ufc[3][2]]
            vars3 = [ufc[3][2], ufc[3][1], ufc[3][0]]

            c = self.Constraint(vars1, [ufc[0], ufc[1], ufc[2]], make_lambda(ufc[0], ufc[1], ufc[2], 1))
            self.all_constraints.append(c)
            self.add_neighbor(vars1[2], c)
            self.add_neighbor(vars1[1], c)

            c = self.Constraint(vars2, [ufc[0], ufc[1], ufc[2]], make_lambda(ufc[0], ufc[1], ufc[2], 2))
            self.all_constraints.append(c)
            self.add_neighbor(vars1[0], c)
            self.add_neighbor(vars1[2], c)

            c = self.Constraint(vars3, [ufc[0], ufc[1], ufc[2]], make_lambda(ufc[0], ufc[1], ufc[2], 3))
            self.all_constraints.append(c)
            self.add_neighbor(vars1[0], c)
            self.add_neighbor(vars1[1], c)


    def pretty_print(self, variables):
        for k, v in variables.items():
            print(v.name, ' ', v.domain)


