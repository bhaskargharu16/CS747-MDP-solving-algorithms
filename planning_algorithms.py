import numpy as np
import time
from pulp import *

class MDP(object):
    def __init__(self):
        self.numStates = 0
        self.numActions = 0
        self.start = 0
        self.end = []
        self.transition_matrix = None
        self.transition_probability_matrix = None
        self.mdptype = ""
        self.discount = 0
    
    def initialise_mdp(self,filepath):
        lines = open(filepath,'r').readlines()
        lines = [line.strip() for line in lines]
        self.numStates = int(lines[0].strip().split()[1])
        self.numActions = int(lines[1].strip().split()[1])
        self.transition_matrix = np.zeros((self.numStates,self.numActions,self.numStates)).astype(float)
        self.transition_probability_matrix = np.zeros((self.numStates,self.numActions,self.numStates)).astype(float)
        self.start = int(lines[2].strip().split()[1])
        self.end = [int(x) for x in lines[3].strip().split()[1:]]
        for idx,line in enumerate(lines[4:-2]):
            line = line.strip().split()
            self.transition_matrix[int(line[1])][int(line[2])][int(line[3])] = float(line[4])
            self.transition_probability_matrix[int(line[1])][int(line[2])][int(line[3])] = float(line[5])
        self.mdptype = lines[-2].strip().split()[1]
        self.discount = float(lines[-1].strip().split()[1])
        return self
    
    def value_iteration(self):
        value_vector = np.zeros(self.numStates).astype(float)
        policy_vector = np.zeros(self.numStates)
        while True:
            old = value_vector
            value_vector = np.max(np.sum(np.multiply(self.transition_probability_matrix,self.transition_matrix + self.discount * value_vector),axis=2),axis=1)
            if np.sum(np.abs(value_vector - old)) <= 1e-12:
                break
        policy_vector = np.argmax(np.sum(np.multiply(self.transition_probability_matrix,self.transition_matrix + self.discount * value_vector),axis=2),axis=1)
        return value_vector,policy_vector

    def linear_programming(self):
        prob = LpProblem("MDP", LpMinimize)
        value_vector = np.array([LpVariable("V"+str(i)) for i in range(self.numStates)])
        prob += np.sum(value_vector) #objective function
        equations = np.sum(np.multiply(self.transition_probability_matrix,self.transition_matrix + self.discount * value_vector),axis=2)
        for s in range(self.numStates):
            for a in range(self.numActions):
                prob += value_vector[s] >= equations[s][a]
        prob.solve(PULP_CBC_CMD(msg=0))
        optimal_value_vector = np.zeros(self.numStates)
        for i in range(self.numStates):
            optimal_value_vector[i] = float(value_vector[i].varValue)
        optimal_policy_vector = np.argmax(np.sum(np.multiply(self.transition_probability_matrix,self.transition_matrix + self.discount * optimal_value_vector),axis=2),axis=1)
        return optimal_value_vector,optimal_policy_vector
    
    def get_value_function(self,policy_vector):
        states = np.array(range(self.numStates))
        rhs = np.sum(self.transition_matrix[states,policy_vector,:]*self.transition_probability_matrix[states,policy_vector,:],axis=1)
        coeffs = np.identity(self.numStates) - self.discount * self.transition_probability_matrix[states,policy_vector,:]
        coeffs = np.linalg.pinv(coeffs)
        value_vector = np.matmul(coeffs,rhs)
        return value_vector

    def howard_policy_iteration(self):
        value_function = np.zeros(self.numStates)
        policy_vector = np.zeros(self.numStates).astype(int)
        while True:
            policy = np.copy(policy_vector)
            value_function = self.get_value_function(policy)
            policy_vector = np.argmax(np.sum(np.multiply(self.transition_probability_matrix,self.transition_matrix + self.discount * value_function),axis=2),axis=1)
            if  all(policy_vector == policy):
                break
        return value_function, policy_vector
        
    def solve_mdp(self,filepath,algorithm):
        start = time.time()
        self.initialise_mdp(filepath)
        if algorithm == 'vi':
            value_vector,policy_vector = self.value_iteration()
            for x,y in zip(value_vector,policy_vector):
                print(x,y)
        elif algorithm == 'lp':
            optimal_value_vector,optimal_policy_vector = self.linear_programming()
            for x,y in zip(optimal_value_vector,optimal_policy_vector):
                print(x,y)
        elif algorithm == 'hpi':
            optimal_value_vector,optimal_policy_vector = self.howard_policy_iteration()
            for x,y in zip(optimal_value_vector,optimal_policy_vector):
                print(round(x,6),y)
        return self