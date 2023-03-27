import pygame
import button
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class DropDown():

    def __init__(self, enable_button: button.Button, options: np.array):
        self.enable_button = enable_button

        self.options = options
        self.option_buttons = np.array([])
        self.current_option = 0

        self.font_size = self.enable_button.get_font_size()
        self.show_full_menu = False

        for i in range(self.options.size):
            self.option_buttons = np.append(self.option_buttons, button.Button(color = WHITE, 
                                                                                     left_corner_x = enable_button.get_x(), 
                                                                                     left_corner_y = enable_button.get_y() + (i + 1) * enable_button.get_height(), 
                                                                                     width = enable_button.get_width(), 
                                                                                     height = enable_button.get_height(),
                                                                                     font_size = self.font_size,
                                                                                     text = self.options[i]))        
    
    def draw(self, window):
        if(not self.show_full_menu):
            for i in range(len(self.options)):
                self.option_buttons[i].change_color(BLACK)
                self.option_buttons[i].draw(window)
                self.option_buttons[i].change_color(WHITE)

            self.enable_button.draw(window, outline = BLACK)

            self.option_buttons[self.current_option].change_left_corner_y(self.enable_button.get_y() + self.enable_button.get_height())
            self.option_buttons[self.current_option].draw(window, outline = BLACK)
            self.option_buttons[self.current_option].change_left_corner_y(self.enable_button.get_y() + (self.current_option + 1) * self.enable_button.get_height())
        else:
            for i in range(self.options.size):
                self.option_buttons[i].draw(window, outline = BLACK)

    def update(self, window):
        mouse_pos = pygame.mouse.get_pos()
        if (self.enable_button.is_over_mouse(mouse_pos)):
            self.show_full_menu = not self.show_full_menu
        elif(self.show_full_menu == True):
            for i in range(self.options.size):
                if(self.option_buttons[i].is_over_mouse(mouse_pos)):
                    self.current_option = i
                    self.show_full_menu = False
                    break
        
        self.draw(window)
    
    def is_over_mouse(self, pos) -> bool:
        is_on_option_buttons = False
        for option_button in self.option_buttons:
            if(option_button.is_over_mouse(pos)):
                is_on_option_buttons = True
                break
        
        return self.enable_button.is_over_mouse(pos) or (self.show_full_menu and is_on_option_buttons)
    
    def get_current_option(self) -> str:
        return self.options[self.current_option]
    
    def get_show_full_menu(self) -> bool:
        return self.show_full_menu