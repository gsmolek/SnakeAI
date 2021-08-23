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
        self.board_size = (number_of_columns) * (number_of_rows)
        self.q_table = np.zeros((self.board_size, number_of_actions+1))
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
        i = 0
        for x in array:
            self.q_table[i][0] = x
            i = i + 1        
    
    def exploit_or_explore(self,state):
        if random.uniform(0, 1) < self.epsilon:
            step = random.randint(0, self.number_of_actions -1)
            return step
        else:
            step = np.argmax(self.q_table[state][1:5])
            actions_available =[]
            if self.q_table[state][1] == self.q_table[state][step+1] :
                actions_available.append(0)
            if self.q_table[state][2] == self.q_table[state][step+1] :
                actions_available.append(1)
            if self.q_table[state][3] == self.q_table[state][step+1] :
                actions_available.append(2)
            if self.q_table[state][4] == self.q_table[state][step+1] :
                actions_available.append(3)
            return random.choice(actions_available)
    
    def exploit_second_best(self,state):
        step = self.q_table[state][1:5]
        temp = self.q_table[state][1:5]
        actions_available =[]
        np.sort(temp)
        if temp[1] == step[0]:
            actions_available.append(0)
        if temp[1] == step[1]:
            actions_available.append(1)
        if temp[1] == step[2]:
            actions_available.append(2)
        if temp[1] == step[3]:
            actions_available.append(3)
        return random.choice(actions_available)
    
    def bellman_equation(self,state,new_state,action,reward):
        if state<0 or state >= self.board_size or new_state<0 or new_state >= self.board_size:
            self.q_table[state][action + 1] = self.q_table[state][action + 1] + self.alpha * (reward + self.gamma * (-1000) - self.q_table[state][action+1])
        else:
            self.q_table[state][action + 1] = self.q_table[state][action + 1] + self.alpha * (reward + self.gamma * np.max(self.q_table[new_state][1:4]) - self.q_table[state][action+1])
        
    def print_table(self):
        print(self.q_table)
            
