import pygame
import random
import time
import animation
from projectile import Projectile, Bomb
from powerup import PowerUp 
from particles import Explosion

GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

#Classe des ennemis
class Enemy(animation.AnimateSprite):

    def __init__(self, game, difficulty, animation_loop, name, size, surface):
        super().__init__(animation_loop, name, size)
        #Settings
        self.game = game
        self.name = name
        self.size = size
        self.planete = 0
        self.difficulty = difficulty
        self.hp = 100 * self.difficulty
        self.max_hp = 100 * self.difficulty
        self.speed = 0
        
        self.spawned = False
        self.all_projectile = pygame.sprite.Group()

        #Projectiles
        self.projectileHit = 0
        self.destroy = time.time()
        self.point = 10

        #Image
        self.rect = self.image.get_rect()
        self.rect.x = 2300
        self.rect.y = random.randint(10, surface.get_height()-250)
        if(self.name == "bomber_"):
            self.rect.y = 30

        #Other settings
        self.launch = time.time()
        self.wait = time.time()
        self.nbr_max = 3
        self.nbr_actuel = 0
        self.gone_where = random.randint(-5, 5)

        # Animation
        self.first_frame = True
        self.wait_anim = time.time()
        self.animation_loop = animation_loop

    #Define the speed of the enemy
    def set_speed(self, speed):
        self.speed = speed * self.difficulty

    #Set the amount of point that it gives when he is killed
    def set_point(self, point):
        self.point = point 

    #Update the animations
    def update_animation(self):
        self.animate()
        self.first_frame = False


    def update_health_bar(self, surface):

       #Set life gauge color
        if(self.hp > (self.max_hp-(self.max_hp*25/100))):
            bar_color = GREEN #Green color

        elif(self.hp > (self.max_hp-(self.max_hp*75/100)) and self.hp <= self.max_hp-(self.max_hp*25)/100):
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
        

    def remove(self, drop, explode):

        #Does powerup drop or not + determination of which
        if drop:
            powerup_ornot = random.randint(0, int((2*self.difficulty)))
            if powerup_ornot == 0 or (powerup_ornot == 4 and self.difficulty == 4): 
                # All bonuses can be dropped
                powerups = [(0, True), (1, True), (2, True)]
                # heal =  0
                # upgrade = 1
                # score = 2

                #Powerup heal disabled
                if self.game.player.hp == self.game.player.max_hp:
                    powerups[0] = (0, False)

                #Powerup upgrade disabled -> the higher the upgrade, the harder it is to get new upgrade bonuses
                if self.game.player.upgrade == 6:
                    powerups[1] = (1, False)
                elif not self.game.player.upgrade == 1:
                    if random.randint(1,self.game.player.upgrade) == 1:
                        powerups[1] = (1, False)

                #Filter powerups to remove those that are False
                available_powerups = list(filter(lambda x: x[1], powerups))
                    #lambda allows to check the second element of each tuple in powerups

                #Randomly select a power up among those that are True
                if available_powerups:
                    selected_powerup = random.randint(0, len(available_powerups)-1)
                    powerup_value = available_powerups[selected_powerup][0]
                    self.spawnPowerup(powerup_value)

        if explode:
            if self.type == 0:
                self.game.all_explo.add(Explosion(self.rect.x, self.rect.y, self.game, True, (300,300)))
            else:
                self.game.all_explo.add(Explosion(self.rect.x, self.rect.y, self.game, False, (200,200)))
            self.game.player.killed += 1
        print(self.game.player.killed)
        self.game.all_enemy.remove(self)

    #Spwan the power up
    def spawnPowerup(self, type):
        self.game.player.all_upgrades.add(PowerUp(self, type, self.difficulty))


    #Define spawn
    def spawn(self):
        if (self.type == 1 or self.type == 2) and self.rect.x > 1604:
            self.rect.x -= 5
        else:
            self.spawned = True
        if self.type == 0 and self.rect.x < 1900:
            self.spawned = True
        
    #Leave the screen after staying too long
    def gone(self):
        self.rect.x += 10
        self.rect.y -= self.gone_where
        if self.rect.y < -200 or self.rect.x > 2100:
            self.remove(False, False)

    #Take damage
    def damage(self, amount, ultime):
        if (self.hp - amount < amount) :
            self.remove(True, True)
            ultime.percent += 0.5
            self.game.score += self.point
        else:
            self.hp -= amount

    #Launch a projectile
    def launch_projectile(self):
        if(self.name == "bomber_"):
            self.all_projectile.add(Bomb(self.game.player, self, 1, 0, self.planete, 5))
        else:
            self.all_projectile.add(Projectile(self.game.player, self, 1, 0, self.planete))
            self.start_animation()

    #Move
    def forward(self, ultime):

        #Put damage to players if collision and delete the enemy
        if self.game.check_collision(self, self.game.all_players):
            self.remove(False, True)
            self.game.player.damage(self.attack, ultime)
        else:
            self.spawn()
            self.rect.x -= self.speed

        #Make enemies disappear from the screen
        if self.rect.x < -200 and self.name != "bomber_":
            self.remove(False, False)
        elif(self.rect.x < -1000 and self.name == "bomber_"):
            self.remove
        #Make stationary enemies disappear
        if self.destroy + 10 < time.time() and (self.type == 1 or self.type == 2):
            self.gone()

        #Shoot bombs
        if self.type == 0 and self.rect.x < 1900 and self.name == "bomber_":
            if self.launch + 1.5/self.difficulty <= time.time():
                self.launch_projectile()
                self.launch = time.time()

        #Shoot missiles for type 1
        if self.type == 1 and self.rect.x == 1600:
            if self.launch + 2/self.difficulty <= time.time():
                self.launch_projectile()
                self.launch = time.time()

        #Shoot missiles for type 2
        if self.type == 2 and self.rect.x == 1600:
            if self.launch + 3/self.difficulty <= time.time():
                if self.nbr_actuel < self.nbr_max:
                    if self.wait + 0.5 <= time.time():
                        self.launch_projectile()
                        self.nbr_actuel += 1
                        self.wait = time.time()
                if self.nbr_actuel >= self.nbr_max:
                    self.launch = time.time()
                    self.nbr_actuel = 0

