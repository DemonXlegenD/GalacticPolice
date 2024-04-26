import pygame
import time
from projectile import Projectile
from particles import Smart_bomb
import animation

GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

#Classe du vaiseau du joueur
class Spaceship(animation.AnimateSprite):

    def __init__(self, game, max_hp, velocity, attack, planete):
        self.game = game
        #Settings
        self.hp = max_hp
        self.max_hp = max_hp
        self.velocity = velocity                 
        self.upgrade = 1
        self.attack = attack * (self.upgrade/2)
        self.ult = False
        self.smart_bomb_count = 5
        self.planete = planete
        self.killed = 0

        # Animation
        self.first_frame = True
        self.wait_anim = time.time()
        if self.upgrade == 1:
            super().__init__(False, 'spaceship1_', (200,150))

        #Image
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 200

        #Group of sprites
        self.all_projectile = pygame.sprite.Group()
        self.all_upgrades = pygame.sprite.Group()
        self.all_smart_bomb = pygame.sprite.Group()

    #Update the animation
    def update_animation(self):
        self.animate()
        self.first_frame = False

    #Update the health bar of the player
    def update_health_bar(self, surface):

        #Set life gauge color
        if(self.hp > 150):
            bar_color = GREEN #Green color

        elif(self.hp > 50 and self.hp <= 150):
            bar_color = YELLOW #Yellow color

        else:
            bar_color = RED #Red color

        #set a color for the gauge background
        back_bar_color = (60, 60, 60)

        #define the position of the gauge of life + width thickness
        hp = (self.hp / self.max_hp) * 200
        bar_position = [self.rect.x, self.rect.y - 20, hp, 10]
        #define the position of the background of the gauge
        back_bar_position = [self.rect.x, self.rect.y - 20, 200, 10]

        #draw the bar of life
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    #Launch a projectile when the player hit the space key
    def launch_projectile(self):
        self.all_projectile.add(Projectile(self, 0, 0, self.upgrade, self.planete)) # les 0 signifient que le projectile est lancé par le joueur
        self.start_animation()

    #Remove all the enemy when ultimate is ready and the player hit the ctrl key
    def ultimate(self, ultime):
        if self.ult == True:
            for enemy in self.game.all_enemy:
                enemy.remove(True, True)
            ultime.percent = 0
            self.ult = False

    #Remove all the projectiles in the area of the smart bomb
    def smart_bomb(self):
        if self.smart_bomb_count != 0:
            for enemy in self.game.all_enemy:
                for proj in enemy.all_projectile:
                    proj.remove()
                    self.smart_bomb_count -= 1
            self.all_smart_bomb.add(Smart_bomb(self.rect.x, self.rect.y, self))
                        # Fix the smart bomb: lag + enlargement problems + prevent shooting after a few seconds
            self.smart_bomb_count -= 1

    #Get health from something             
    def get_health(hp, max_hp, heal):
        if hp+heal <= max_hp:
            hp += heal
        else:
            hp = max_hp 

    #Receive damage
    def damage(self, amount, ultime):
        if (self.hp - amount <= 0) :
            self.game.test_score()
            #if the player has no more life points
            self.game.game_over()
            ultime.percent = 0

        else:
            self.hp -= amount
            
            

    # ---- Movements ---- #
    def move_right(self):
        self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity
    
    def move_down(self):
        self.rect.y += self.velocity

    def move_up(self):
        self.rect.y -= self.velocity

    #Upgrade the spaceship with new assets
    def upgrade_ship(self):
        if self.upgrade == 1:
            super().__init__(False,'spaceship1_', (200, 150))
        if self.upgrade == 2:
            # self.image = pygame.image.load('PygameAssets/spaceship2_.png')
            super().__init__(False,'spaceship2_', (200, 150))
        elif self.upgrade == 3:
            # self.image = pygame.image.load('PygameAssets/spaceship3_.png')
            super().__init__(False,'spaceship3_', (200, 150))
        elif self.upgrade == 4:
            self.velocity +=5
            # self.image = pygame.image.load('PygameAssets/spaceship4_.png')
            super().__init__(False,'spaceship4_', (200, 150))
        elif self.upgrade == 5:
            # self.image = pygame.image.load('PygameAssets/spaceship5_.png')
            super().__init__(False,'spaceship5_', (200, 150))
        elif self.upgrade == 6:
            self.velocity +=5
            # self.image = pygame.image.load('PygameAssets/spaceship6_.png')
            super().__init__(False,'spaceship6_', (200, 150))
        self.attack = self.attack + 2*self.upgrade
        self.image = pygame.transform.scale(self.image, (200, 150))