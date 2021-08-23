#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 11:05:19 2021

@author: GSMolek
"""
import json
from tkinter import *
from PIL import ImageTk,Image
from Snake import Snake
from QLearning import QLearning
import time
import csv
import os
import numpy as np
import random

class Environment():
    def __init__(self, board_size, number_of_rows, number_of_columns, blocks_color, frame_color) :
        self.window = Tk()
        self.window.title("Snake AI")
        self.board_size = board_size
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.number_of_blocks = number_of_columns*number_of_rows
        self.block_height = int(self.board_size / self.number_of_rows)
        self.block_width = int(self.board_size / self.number_of_columns)
        self.blocks_color = blocks_color
        self.frame_color = frame_color
        self.environment_blocks = []
        self.blocks_dictionary={}
        self.blocks_dicovered = np.zeros((number_of_rows,number_of_columns))
        self.canvas = Canvas(self.window,width = board_size,height = board_size)
        self.canvas.pack()
        self.initialize_board()
        self.window.update()
        
    def initialize_board(self):
        """
        Displaying a grid with the sizes provided through the constructor.
        Also, it appends the block created into the local array called "environment_blocks"

        Returns
        -------
        None.

        """
        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns):
                x0 = i * self.block_height
                y0 = j * self.block_width
                x1 = x0 + self.block_height
                y1 = y0 + self.block_width
                block = self.canvas.create_rectangle(x0,y0,x1,y1,fill = self.blocks_color,outline = self.frame_color,)
                self.environment_blocks.append(block)
                key = str(i)+","+str(j)
                print(key)
                self.blocks_dictionary[key] = block
                self.window.update()

    
    def pass_through_block(self, i, j):
        key = str(i)+","+str(j)
        self.canvas.itemconfig(self.blocks_dictionary[key],fill = "#525263")
        self.blocks_dicovered[i][j] = 1
    
    def reset_all_blocks(self):
        self.blocks_dicovered = np.zeros((self.number_of_rows,self.number_of_columns))
        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns):
                key = str(i)+","+str(j)
                self.canvas.itemconfig(self.blocks_dictionary[key], fill = self.blocks_color )
    
    def reward(self,state):
        i,j = state
        if i<0 or j < 0 or i>=self.number_of_columns or j>=self.number_of_rows:
            return -1000
        if self.blocks_dicovered[i][j] == 0 :
            return 10
        else:
            return -10

    def find_next_step(self,i, j, action):
        if action == 0:
            return (i,j-1)
        if action == 1:
            return (i, j+1)
        if action == 2:
            return (i-1,j)
        if action == 3:
            return (i+1,j)

if __name__ == '__main__':
    env = Environment(600,13,13,blocks_color = "#6bb578",frame_color = "#cbd1cc")
    snake = Snake(env.board_size,env.window, env.canvas,"#2be3c7","#000000", 13, 13, 3)
    q = QLearning(0.01,0.9,0.1, 13, 13, 4)
    if os.path.exists("q_table.txt"):
        q.q_table = np.loadtxt("./q_table.txt")
    for episode in range(100000):
        env.reset_all_blocks()
        snake.restart_snake()
        while(True):
            if episode > 1000:
                time.sleep(0.5)
            i,j = snake.snake[-1]
            a = q.exploit_or_explore(env.number_of_rows*i + j)
            if not snake.is_move_allowed(a):
                a = q.exploit_second_best(env.number_of_rows*i+j)
            i_next,j_next = env.find_next_step(i, j, a)
            snake.move(a)
            if snake.is_hit():
                key = str(i)+","+str(j)
                key2 = str(i_next)+","+str(j_next)
                print("position")
                print(a)
                print(q.q_table[a+1])
                print("key")
                print(key)
                print(key2)
                q.bellman_equation(env.number_of_rows*i+j, env.number_of_rows*i_next+j_next, a, env.reward((i_next,j_next)))
                env.reset_all_blocks()
                break
            q.bellman_equation(env.number_of_rows*i+j, env.number_of_rows*i_next+j_next, a, env.reward((i,j)))
            env.pass_through_block(i_next, j_next)
            if 0 not in env.blocks_dicovered:
                print("well done!")
                break
            env.window.update()