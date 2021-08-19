#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 23:42:38 2021

@author: GSMolek
"""
import random
#Actions [Up = 0, Down = 1, Left = 2 , Right = 3]
class Snake:
    def __init__(self, board_size, window, canvas, color, outline_color, number_of_rows, number_of_columns, snake_length):
        self.window = window
        self.canvas = canvas
        self.board_size = board_size
        self.color = color
        self.outline_color = outline_color
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.snake_length = snake_length
        self.snake = []
        self.snake_objects = []
        self.block_height = int(self.board_size / self.number_of_rows)
        self.block_width = int(self.board_size / self.number_of_columns)
        self.unallowed_actions=[1, 0, 3, 2]
        self.hit = False
        """
        For snake heading of - 0(up) : 1(down) not allowed
                              1(down) : 0(up) not allowed
                              2(Left) : 3(Right) not allowed
                              3(Right) : 2(left) not allowed
        """
        self.create_snake()
        print(self.snake)
        self.draw_agent_object()
        self.heading_to = self.initialize_heading()
        
    def random_body(self,i = -2, j = -2 ):
        """
        Parameters
        ----------
        i : int,
            The i index of the latest body part of the snake
            if i == -2 and j == -2 it selects random index in the matrix 
            for the first part of the snake body.
            The default is -2.
        j : int,
            the j index of the latest body part of the snake
            if i == -2 and j == -2 it selects random index in the matrix 
            for the first part of the snake body.
            The default is -2.

        Returns
        -------
        int
            The newly generated i index of an additional body part adjacent to the previous, 
            if i == -2, generation of a new i index failed.
        int
            The newly generated j index of an additional body part adjacent to the previous.
            if j == -2, generation of a new j index failed.
        """
        if i == -2 and j == -2 :
            first_i = random.randint(0, self.number_of_rows)
            first_j = random.randint(0, self.number_of_columns)
            return (first_i, first_j)
        new_position = random.randint(0, 3)
        if new_position == 0 and (i-1) != -1 and (j-1) != -1 :
            return (i-1,j)
        elif new_position == 1 and (i+1) != self.number_of_rows and (j+1) != self.number_of_rows :
            return (i+1, j)
        elif new_position == 2 and (j-1) != -1  and (i-1) != -1 :
            return (i,j-1)
        elif new_position == 3 and (j+1) != self.number_of_columns and (i+1) != self.number_of_columns :
            return (i, j+1)
        else:
            return -2,-2

    def create_snake(self):
        """
        Creates the indexes for the snake body according to the snake length provided through the class constructor.
        The indexes are stored in local array called "snake".
        Returns
        -------
        None.

        """
        i=-2
        j=-2
        for k in range(self.snake_length):
            flag=1
            while(flag):
                i_new,j_new = self.random_body(i,j)
                if i_new != -2 and j_new != -2 and i_new != -1 and j_new != -1 and i_new != self.number_of_rows and j_new != self.number_of_columns and (i_new,j_new) not in self.snake:
                    i = i_new
                    j = j_new
                    self.snake.append((i,j))
                    flag = 0
                
    def draw_agent_object(self) :
        """
        Makes the snake indexes stored in the local array called "snake" appear on the grid

        Returns
        -------
        None.

        """
        for index in self.snake :
            i, j = index
            x0 = i * self.block_height
            y0 = j * self.block_width
            x1 = x0 + self.block_height
            y1 = y0 + self.block_width
            self.snake_objects.append(self.canvas.create_rectangle(x0, y0, x1, y1, fill = self.color, outline = self.outline_color)  )      
        self.window.update()
    
    def initialize_heading(self):
        """
        Determine the initial heading of the newely generated snake.

        Returns
        -------
        int
            "0" for "Up", "1" for "Down", "2" for "Left", "3" for "Right"
            initial heading.

        """
        i_head,j_head = self.snake[-1]
        i_body,j_body = self.snake[self.snake_length-2]
        
        if i_body == i_head and j_body-1 == j_head:
            return 1
        if i_body == i_head and j_body+1 == j_head:
            return 0
        if i_body+1 == i_head and j_body == j_head:
            return 2
        if i_body-1 == i_head and j_body == j_head:
            return 3
    
    def is_move_allowed(self,action):
        """
        

        Parameters
        ----------
        action : int
            Check if the next step of the snake is allowed
            "0" for "Up", "1" for "Down", "2" for "Left", "3" for "Right".

        Returns
        -------
        bool
            True - Allowed
            False - Not allowed.

        """
        if action >= 0 and action <=3 :
            if action != self.unallowed_actions[self.heading_to]:
                return True
            return False
    
    def is_hit(self):
        """
        if the snake hit himself or a wall

        Returns
        -------
        bool
            True if a hit detected
            False otherwise.

        """
        i,j = self.snake[-1]
        snake_tail = self.snake[0:self.snake_length - 2]
        print("tail: ")
        print(str(i)+", "+str(j))
        print(snake_tail)
        if (i,j) in snake_tail or i >= self.number_of_columns or j >= self.number_of_rows or j<0 or i<0 :
            return True
        return False
    
    
    def move(self, action):
        """
        moves the snake one step twards up, down, right or left position
        updates the arrays snake and snake_objects
        delets the snakes tail from the canvas and adds a block to the new position

        Parameters
        ----------
        action : int
            integer between 0-3 indicating the direction of movement, where Up = 0, Down = 1, Left = 2, Right = 3.

        Returns
        -------
        None.

        """
        if self.is_move_allowed(action):
            i,j = self.snake[-1]
            if action == 0 :
                self.snake.append((i,j-1))
            elif action == 1 :
                self.snake.append((i,j+1))
            elif action == 2 :
                self.snake.append((i-1,j))
            elif action == 3 :
                self.snake.append((i+1,j))
            i,j = self.snake[-1]
            if self.is_hit():
                self.hit = True
                print("h")
                return
            else:
                x0 = i * self.block_height
                y0 = j * self.block_width
                x1 = x0 + self.block_height
                y1 = y0 + self.block_width
                self.snake_objects.append(self.canvas.create_rectangle(x0, y0, x1, y1, fill = self.color, outline = self.outline_color))
                self.snake.pop(0)
                self.canvas.delete(self.snake_objects[0])
                self.snake_objects.pop(0)
                self.window.update()
            

        