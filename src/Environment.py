#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 11:05:19 2021

@author: GSMolek
"""
from tkinter import *
from PIL import ImageTk,Image
from Snake import Snake
from QLearning import QLearning
import time

class Environment():
    def __init__(self, board_size, number_of_rows, number_of_columns, blocks_color, frame_color) :
        self.window = Tk()
        self.window.title("Snake AI")
        self.board_size = board_size
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.block_height = int(self.board_size / self.number_of_rows)
        self.block_width = int(self.board_size / self.number_of_columns)
        self.blocks_color = blocks_color
        self.frame_color = frame_color
        self.environment_blocks = []
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
                self.environment_blocks.append(self.canvas.create_rectangle(x0,y0,x1,y1,fill = self.blocks_color,outline = self.frame_color,))
    
    def reward(self,state):
        i,j = state
        if i<0 or j < 0 or i>=self.number_of_columns or j>=self.number_of_rows:
            return -100
        else:
            return 0

    def find_next_step(self,i, j, action):
        if action == 0:
            return (i,j-1)
        if action == 1:
            return (i, j+1)
        if action == 2:
            return (i-1,j)
        if action == 3:
            return (i+1,j)
        
env = Environment(600,13,13,blocks_color = "#6bb578",frame_color = "#cbd1cc")
snake = Snake(env.board_size,env.window, env.canvas,"#2be3c7","#000000", 13, 13, 5)
q = QLearning(0.9,0.9,0.1, 13, 13, 4)
q.print_table()
while(True):
    time.sleep(1)
    i,j = snake.snake[-1]
    a = q.exploit_or_explore(3*i + j)
    if snake.is_move_allowed(a):
        i_next,j_next = env.find_next_step(i, j, a)
        q.bellman_equation(3*i+j, 3*i_next+j_next, a, env.reward((i,j)))
        snake.move(a)
        if snake.is_hit():
            break
    env.window.update()     