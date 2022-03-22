# Week 1 Lab 1 Assignment

import numpy as np
import sys
from time import time

class Node:
    def __init__(self, parent, st, p_cost, h_cost):
        
        self.parent = parent
        self.st = st
        self.p_cost = p_cost
        self.h_cost = h_cost
        self.cost = p_cost + h_cost
    
    def __hash__(self):
        
        return hash(''.join(self.st.flatten()))
    
    def __str__(self):
        return str(self.st)
    
    def __eq__(self, other):
        
        return hash(''.join(self.st.flatten())) == hash(''.join(other.st.flatten())) 
    
    def __ne__(self, other):
        return hash(''.join(self.st.flatten())) != hash(''.join(other.st.flatten()))

class PriorityQueue():
    
    def __init__(self):
        self.queue = []

    def pop(self):
        
        next_st = None
        st_cost = 10**18
        idx = -1
        
        for i in range(len(self.queue)):
            
            if self.queue[i].cost<st_cost:
                st_cost = self.queue[i].cost
                idx = i
        
        return self.queue.pop(idx) 

    def __str__(self):
        l = []
        for i in self.queue:
            l.append(i.st)
        
        return str(l)

    def push(self, node):
        self.queue.append(node)


    def __len__(self):
        return len(self.queue)
    
    def is_empty(self):    
        return len(self.queue)==0
    

    

            
class Environment():
    
    def __init__(self, dep = None, goal_st = None):
        self.actions = [1,2,3,4] #1 - Up, 2 - Down, 3 - Right, 4 - Left
        self.goal_st = goal_st
        self.dep = dep
        self.start_st = self.generate_start_st()


    def get_start_st(self):
        return self.start_st
    
    def get_goal_st(self):
        return self.goal_st

    
    def generate_start_st(self):
        
        past_st = self.goal_st
        i=0
        while i!= self.dep:
            new_sts = self.get_next_sts(past_st)
            choice = np.random.randint(low=0, high=len(new_sts))
            
            if np.array_equal(new_sts[choice], past_st):
                continue
            
            past_st = new_sts[choice]
            i+=1
            
        return past_st
    

    
    def get_next_sts(self, st):
        
        space = (0,0)
        for i in range(3):
            for j in range(3):
                if st[i,j] == '_':
                    space = (i,j)
                    break
        
        new_sts = []
        
        if space[0] > 0:# Move Up
            new_st = np.copy(st)
            
            val = new_st[space[0], space[1]]
            new_st[space[0], space[1]]  = new_st[space[0]-1, space[1]]
            new_st[space[0]-1, space[1]] = val
            
            new_sts.append(new_st)
            
        if space[0] < 2: #Move down
            new_st = np.copy(st)
            
            val = new_st[space[0], space[1]]
            new_st[space[0], space[1]]  = new_st[space[0]+1, space[1]]
            new_st[space[0]+1, space[1]] = val
            
            new_sts.append(new_st)
        
        if space[1]<2: #Move right
            new_st = np.copy(st)
            
            val = new_st[space[0], space[1]]
            new_st[space[0], space[1]] = new_st[space[0], space[1]+1]
            new_st[space[0], space[1]+1] = val
            
            new_sts.append(new_st)
            
        if space[1] > 0: #Move Left
            new_st = np.copy(st)
            
            val = new_st[space[0], space[1]]
            new_st[space[0], space[1]] = new_st[space[0], space[1]-1]
            new_st[space[0], space[1]-1] = val
            
            new_sts.append(new_st)
        
        return new_sts
    
    def reached_goal(self, st):
        
        for i in range(3):
            for j in range(3):
                if st[i,j] != self.goal_st[i,j]:
                    return False
        
        return True


class Agent:
    
    def __init__(self, env, heuristic):
        self.frontier = PriorityQueue()
        self.explored = dict()
        self.start_st = env.get_start_st()
        self.goal_st = env.get_goal_st()
        self.env = env
        self.goal_node = None
        self.heuristic = heuristic
    
    def run(self):
        init_node = Node(parent = None, st = self.start_st, p_cost = 0, h_cost=0)
        self.frontier.push(init_node)
        steps = 0
        while not self.frontier.is_empty():

            curr_node = self.frontier.pop()

            next_sts = self.env.get_next_sts(curr_node.st)

            if hash(curr_node) in self.explored:
                continue

            self.explored[hash(curr_node)] = curr_node

            if self.env.reached_goal(curr_node.st):
                self.goal_node = curr_node
                break
            goal_st = self.env.get_goal_st()

            l = []
            for st in next_sts:

                h_cost = self.heuristic(st, goal_st)
                node = Node(parent=curr_node, st=st, p_cost=curr_node.p_cost+1, h_cost=h_cost)
                self.frontier.push(node)
            steps += 1
        
        
        return steps, self.soln_dep()
    
    def soln_dep(self):
        node = self.goal_node
        count = 0
        while node is not None:
            node = node.parent
            count+=1
        
        return count
    
    def print_nodes(self):
        
        node = self.goal_node
        l = []
        while node is not None:
            l.append(node)
            node = node.parent

        step = 1
        for node in l[::-1]:
            print("Step: ",step)
            print(node)
            step+=1
    
    def get_memory(self):
        
        mem = len(self.frontier)*56 + len(self.explored)*56
        return mem



def heuristic0(curr_st, goal_st):
    return 0


def heuristic1(curr_st, goal_st):
    
    count = 0
    for i in range(3):
        for j in range(3):
            if curr_st[i, j]!=goal_st[i,j]:
                count+=1
    
    return count

def heuristic2(curr_st, goal_st):
    
    dist = 0

    for i in range(3):
        for j in range(3):
            ele = curr_st[i, j]
            goal_i, goal_j = np.where(goal_st==ele)
            d = abs(goal_i[0] - i) + abs(goal_j[0] - j)
            dist += d
    
    return dist

dep = 500
goal_st = np.array([[1,2,3], [8,'_',4], [7,6,5]])
env = Environment(dep, goal_st)
print("Start st: ")
print(env.get_start_st())
print("Goal st: ")
print(goal_st)

agent = Agent(env = env, heuristic = heuristic2)

agent.run()

deps = np.arange(0,501,50)
goal_st = np.array([[1,2,3], [8,'_',4], [7,6,5]])
times_taken = {}
mems = {}
for dep in deps:
    
    time_taken = 0
    mem = 0
    for i in range(50):
        env = Environment(dep=dep, goal_st=goal_st)
        agent = Agent(env = env, heuristic = heuristic2)
        start_time = time()
        agent.run()
        end_time = time()
        time_taken+=end_time - start_time
        mem+=agent.get_memory() 
    
    time_taken/=50
    mem = mem/50
    times_taken[dep] = time_taken
    mems[dep] = mem
    print(dep, time_taken, mem)