#Define a class for the asteroid
class Asteroid(Enemy):

    def __init__(self, game, difficulty, type, size, surface):
        super().__init__(game, difficulty, False, "asteroid", size, surface)
        self.hp = 100 * self.difficulty
        self.max_hp = 100 * self.difficulty
        self.attack = 30 * self.difficulty
        self.point = 10 * self.difficulty
        self.set_speed(1 * self.difficulty) 
        self.type = type


#Define a class for the Spaceship number 1
class Spaceship1(Enemy):

    def __init__(self, game, difficulty, type, size, surface):
        super().__init__(game, difficulty, False,"ship1_", size, surface)
        self.hp = 30 * self.difficulty
        self.max_hp = 30 * self.difficulty
        self.set_speed(0) 
        self.attack = 200 * self.difficulty
        self.set_point(15 * self.difficulty)
        self.type = type

#Define a class for the Spaceship number 2
class Spaceship2(Enemy):

    def __init__(self, game, difficulty, type, size, surface):
        super().__init__(game, difficulty, False, "ship2_", size, surface)
        self.hp = 25 * self.difficulty
        self.max_hp = 25 * self.difficulty
        self.set_speed(0) 
        self.attack = 200 * self.difficulty
        self.set_point( 15 * self.difficulty)
        self.type = type

#Define a class for the Red bird
class RedBird(Enemy):

    def __init__(self, game, difficulty, type, size, surface):
        super().__init__(game, difficulty, True, "red_bird_", size, surface)
        self.hp = 25
        self.max_hp = 25 * self.difficulty
        self.set_speed(1 * self.difficulty)
        self.attack = 15 * self.difficulty
        self.set_point(5 *self.difficulty)
        self.type = type
        self.start_animation()

#Define a class for the Helicopter
class Helicopter(Enemy):

    def __init__(self, game, difficulty, type, size, surface):
        super().__init__(game, difficulty, True, "helicopter_", size, surface)
        self.hp = 30 * self.difficulty
        self.max_hp = 30 * self.difficulty
        self.set_speed(0) 
        self.attack = 200 * self.difficulty
        self.set_point(15 * self.difficulty)
        self.type = type
        self.start_animation()
    

class Bomber(Enemy):

    def __init__(self, game, difficulty, type, size, surface):
        super().__init__(game, difficulty, True, "bomber_", size, surface)
        self.hp = 50 * self.difficulty
        self.max_hp = 50 * self.difficulty
        self.set_speed(2) 
        self.attack = 200 * self.difficulty
        self.set_point(15 * self.difficulty)
        self.type = type
        
    