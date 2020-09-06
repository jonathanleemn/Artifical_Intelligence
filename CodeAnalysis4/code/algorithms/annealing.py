# http://katrinaeg.com/simulated-annealing.html
# http://www.cs.nott.ac.uk/~gxk/aim/notes/simulatedannealing.doc

from datetime import datetime
import random, math
import decimal
from node import Node, NodeFactory
from algorithm import Algorithm

class SimulatedAnnealing(Algorithm):
    def __init__(self, verbose=False, alpha=.98, start=500000, end=.25, iterations=200):
        Algorithm.__init__(self, verbose)
        self.solution = []  # using a list to follow convention of previous algo's

        # Related to the temperature schedule
        # T = T*alpha is applied every "iterations"
        self.alpha = alpha          # Increase to slow cooling
        self.start_temp = start     # Increase to run algorithm longer
        self.end_temp = end         # At about .25, the probability is near 0
        self.iterations_per_temp = iterations       # increase to slow cooling
        
        self.temperature = start
        self.temp_iterations = 0
        self.elapsed_time = 0
        self.start_time = datetime.now()
        # value and temp stored at each iteration then written to file for graphing
        self.value_data = []
        self.temperature_data = []
        self.moves_to_better = 0
        self.moves_to_worse = 0

    def adjust_temperature(self):
        # temperature is cooled every X iterations
        # there are a variety of approaches to adjusting the temperature
        # Here, we are decreasing by a % (alpha) at each adjustment
        self.temp_iterations += 1
        if self.temp_iterations >= self.iterations_per_temp:
            self.temperature *= self.alpha
            self.temp_iterations = 0
            if self.verbose: print('temperature now ', self.temperature)
        self.temperature_data.append(self.temperature)

    def calculate_probability(self, error):
        # there could be other means of calculating probability
        return math.exp(error/self.temperature)
        
    def solve(self, problem):
        self.problem = problem
        # Not a great name for it, but Node is a useful structure for annealing
        node_factory = NodeFactory(verbose=self.verbose)
        node = node_factory.make_node(problem.get_initial_state())
        node.value = problem.apply_objective_function(node.state)
        # at each iteration, self.solution will contain the best seen so far
        self.solution = [node]
        if self.verbose:
            print("Initial state: ", problem.pretty_print(node))
            print("Evaluation: ", node.value)
        if node.value == 0:
            self.total_node_count = 1
            return self.solution

        while self.temperature > self.end_temp:
            # get a neighbor and decide to change to that state
            next_node = node_factory.make_node(problem.get_random_neighbor(node.state))
            next_node.value = problem.apply_objective_function(next_node.state)
            self.value_data.append(next_node.value)
            if next_node.value == 0:
                self.solution = [next_node]
                self.total_node_count = node_factory.node_count
                return self.solution
            if next_node.value <= node.value:
                node = next_node
                self.moves_to_better += 1
                if node.value < self.solution[0].value:
                    self.solution = [node]
            else:
                if random.uniform(0,1) <= self.calculate_probability(node.value-next_node.value):
                    node = next_node
                    self.moves_to_worse += 1
            self.adjust_temperature()

        self.total_node_count = node_factory.node_count
        self.elapsed_time = self.calculate_elapsed_time()
        if self.verbose:
            print("Elapsed Time: %sms" % (str(self.elapsed_time)))

        return self.solution

    def save_data(self):
        # store the data in a file for graphing (overwrites file)
        file = open("value.txt","w")
        for i in self.value_data:
            file.write(str(i))
            file.write('\n')
        file.close()
        file = open("temp.txt","w")
        for i in self.temperature_data:
            file.write(str(i))
            file.write('\n')
        file.close()

    def calculate_elapsed_time(self):
        end_time = datetime.now()
        elapsed_time = (end_time - self.start_time).microseconds / 1000
        return elapsed_time

    def print_stats(self):
        no_move = self.total_node_count - self.moves_to_better - self.moves_to_worse
        print("Total iterations: ", self.total_node_count)
        print("Moves to better states: ", self.moves_to_better)
        print("Moves to worse states: ", self.moves_to_worse)
        print("Did not move to neighbor: ", no_move)

#if __name__ == '__main__':
#    problem = problem()
#    print("problem:")
#    print(problem)
#    SimulatedAnnealing(problem).run()
