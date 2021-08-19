#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 17:21:07 2021

@author: GSMolek
"""
import numpy as np
import random

class QLearning:
    def __init__(self, alpha, gamma, epsilon, number_of_rows, number_of_columns, number_of_actions):
        board_size = number_of_columns * number_of_rows
        print("board:" + str(board_size))
        self.q_table = np.zeros((board_size, number_of_actions+1))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.number_of_actions = number_of_actions
        self.number_of_columns = number_of_columns
        self.number_of_rows = number_of_rows
        self.initialize_q_table()
    
    def initialize_q_table(self):
        array = []
        for i in range(0, self.number_of_rows):
            for j in range(0, self.number_of_columns ):
                array.append( self.number_of_columns * i + j)
        print(len(array))
        i = 0
        for x in array:
            self.q_table[i][0] = x
            i = i + 1        
    
    def exploit_or_explore(self,state):
        if random.uniform(0, 1) < self.epsilon:
            step = random.randint(0, self.number_of_actions -1)
            return step
        else:
            step = np.argmax(self.q_table[state][1:3])
            actions_available =[]
            if self.q_table[state][1] == step :
                actions_available.append(0)
            if self.q_table[state][2] == step :
                actions_available.append(1)
            if self.q_table[state][3] == step :
                actions_available.append(2)
            if self.q_table[state][4] == step :
                actions_available.append(3)
            return random.choice(actions_available)
    
    def bellman_equation(self,state,new_state,action,reward):
        self.q_table[state][action + 1] = self.q_table[state][action + 1] + self.alpha * (reward + self.gamma * np.max(self.q_table[new_state][1:4]) - self.q_table[state][action+1])
        
    def print_table(self):
        print(self.q_table)
            
