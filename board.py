import pygame
import pymunk
import numpy as np

BLACK = (0, 0, 0, 109)
RED = (255, 0, 0, 100)
YELLOW = (255, 255, 100)
BLUE = (0, 0, 255, 100)

NUMS_TO_COLORS = {1: RED, -1: YELLOW, 0: BLACK}

class Board:
    def __init__(self, rows: int, cols: int, left_corner_x: int, left_corner_y: int, width: int, height: int, color: tuple[int, int, int]):
        self.rows = rows
        self.cols = cols

        self.left_corner_x = left_corner_x
        self.left_corner_y = left_corner_y

        self.width = width
        self.height = height

        self.color = color

        self.chip_matrix = np.zeros((self.rows, self.cols), int)

        self.buffer = 5
        self.token_radius = (self.height - (self.rows + 1) * self.buffer) / (2 * self.rows)

    def draw(self, space):
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = self.left_corner_x + self.width/2, self.left_corner_y + self.height/2

        shape = pymunk.Poly.create_box(body, (self.width, self.height))
        shape.color = BLUE
        space.add(body, shape)

        for i in range(self.rows):
            for j in range(self.cols):
                body = pymunk.Body(body_type = pymunk.Body.STATIC)
                body.position = (self.left_corner_x + (j + 1) * self.buffer + (2 * j + 1) * self.token_radius, 
                                 self.left_corner_y + (i + 1) * self.buffer + (2 * i + 1) * self.token_radius)

                shape = pymunk.Circle(body, self.token_radius)
                shape.color = NUMS_TO_COLORS[self.chip_matrix[i][j]]
                
                space.add(body, shape)                

    def get_num_rows(self):
        return self.rows

    def get_num_cols(self):
        return self.cols

    def get_width(self):
        return self.width
    
    def get_chip_matrix(self):
        return self.chip_matrix
    
    def set_chip_matrix(self, element_x: int, element_y: int, new_num: int):
        self.chip_matrix[element_x][element_y] = new_num
    
    def get_left_corner_x(self):
        return self.left_corner_x
    
    def get_left_corner_y(self):
        return self.left_corner_y

    def get_buffer(self):
        return self.buffer
    
    def get_token_radius(self):
        return self.token_radius
    
    def check_win(self):
        for i in range(self.rows):
            for j in range(self.cols - 3):
                if(self.chip_matrix[i][j] != 0 and self.chip_matrix[i][j] == self.chip_matrix[i][j + 1] and self.chip_matrix[i][j] == self.chip_matrix[i][j + 2] and self.chip_matrix[i][j] == self.chip_matrix[i][j + 3]):
                    return self.chip_matrix[i][j]
        
        for i in range(self.rows - 3):
            for j in range(self.cols):
                if(self.chip_matrix[i][j] != 0 and self.chip_matrix[i][j] == self.chip_matrix[i + 1][j] and self.chip_matrix[i][j] == self.chip_matrix[i + 2][j] and self.chip_matrix[i][j] == self.chip_matrix[i + 3][j]):
                    return self.chip_matrix[i][j]
        
        for i in range(self.rows - 3):
            for j in range(self.cols - 3):
                if(self.chip_matrix[i][j] != 0 and self.chip_matrix[i][j] == self.chip_matrix[i + 1][j + 1] and self.chip_matrix[i][j] == self.chip_matrix[i + 2][j + 2] and self.chip_matrix[i][j] == self.chip_matrix[i + 3][j + 3]):
                    return self.chip_matrix[i][j]
    
        for i in range(3, self.rows):
            for j in range(self.cols - 3):
                if(self.chip_matrix[i][j] != 0 and self.chip_matrix[i][j] == self.chip_matrix[i - 1][j + 1] and self.chip_matrix[i][j] == self.chip_matrix[i - 2][j + 2] and self.chip_matrix[i][j] == self.chip_matrix[i - 3][j + 3]):
                    return self.chip_matrix[i][j]
        
        full = True
        for i in range(self.rows):
            for j in range(self.cols):
                if(self.chip_matrix[i][j] == 0):
                    full = False
                    break
        if(full):
            return 2
        
        return 0
               



