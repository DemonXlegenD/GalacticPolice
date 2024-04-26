import pygame
from spaceship import Spaceship

class UltimateCharging():
    def __init__(self, difficulty):
        self.percent = 0
        self.percent_speed = 4 / difficulty

    #Add percent to the gauge ultimate
    def add_percent(self):
        self.percent += self.percent_speed / 100

    #Update the ultimate bar
    def update_bar(self, surface, Player):

        self.add_percent()

        if self.percent >= 100 and Player.ult == False:
            Player.ult = True
            print(Player.ult)


        #background bar (grey)
        pygame.draw.rect(surface, (114, 101, 98), [
            0, # X
            surface.get_height()-40, # Y
            surface.get_width(), #window length
            20 #thickness
        ])

        # dark blue bar: ult gauge
        pygame.draw.rect(surface, (0, 90, 211), [
            0, # X
            surface.get_height()-40, # Y
            (surface.get_width() /100) * self.percent, #window length
            20 #thickness
        ])