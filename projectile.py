import pygame

#definir la classe qui va gerer les projectiles

class Projectile(pygame.sprite.Sprite):

    def __init__(self, player, enemy, who, level, planete, speed = 15, fall = False):
        super().__init__()
        self.target = who #who is launching ? 1 = enemy / 0 = player
        self.level = level #level of the upgrade, 0 = enemy
        self.planete = planete
        self.speed = speed
        self.player = player 
        self.enemy = enemy #kind of the enemy
        self.is_falling = fall
        try:
            if self.enemy.type == 2:
                self.damage = 12
            else:
                self.damage = 15
        except:
            self.damage = 15

        # Sprites
        if self.target == 0:
            if self.level == 1:
                self.image = pygame.image.load('PygameAssets/little_purple_beam.png')
            elif self.level == 2:
                self.image = pygame.image.load('PygameAssets/purple_beam.png')
            elif self.level == 3:
                self.image = pygame.image.load('PygameAssets/blue_beam.png')
            elif self.level == 4:
                self.image = pygame.image.load('PygameAssets/cyan_beam.png')
            elif self.level == 5:
                self.image = pygame.image.load('PygameAssets/cyan_ball2.png')
            elif self.level >= 6:
                self.image = pygame.image.load('PygameAssets/cyan_ball1.png')
            self.rect = self.image.get_rect()
            self.rect.x = player.rect.x + 150
            self.rect.y = player.rect.y + 85
        elif self.target == 1:
            if(self.planete == 0):
                self.image = pygame.image.load('PygameAssets/red_beam.png')
            elif(self.planete == 1):
                self.image = pygame.image.load('PygameAssets/Missile-Transparent.png')
            self.rect = self.image.get_rect()
            self.rect.x = enemy.rect.x - 30
            self.rect.y = enemy.rect.y + 30

    #Remove all the projectile from the player or the enemy
    def remove(self):
        if self.target == 0:
            self.player.all_projectile.remove(self)
        if self.target == 1:
            self.enemy.all_projectile.remove(self)

    #The projectile is moving
    def move(self, ultime) : 
        if self.target == 0:
            self.rect.x += self.speed
        if self.target == 1:
            self.rect.x -= self.speed

        if self.target == 0:
            #Check collision with the enemies
            for enemy in self.player.game.check_collision(self, self.player.game.all_enemy):
                if enemy.spawned == True or (enemy.rect.x < 1900 and enemy.type == 0):
                    self.remove()
                    #Apply the damage to the enemy
                    enemy.damage(self.player.attack, ultime)

                #Check collision
                for proj in self.player.game.check_collision(self, enemy.all_projectile):
                    self.remove()
                    proj.remove()

            #Detect if the projectile is out of the screen
            if self.rect.x > 1920:
                self.remove()

        elif self.target == 1:
            #Check the collision with the player
            if self.player.game.check_collision(self, self.player.game.all_players):
                self.remove()
                #Apply the damage to the player
                self.player.damage(self.damage, ultime)

            #Check collision with others projectiles
            for proj in self.player.game.check_collision(self, self.player.all_projectile):
                self.remove()
                proj.remove()

            #Check if it is out of the screen
            if self.rect.x < -200:
                self.remove()

                
        

class Bomb(Projectile):
    def __init__(self, player, enemy, who, level, planete, speed):
        super().__init__(player, enemy, who, level, planete, speed, True)
        self.speed_x = int(speed/4)
        self.speed_y = speed
        self.image = pygame.image.load('PygameAssets/bomb_.png')
        self.image = pygame.transform.scale(self.image, (40, 50))
        self.rect = self.image.get_rect()
        self.rect.x = enemy.rect.x
        self.rect.y = enemy.rect.y

    def fall(self, ultime):
        self.rect.x -= self.speed_x
        self.rect.y += self.speed_y

        if self.target == 1:
            #Check the collision with the player
            if self.player.game.check_collision(self, self.player.game.all_players):
                self.remove()
                #Apply the damage to the player
                self.player.damage(self.damage, ultime)

            #Check collision with others projectiles
            for proj in self.player.game.check_collision(self, self.player.all_projectile):
                self.remove()
                proj.remove()

        if self.rect.y >= 1070 and self.enemy.name == "bomber_":
            self.remove()
        
    