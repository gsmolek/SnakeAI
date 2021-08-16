#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 11:05:19 2021

@author: popos
"""
from tkinter import *
from PIL import ImageTk,Image
from Snake import Snake
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

env = Environment(600,13,13,blocks_color = "#6bb578",frame_color = "#cbd1cc")
snake = Snake(env.board_size,env.window, env.canvas,"#2be3c7","#000000", 13, 13, 3)        