import pygame

class Controls:

    def __init__(self):
        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.right = pygame.K_RIGHT
        self.left = pygame.K_LEFT
        self.fire = pygame.K_SPACE
        self.smart_bomb = pygame.K_LALT
        self.ult = pygame.K_LCTRL
        self.escape = pygame.K_ESCAPE
        self.list_controls = [("Key up : ",self.up), ("Key down : ", self.down),  ("Key right : ",self.right), ("Key left : ", self.left), ("Key to use smart bomb : ", self.smart_bomb), ("Key to use ult : ",self.ult), ("Key to fire : " ,self.fire), ("Key to escape, pause or resume the game : ", self.escape)]

    #Change the key (cannot use it, we do not develop the part of the function)
    def change_key(self, actual_key, input_key):
        if(input_key == self.list_controls[actual_key]):
            self.list_controls[actual_key] = input_key
        elif(input_key in self.list_controls):
            print("Alerte")
        elif(input_key not in self.list_controls):
            self.list_controls[actual_key] = input_key
    
    #Show the keys in the settings
    def show_keys(self, screen):

        #Desplay keys
        for i, key in enumerate(self.list_controls):
            text = pygame.font.SysFont(None, 60).render(key[0] + pygame.key.name(key[1]), True, (255,255,255))
            
            if(i <= 3):
                screen.blit(text, (100 + i*400, 600))

            elif(i <= 6):
                screen.blit(text, (100 + (i-4)*700, 700))

            else:
                screen.blit(text, (100 + (i-7)*400, 800))
            