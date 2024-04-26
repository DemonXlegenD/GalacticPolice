import pygame
import math
import time
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox




class Screen:
    def __init__(self, w, h):
        #Width, height of the screen and of the background
        self.width = w
        self.height = h
        self.bg_width = w
        self.bg_height = h 

        
        #State of the screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.scroll = 0
        self.tiles = math.ceil(self.width/self.bg_width) + 1
        self.seconde = time.time()

        #Background
        pygame.display.set_caption("Shoot'em up")
        self.background = pygame.image.load('PygameAssets/space/bgspace.jpg')
        self.background = pygame.transform.scale(self.background, (self.bg_width, self.bg_height))
        self.banner = pygame.image.load('PygameAssets/space/banner.png')
        self.banner = pygame.transform.scale(self.banner, (600, 500))
        self.banner_rect = self.banner.get_rect()
        self.banner_rect.x = math.ceil((self.screen.get_width()-600)/2)
        self.banner_rect.y = math.ceil(self.screen.get_height()/70)
        self.gameover = pygame.image.load('PygameAssets/gameover.png')
        self.gameover = pygame.transform.scale(self.gameover, (700, 500))
        self.gameover_rect = self.gameover.get_rect()
        self.gameover_rect.x = math.ceil((self.screen.get_width()-700)/2)
        self.gameover_rect.y = -700 

        #Settings 
        self.slider_volume = Slider(self.screen, 400, 500, 800, 20, initial = 100, min=0, max=100, step=1, colour=(255, 255, 255))
        self.slider_volume_visible = False
        self.slider_fps = Slider(self.screen, 400, 500, 800, 20, initial = 40, min=0, max=100, step=10, colour=(255, 255, 255))
        self.slider_fps_visible = False
        self.volume = pygame.font.SysFont("Roboto" ,30).render( "volume", 1 , (255,255,255) )
        self.fps = pygame.font.SysFont("Roboto" ,30).render( "fps", 1 , (255,255,255) )
        self.text_volume = TextBox(self.screen, 1350, 485, 50, 50, fontSize=30)
        self.text_fps = TextBox(self.screen, 1350, 485, 50, 50, fontSize=30)
        self.text_volume.disable()
        self.text_fps.disable()

    #Show the background and the banner of the game in the main menu
    def show_screen(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.banner, self.banner_rect)
        
    #Show the game over screen
    def end_screen(self):    
        self.screen.blit(self.gameover, self.gameover_rect)
        self.gameover_rect.y += 10
        
    #Change the background depending on the levels or where the player is in the game  
    def change_bg(self, path):
        self.background = pygame.image.load(path)
        self.background = pygame.transform.scale(self.background, (self.bg_width, self.bg_height))
    
    #Scroll the background
    def scrolling(self, t):

        if abs(self.scroll) > self.bg_width:
            self.scroll = 0

        for i in range(0, self.tiles):
            self.screen.blit(self.background, (i * self.bg_width + self.scroll, 0))
        
        self.scroll -= t