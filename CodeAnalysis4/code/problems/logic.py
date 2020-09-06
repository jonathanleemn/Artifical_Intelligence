import functools
from functools import reduce
from csp_problem import ConstraintProblem


class Logic(ConstraintProblem):
    # Input is the size of the puzzle and user-friendly constraints
    def __init__(self, constraints):
        ConstraintProblem.__init__(self)
        # Each variable has a name and domain. It's stored in a dictionary indexed by the name (e.g. "A1")
        self.construct_variables()
        # Convert the user-friendly constraints to formally defined ones.
        self.construct_user_constraints(constraints)
        # This is not really used, but might come in handy later -- make separate groups for unary and binary.
        self.sort_constraints()

    def construct_variables(self):
        domainA = [['dog', 'ghost'], ['dog', 'pirate'], ['dog', 'clown'], ['dog', 'hotdog'],
                   ['cat', 'ghost'], ['cat', 'pirate'], ['cat', 'clown'], ['cat', 'hotdog'],
                   ['fish', 'ghost'], ['fish', 'pirate'], ['fish', 'clown'], ['fish', 'hotdog'],
                   ['bird', 'ghost'], ['bird', 'pirate'], ['bird', 'clown'], ['bird', 'hotdog']]
        domainB = [['dog', 'ghost'], ['dog', 'pirate'], ['dog', 'clown'], ['dog', 'hotdog'],
                   ['cat', 'ghost'], ['cat', 'pirate'], ['cat', 'clown'], ['cat', 'hotdog'],
                   ['fish', 'ghost'], ['fish', 'pirate'], ['fish', 'clown'], ['fish', 'hotdog'],
                   ['bird', 'ghost'], ['bird', 'pirate'], ['bird', 'clown'], ['bird', 'hotdog']]
        domainC = [['dog', 'ghost'], ['dog', 'pirate'], ['dog', 'clown'], ['dog', 'hotdog'],
                   ['cat', 'ghost'], ['cat', 'pirate'], ['cat', 'clown'], ['cat', 'hotdog'],
                   ['fish', 'ghost'], ['fish', 'pirate'], ['fish', 'clown'], ['fish', 'hotdog'],
                   ['bird', 'ghost'], ['bird', 'pirate'], ['bird', 'clown'], ['bird', 'hotdog']]
        domainD = [['dog', 'ghost'], ['dog', 'pirate'], ['dog', 'clown'], ['dog', 'hotdog'],
                   ['cat', 'ghost'], ['cat', 'pirate'], ['cat', 'clown'], ['cat', 'hotdog'],
                   ['fish', 'ghost'], ['fish', 'pirate'], ['fish', 'clown'], ['fish', 'hotdog'],
                   ['bird', 'ghost'], ['bird', 'pirate'], ['bird', 'clown'], ['bird', 'hotdog']]

        self.variables['Alice'] = self.Variable('Alice', domainA)
        self.variables['Bennie'] = self.Variable('Bennie', domainB)
        self.variables['Cher'] = self.Variable('Cher', domainC)
        self.variables['Dominique'] = self.Variable('Dominique', domainD)


    def construct_user_constraints(self, user_friendly_constraints):

        names = ['Alice', 'Bennie', 'Cher', 'Dominique']
        for var1 in names:
            for var2 in names:
                if (not var1 == var2):
                    c = self.Constraint([var1, var2], "not ==", lambda x, y: not x[0] == y[0])
                    self.all_constraints.append(c)
                    self.add_neighbor(var2, c)
                    c = self.Constraint([var1, var2], "not ==", lambda x, y: not x[1] == y[1])
                    self.all_constraints.append(c)
                    self.add_neighbor(var2, c)


        fn1 = lambda x: x[1] == 'pirate'
        constraint1 = self.Constraint(['Alice'], "==", fn1)
        self.all_constraints.append(constraint1)

        fn2 = lambda x: x[1] == 'clown'
        constraint2 = self.Constraint(['Bennie'], "==", fn2)
        self.all_constraints.append(constraint2)

        fn3 = lambda x: x[0] == 'dog' and x[1] == 'hotdog'
        constraint3 = self.Constraint(['Cher'], "==", fn3)
        self.all_constraints.append(constraint3)

        fn4 = lambda x: x[1] == 'ghost' if x[0] == 'fish' else x[1] != 'ghost'
        constraint4 = self.Constraint(['Dominique'], "==", fn4)
        self.all_constraints.append(constraint4)

        fn5 = lambda x: x[0] != 'cat'
        constraint5 = self.Constraint(['Alice'], "!=", fn5)
        self.all_constraints.append(constraint5)


        def make_lambda(opchar, value, unary=False):
            if unary:
                return (lambda x: ConstraintProblem.operators[opchar](x, value))
            else:
                return (lambda x, y:
                        (value == ConstraintProblem.operators[opchar](x, y)) or
                        (value == ConstraintProblem.operators[opchar](y, x)))

    def pretty_print(self, variables):
        for k, v in variables.items():
            print(v.name, ' ', v.domain)


