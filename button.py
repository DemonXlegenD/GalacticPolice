import pygame
import math


class Button:
    def __init__(self, screen, x, y, w, h, path):
        self.screen = screen

        #Settings
        self.posx = x
        self.posy = y 
        self.width = w 
        self.height = h
        self.path = path
        self.button = pygame.image.load(self.path)
        self.button = pygame.transform.scale(self.button, (self.width, self.height))
        self.button_rect = self.button.get_rect()
        self.button_rect.x = math.ceil((self.screen.width-self.width)/self.posx)
        self.button_rect.y = math.ceil((self.screen.height-self.height)/self.posy)
        self.is_pressed = False
        self.is_shown = False

    #Display the button
    def show_button(self):
        
        if(self.is_shown):
            #Mouse position
            souris_x, souris_y = pygame.mouse.get_pos()

            #Check if the mouse is over the button (Hover)
            if self.button_rect.x < souris_x < self.button_rect.x + self.width and self.button_rect.y < souris_y < self.button_rect.y + self.height:
                #Button magnification
                self.button = pygame.image.load(self.path)
                self.button = pygame.transform.scale(self.button, (self.width * 1.2, self.height * 1.2))
                self.screen.screen.blit(self.button, ((self.button_rect.x  - (self.width * 1.2 - self.width)/2, (self.button_rect.y  - (self.height * 1.2 - self.height)/2))))
            else:
                self.button = pygame.image.load(self.path)
                self.button = pygame.transform.scale(self.button, (self.width, self.height))
                self.screen.screen.blit(self.button, self.button_rect)
        
