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
        self.q_table = np.zeros((board_size, number_of_actions))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.number_of_columns = number_of_columns
        self.number_of_rows = number_of_rows
        self.initialize_q_table()
    
    def initialize_q_table(self):
        array = []
        for i in range(0, self.number_of_rows - 1):
            for j in range(0, self.number_of_columns - 1):
                array.append( self.number_of_columns * i * j)
        print(len(array))
        for i in array:
            self.q_table[i][0] = array[i]                
    """
    def exploit_or_explore(self,state):
        if random.uniform(0, 1) < self.epsilon:
            step = random.randint(0, number_of_actions - 1)
        else:
    """
    def print_table(self):
        print(self.q_table)
            
