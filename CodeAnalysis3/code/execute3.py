import sys
import random

sys.path.append('problems')
sys.path.append('algorithms')

from annealing import SimulatedAnnealing
from nqueens import NQueens
from scheduling import Scheduling

if __name__ == '__main__':
   # problem = NQueens(10,
   #                   neighbor_selection="swap",
   #                   objective_fn="all",
   #                   start_fn="permute",
   #                   start_state=[6, 6, 6, 0, 7, 0, 8, 6, 9, 7])

    algorithm = SimulatedAnnealing(
        verbose=False,
        alpha=.98,
        start=600000,
        end=.25,
        iterations=500)

    # solution = algorithm.solve(problem)
    # algorithm.save_data()
    # algorithm.print_solution()
    # algorithm.print_stats()

    # For when scheduling is working
    max_time = 100 # arbitrary maximum time for any given task
    n = 40 # (number of jobs)
    p = 10 # (number of people)
    times = [random.randint(1,max_time) for i in range(n)]
    problem = Scheduling( job_times = times, people_count = p)
    #
    solution = algorithm.solve(problem)
    algorithm.print_solution()
    algorithm.print_stats()