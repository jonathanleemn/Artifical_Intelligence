import random

from problem import Problem
from copy import deepcopy

class Scheduling(Problem):
    '''
    The scheduling problem is an optimization problem that is attempting to minimize
    the time it takes to complete a collection of jobs distributed across a number of
    people or processors or robots or whatever is doing the work. Formally, it would be
    defined as:
    - A collection of _n_ jobs.
    - Each job _j_ take time <i>t<sub>j</sub></i>
    - There are _p_ people to process the jobs
    - Each person completes his/her last job at time <i>p<sub>t</sub></i>
    - The time to complete all jobs is the maximum over all <i>p<sub>t</sub></i>

    A state can be represented as a list of size _n_. Each element state[i] is in the
    range {0:p-1}, which indicates that job _i_ will be completed by person state[i].
    '''
    
    def __init__(self, job_times, people_count = 3, start_state=None,
                 neighbor_selection="giveLongestToShortest", objective_fn="completeTime", start_fn="random"):
        
        Problem.__init__(self, [])
        self.job_count = len(job_times)
        self.job_times = job_times
        self.people_count = people_count
        self.start_state = start_state
        self.start_fn = start_fn
        # Keeping these in case you want to experiment with objective fn and neighbors
        self.neighbor_selection = neighbor_selection
        self.objective_fn = objective_fn
        self.initialize_neighbor_selection_dict()
        self.initialize_objective_fn_dict()

    def random_solution_state(self):
        # Randomly assign every job to a person
        return [random.randint(0,self.people_count-1) for i in range(self.job_count)]

    def get_initial_state(self):
        if not self.start_fn == "given":
            return self.random_solution_state()
        else:
            return self.start_state

    def get_random_neighbor(self, state):
        copy_state = deepcopy(state)
        return self.selection_for_neighbor[self.neighbor_selection](copy_state)

    # vvvvvvvvvvvvvv  DEFINE a function to get a neighbor  vvvvvvvvvvvvvv
    # put it in the selection_for_neighbor dictionary below
    #def ....
    def replace_for_neighbor(self,state): # replace a random n 
        state[random.randint(0,self.job_count-1)] = random.randint(0,self.people_count-1)
        return state

    def replaceTwo_for_neighbor(self,state): # replace two random n 
        state[random.randint(0,self.job_count-1)] = random.randint(0,self.people_count-1)
        state[random.randint(0,self.job_count-1)] = random.randint(0,self.people_count-1)
        return state

    def replaceFive_for_neighbor(self,state): # replace five random n 
        state[random.randint(0,self.job_count-1)] = random.randint(0,self.people_count-1)
        state[random.randint(0,self.job_count-1)] = random.randint(0,self.people_count-1)
        state[random.randint(0,self.job_count-1)] = random.randint(0,self.people_count-1)
        state[random.randint(0,self.job_count-1)] = random.randint(0,self.people_count-1)
        state[random.randint(0,self.job_count-1)] = random.randint(0,self.people_count-1)
        return state

    def replaceLongest_for_neighbor(self,state): # find the person with maxTime and give their longest job to a random other person (the random person could be them
        max_time = 0
        maxP = -1
        for p in range(self.people_count):
            pTime = 0
            for i in range(self.job_count):
                if state[i] == p:
                    pTime = pTime + self.job_times[i]
            if max_time < pTime:
                max_time = pTime
                maxP = p
        maxJ = -1
        for i in range(self.job_count):
            if state[i] == maxP:
                if maxJ == -1:
                    maxJ = i
                if self.job_times[i] > self.job_times[maxJ]:
                    maxJ = i
        state[maxJ] = random.randint(0,self.people_count-1)
        return state

    def giveLongestToShortest_for_neighbor(self,state): # find the person with maxTime and give their longest job to the person with minTime
        max_time = 0
        min_time = -1
        maxP = -1
        minP = -1
        for p in range(self.people_count):
            pTime = 0
            for i in range(self.job_count):
                if state[i] == p:
                    pTime = pTime + self.job_times[i]
            if max_time < pTime:
                max_time = pTime
                maxP = p
            if min_time == -1:
                minTime = pTime
                minP = p
            if min_time > pTime:
                minTime = pTime
                minP = p
        maxJ = -1
        for i in range(self.job_count):
            if state[i] == maxP:
                if maxJ == -1:
                    maxJ = i
                if self.job_times[i] > self.job_times[maxJ]:
                    maxJ = i
        state[maxJ] = minP
        return state

    def new_for_neighbor(self, state):
        return self.random_solution_state()


    def apply_objective_function(self, state):
        return self.functions_for_evaluation[self.objective_fn](state)

    # vvvvvvvvvvvvvv  DEFINE at least one objective function  vvvvvvvvvvvvvv
    # put it in the functions_for_evaluation dictionary below
    #def ...
    def complete_time(self,state): # return max pt
        max_time = 0
        for p in range(self.people_count):
            pTime = 0
            for i in range(self.job_count):
                if state[i] == p:
                    pTime = pTime + self.job_times[i]
            if max_time < pTime:
                max_time = pTime
        return max_time


    # vvvvvvvvvvvvv   ADD YOUR neighbor and objective fn here vvvvvvvvvvvvvv
    # "new": generate entirely new state by calling random_solution_state
    def initialize_neighbor_selection_dict(self):
        self.selection_for_neighbor = {
            "replace": self.replace_for_neighbor,
            "replaceTwo": self.replaceTwo_for_neighbor,
            "replaceFive": self.replaceFive_for_neighbor,
            "replaceLongest": self.replaceLongest_for_neighbor,
            "giveLongestToShortest": self.giveLongestToShortest_for_neighbor,
            "new": self.new_for_neighbor
        }

    def initialize_objective_fn_dict(self):
        self.functions_for_evaluation = {
            "completeTime": self.complete_time
        }

    def pretty_print(self, node):
        job_assignment = node.state
        print("Value ", self.apply_objective_function(node.state))
        for p in range(self.people_count):
            jobs = [i for i in range(self.job_count) if job_assignment[i]==p]
            print(p,'has jobs',end=" ")
            print(jobs)

def all_unique(elements):
    try:
        answer = len(set(elements)) == len(elements)
    except:
        print('FAIL ',elements)
        return True
    return answer




