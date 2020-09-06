import functools
from functools import reduce
from csp_problem import ConstraintProblem


# The primary problem set-up consists of "variables" and "constraints":
#   "variables" are a dictionary of constraint variables (of type ConstraintVar), example variables['A1']
#   For KenKen, each row is labeled with a letter. "A" is the top row.
#       And each column is a number. "1" is the leftmost column.
#   
#   "constraints" are the unary and binary constraints that must be satisfied.
#   For KenKen, constraints will include uniqueness for rows and columns (generic for all kenken's)
#       And for the specifics of the puzzle, which are provided in a "user-friendly" format,
#       then converted to a usable representation.
#   

class KenKen(ConstraintProblem):
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
        # This is not really used, but might come in handy later -- make separate groups for unary and binary.
        self.sort_constraints()

    def construct_variables(self):
        # creating labels 'A1' 'A2' ... 'B1' 'B2' ...
        A_ascii = ord('A')
        self.row_labels = [chr(i + A_ascii) for i in range(0, self.size)]
        self.column_labels = [str(i) for i in range(1, self.size + 1)]
        for row in self.row_labels:
            for col in self.column_labels:
                # Make it and store in the dictionary of variables.
                self.variables[row + col] = self.Variable(row + col, [d for d in range(1, self.size + 1)])

    def construct_rows_unique_constraints(self):
        if self.row_labels == [] or self.column_labels == []:
            # This is not a graceful exit.
            print('You must first call construct_variables() before constructing constraints')
            exit()
        for row in self.row_labels:
            labels = []
            for col in self.column_labels:
                labels.append(row + col)
            # Creates binary "not ==" constraints for all pair combinations in the list
            self.create_all_unique_constraints(labels)

    def construct_columns_unique_constraints(self):
        if self.row_labels == [] or self.column_labels == []:
            print('You must first call construct_variables() before constructing constraints')
            return
        for col in self.column_labels:
            labels = []
            for row in self.row_labels:
                labels.append(row + col)
            # Creates binary "not ==" constraints for all pair combinations in the list
            self.create_all_unique_constraints(labels)

    def construct_all_unique(self):
        self.construct_columns_unique_constraints()
        self.construct_rows_unique_constraints()

    def construct_user_constraints(self, user_friendly_constraints):
        # constraints are provided in a more user-friendly format
        # EXAMPLES: ['-', 2, ['A1','B1']], ['==', 1, ['B2']]
        # This will convert that to a format required by the csp algorithm
        # ufc is a triplet:
        # - index 0 is the operator,
        # - index 1 is the result value
        # - index 2 is a variable list (required to have 1 or 2 elements only)

        def make_lambda(opchar, value, unary=False):
            if unary:
                return (lambda x: ConstraintProblem.operators[opchar](x, value))
            else:
                return (lambda x, y:
                        (value == ConstraintProblem.operators[opchar](x, y)) or
                        (value == ConstraintProblem.operators[opchar](y, x)))

        for ufc in user_friendly_constraints:
            if len(ufc[2]) == 1:  # unary constraint
                # EXAMPLE: constraint is ['==',2,['A3']]
                # This creates Constraint(['A3'], lambda x: x == 2)
                # Note that the lambda example is infix, however
                # we are using operators[..]( , ) -- a prefix notation (but same result)
                # The call to make_lambda is used because of "lazy evaluation"
                # of the lambda fn -- meaning it won't dereference until it evaluates the lambda.
                # At that point, ufc is equal to the last constraint evaluated.
                # Do not do lambda x: operators[ufc[0]](x,ufc[2]) !!!!  (It took me a bit to debug that)
                self.all_constraints.append(self.Constraint(ufc[2], ufc[0],
                                                            make_lambda(ufc[0], ufc[1], unary=True)))
            elif len(ufc[2]) == 2:  # binary constraint
                # EXAMPLE: constraint is ['-',2,['A2','B2']]
                # This requires 2 constraints because Revise() only edits the
                # first variable listed.
                # So this creates one for ['A2', 'B2'] and one for ['B2', 'A2']
                # Call to make_lambda used because of lazy evaluation (see note in above if-statement

                vars1 = ufc[2]
                vars2 = [ufc[2][1], ufc[2][0]]

                c = self.Constraint(vars1, ufc[0], make_lambda(ufc[0], ufc[1]))
                self.all_constraints.append(c)
                self.add_neighbor(vars1[1], c)

                c = self.Constraint(vars2, ufc[0], make_lambda(ufc[0], ufc[1]))
                self.all_constraints.append(c)
                self.add_neighbor(vars1[0], c)
            else:
                print("Not yet equipped to manage more than arc consistency")
                return

    def pretty_print(self, variables):
        for k, v in variables.items():
            print(v.name, ' ', v.domain)


