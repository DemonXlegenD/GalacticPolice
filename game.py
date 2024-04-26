import pygame
import time
import random
from screen import Screen
from spaceship import Spaceship
from controle import Controls
from enemy import Asteroid, Spaceship1, Spaceship2, RedBird, Helicopter, Bomber
from button import Button
from ult_event import UltimateCharging
from score import Score
from inputbox import InputBox
from pyvidplayer import Video

#créer une classe qui va représenter notre jeu
class Game:

    def __init__(self):

        
        self.screen = Screen(1920, 1080)
        self.which_screen = 0

        #set whether or not our game has started or is paused
        self.is_playing = False
        self.is_gameover = False
        self.is_paused = False
        self.difficulty = 1
        self.planete = 0
        #input player
        self.inputbox = InputBox(100, self.screen.height/2, self.screen.width/2, self.screen.height/10)
        self.name_needed = False
        #generate the ultimate event
        self.ult_event = UltimateCharging(self.difficulty)
        
        #generate our player
        self.number_players = 1
        self.all_players = pygame.sprite.Group()
        self.player = Spaceship(self, 200,5,15, self.planete)
        self.all_players.add(self.player)

        #set the score to 0
        self.score = 0
        self.font = pygame.font.Font("Roboto/Roboto-Bold.ttf", 25)
        self.level = 0
        self.load_score = Score()
        self.game_controls = Controls()

        #Event keybord
        self.pressed = {}

        #Credits
        self.vid = Video("credits.mp4")
        self.start_vid = False
        self.vid.set_size((self.screen.width, self.screen.height))

        #=====================================================================================================================#
        #-------------------------------------------------------PLAY----------------------------------------------------------#
        #=====================================================================================================================# 
        
        self.button_play = Button(self.screen, 2, 1.60, 450, 200,'PygameAssets/button/button-play.png')

        #=====================================================================================================================#
        #-------------------------------------------------------QUIT----------------------------------------------------------#
        #=====================================================================================================================# 
        
        self.button_quit = Button(self.screen, 2, 1.10, 450, 200,'PygameAssets/button/button-quit.png')

        #=====================================================================================================================#
        #-------------------------------------------------------MENU----------------------------------------------------------#
        #=====================================================================================================================# 
        
        self.button_menu = Button(self.screen, 2, 2, 450, 200,'PygameAssets/button/button-menu.png')

        #=====================================================================================================================#
        #------------------------------------------------------PLANETES-------------------------------------------------------#
        #=====================================================================================================================#

        self.buttons_planetes = [
            Button(self.screen, 1.25, 1.80, 300, 300,'PygameAssets/space/planetes/terre.png'), 
            Button(self.screen, 1.80, 1.10 , 200, 200,'PygameAssets/space/planetes/planete1.png'), 
            Button(self.screen, 1.60, 8, 250, 250,'PygameAssets/space/planetes/planete2.png'),
            Button(self.screen, 1.90, 2, 200, 200,'PygameAssets/space/planetes/planete3.png'),
            Button(self.screen, 8, 1.10, 450, 300,'PygameAssets/space/planetes/planete4.png'),
            Button(self.screen, 1.10, 7.5, 175, 175,'PygameAssets/space/planetes/planete5.png'),
            Button(self.screen, 1.10, 1.15, 150, 150,'PygameAssets/space/planetes/planete6.png')
            ]

        self.button_space = Button(self.screen, 15, 4, 700, 500,'PygameAssets/space/champdemeteorite.png')
        
        #=====================================================================================================================#
        #------------------------------------------------------SETTINGS-------------------------------------------------------#
        #=====================================================================================================================#

        self.buttons_settings = [
            Button(self.screen, 100, 100, 50, 50,'PygameAssets/button/button-settings.png'),
            Button(self.screen, 10.15, 4, 200, 150,'PygameAssets/button/Gameplay.png'),
            Button(self.screen, 10.15, 4, 200, 150,'PygameAssets/button/Gameplay_underline.png'),
            Button(self.screen, 2.25, 4, 200, 150,'PygameAssets/button/audio.png'),
            Button(self.screen, 2.25, 4, 200, 150,'PygameAssets/button/audio_underline.png'),
            Button(self.screen, 1.3, 4, 200, 150,'PygameAssets/button/controle.png'),
            Button(self.screen, 1.3, 4, 200, 150,'PygameAssets/button/controle_underline.png')
    
        ]

        #=====================================================================================================================#
        #---------------------------------------------------DIFFICULTIES------------------------------------------------------#
        #=====================================================================================================================#

        self.buttons_difficulties = [
            Button(self.screen, 2, 7, 500, 150,'PygameAssets/button/easy-button.png'),
            Button(self.screen, 2, 3, 500, 150,'PygameAssets/button/medium-button.png'),
            Button(self.screen, 2, 1.90, 500, 150,'PygameAssets/button/hard-button.png'),
            Button(self.screen, 2, 1.40, 500, 150,'PygameAssets/button/nightmare-button.png')
        ]

        #=====================================================================================================================#
        #--------------------------------------------------------BACK---------------------------------------------------------#
        #=====================================================================================================================#
        
        self.button_back =  Button(self.screen, 100, 100, 100, 100,'PygameAssets/button/retour.png')

        self.button_credits = Button(self.screen, 1.05, 1.05, 300, 100,'PygameAssets/button/credits.png')
        #group of enemies
        self.all_enemy = pygame.sprite.Group()       
        self.all_explo = pygame.sprite.Group()   
    
    #Show credits

    def show_credits(self):
        self.button_play.is_shown = False
        self.button_quit.is_shown = False
        self.button_credits.is_shown = False
        self.button_menu.is_shown = False
        self.buttons_settings[0].is_shown = False
        self.button_space.is_shown = False
        self.button_back.is_shown = True
        for settings in self.buttons_settings[1:]:
            settings.is_shown = False
        for planete in self.buttons_planetes:
            planete.is_shown = False
        for difficulty in self.buttons_difficulties:
            difficulty.is_shown = False

    def credits(self):
        self.vid.draw(self.screen.screen, (0, 0))
        

    #Show scores
    def test_score(self):
        self.load_score.new_score = self.score
        self.load_score.check_update()
        if self.load_score.name_needed:
            self.name_needed = True

    #Ask to enter a name
    def entername(self, screen):
        if not self.inputbox.fait:
            for event in pygame.event.get():
                self.inputbox.handle_event(event)
            self.inputbox.update()
            self.inputbox.draw(screen)
            pygame.display.flip()
        else:
            self.load_score.name = self.inputbox.text
            self.name_needed = False
            self.load_score.update_score()

    #Create a new player
    def create_player(self, difficulty):
        #generate our player
        self.difficulty = difficulty
        self.all_players = pygame.sprite.Group()
        self.player = Spaceship(self, 200, 10, 30, self.planete)
        self.all_players.add(self.player)

    #Show the settings
    def reset_show_settings(self):
        for settings in self.buttons_settings[1:]:
            settings.is_shown = False
        for settings in self.buttons_settings[1::2]:
            settings.is_shown = True

    #Show the main menu and nothing else
    def show_menu(self):
        self.button_play.is_shown = True
        self.button_quit.is_shown = True
        self.button_credits.is_shown = True
        self.button_menu.is_shown = False
        self.buttons_settings[0].is_shown = True
        self.button_space.is_shown = False
        self.button_back.is_shown = False
        for settings in self.buttons_settings[1:]:
            settings.is_shown = False
        for planete in self.buttons_planetes:
            planete.is_shown = False
        for difficulty in self.buttons_difficulties:
            difficulty.is_shown = False

    
    #Show the  menu pause and nothing else
    def show_pause(self):
        self.button_play.is_shown = False
        self.button_quit.is_shown = True
        self.button_credits.is_shown = False
        self.button_menu.is_shown = True
        self.buttons_settings[0].is_shown = True
        self.button_space.is_shown = False
        self.button_back.is_shown = False
        for settings in self.buttons_settings[1:]:
            settings.is_shown = False
        for planete in self.buttons_planetes:
            planete.is_shown = False
        for difficulty in self.buttons_difficulties:
            difficulty.is_shown = False


    #Show the planetes and nothing else
    def show_planetes(self):
        self.button_play.is_shown = False
        self.button_quit.is_shown = False
        self.button_credits.is_shown = False
        self.button_menu.is_shown = False
        self.button_back.is_shown = True
        self.button_space.is_shown = True
        for settings in self.buttons_settings:
            settings.is_shown = False
        for planete in self.buttons_planetes:
            planete.is_shown = True
        for difficulty in self.buttons_difficulties:
            difficulty.is_shown = False

    #Show the game modes and nothing else
    def show_game_modes(self):
        self.button_play.is_shown = False
        self.button_quit.is_shown = False
        self.button_credits.is_shown = False
        self.button_menu.is_shown = False
        self.button_back.is_shown = True
        self.button_space.is_shown = False
        for settings in self.buttons_settings:
            settings.is_shown = False
        for planete in self.buttons_planetes:
            planete.is_shown = False
        for difficulty in self.buttons_difficulties:
            difficulty.is_shown = True

    #Show the settings and nothing else
    def to_show_settings(self):
        self.button_play.is_shown = False
        self.button_quit.is_shown = False
        self.button_credits.is_shown = False
        self.button_menu.is_shown = False
        self.buttons_settings[0].is_shown = False
        self.button_space.is_shown = False
        for settings in self.buttons_settings[1::2]:
            settings.is_shown = True
        for planete in self.buttons_planetes:
            planete.is_shown = False
        for difficulty in self.buttons_difficulties:
            difficulty.is_shown = False
        self.button_back.is_shown = True

    #Settings Gameplay
    def show_gameplay(self):
        self.screen.slider_fps.draw()
        self.screen.text_fps.draw()
        self.screen.screen.blit(self.screen.fps, (320, 450))
        
    #Settings Audio
    def show_audio(self):  
        self.screen.slider_volume.draw()
        self.screen.text_volume.draw()
        self.screen.screen.blit(self.screen.volume, (320, 450))
        
    #Settings controls
    def show_controls(self):
        self.game_controls.show_keys(self.screen.screen)
        
    #Show the buttons
    def show_buttons(self):

        self.button_play.show_button()
        self.button_quit.show_button()
        self.button_credits.show_button()
        self.button_back.show_button()
        self.button_menu.show_button()
        self.button_space.show_button()
        for settings in self.buttons_settings:
            settings.show_button()
        for planete in self.buttons_planetes:
            planete.show_button()
        for difficulty in self.buttons_difficulties:
            difficulty.show_button()

    #The planetes are shown
    def are_buttons_planete_shown(self):
        shown = True
        for button in self.buttons_planetes:
            if(not button.is_shown):
                shown = button.is_shown

        return shown
    
    #The settings are shown
    def are_buttons_settings_shown(self):
        shown = False
        for button in self.buttons_settings[1:]:
            if(button.is_shown):
                shown = button.is_shown
        return shown

    #The difficulties are shown
    def are_buttons_difficulty_shown(self):
        shown = True
        for button in self.buttons_difficulties:
            if(not button.is_shown):
                shown = button.is_shown

        return shown
            
    #Start the game
    def start(self):
        self.is_playing = True
        self.button_play.is_shown = False
        self.button_quit.is_shown = False
        self.button_menu.is_shown = False
        self.button_back.is_shown = False
        for settings in self.buttons_settings:
            settings.is_shown = False
        for planete in self.buttons_planetes:
            planete.is_shown = False
        for difficulty in self.buttons_difficulties:
            difficulty.is_shown = False

    #Reset the game 
    def game_reset(self):
        self.all_enemy = pygame.sprite.Group()
        self.player.hp = self.player.max_hp
        self.screen.scrolling(0)
        self.score = 0
        self.pressed = {}
        self.is_playing = False

    #The game is over
    def game_over(self):
        #reset game, remove enemies, reset players to 100 life, game hold
        self.game_reset()
        self.is_gameover = True

    #Add score to the player
    def add_score(self, points = 10):
        self.score += points

    #Update the game
    def update(self):

        #show score on screen
        score_text = self.font.render(f"Score : {self.score}", 1, (255, 255, 255))
        self.screen.screen.blit(score_text, (20, 20))

        #apply our player image
        self.screen.screen.blit(self.player.image, self.player.rect)
        
        #show life bar
        self.player.update_health_bar(self.screen.screen)

        #Shooting Animation
        if self.player.first_frame:
            self.player.update_animation()
        if self.player.wait_anim + 0.04 <= time.time():
            self.player.update_animation()
            self.player.wait_anim = time.time()
        

        # Spawn enemy
        if time.time() > self.screen.seconde + 3:
            
            self.spawn_enemy(self.screen.screen)
            self.screen.seconde = time.time()


           #  ------------------------------------------- Projectiles -------------------------------------------
        #recover the projectiles
        for projectile in self.player.all_projectile:
            projectile.move(self.ult_event)

        #apply all the images from my projectile group
        self.player.all_projectile.draw(self.screen.screen)

        #collect projectiles from enemies
        for enemy in self.all_enemy:
            for projectile in enemy.all_projectile:
                if(enemy.name == "bomber_"):
                    projectile.fall(self.ult_event)
                else:
                    projectile.move(self.ult_event)
                

        #apply all the images from my projectile group
        for enemy in self.all_enemy:
            enemy.all_projectile.draw(self.screen.screen)
            enemy.update_animation()

        #  ------------------------------------------- Enemy -------------------------------------------
        #recover the enemies
        for enemy in self.all_enemy:
            enemy.forward(self.ult_event)
            enemy.update_health_bar(self.screen.screen) 
            if enemy.animation_loop:
                enemy.update_animation()
                
            else:
                #Shooting Animation
                try:
                    if enemy.first_frame:
                        enemy.update_animation()
                    if enemy.wait_anim + 0.04 <= time.time():
                        enemy.update_animation()
                        enemy.wait_anim = time.time()
                except:
                    None

        #apply all the images of my enemy group
        self.all_enemy.draw(self.screen.screen)


         #  ------------------------------------------- Explosion -------------------------------------------
        #collect explosions
        for explosion in self.all_explo:
            if explosion.first:
                explosion.update_animation()
            #Waiting time between each frame
            if explosion.wait_anim + 0.06 <= time.time():
                explosion.update_animation()
                if explosion.remove_time + 0.5 <= time.time():
                    explosion.remove()
                explosion.wait_anim = time.time()

        #apply all the images from my explosion group
        self.all_explo.draw(self.screen.screen)

        #  ------------------------------------------- Smart bomb -------------------------------------------
        for smart in self.player.all_smart_bomb:
            smart.growing(8)

        self.player.all_smart_bomb.draw(self.screen.screen)

        #  ------------------------------------------- powerUp -------------------------------------------
        #recover the enemies
        for powerUp in self.player.all_upgrades:
            powerUp.forward()
        self.player.all_upgrades.draw(self.screen.screen)

        #  ------------------------------------------- Ultime -------------------------------------------
        #refresh game event bar
        self.ult_event.update_bar(self.screen.screen, self.player)

        #check if the player wants to go left or right
        if (self.pressed.get(self.game_controls.right) or self.pressed.get(pygame.K_d)) and self.player.rect.x + self.player.rect.width<=  self.screen.screen.get_width():
            self.player.move_right()
        if (self.pressed.get(self.game_controls.left) or self.pressed.get(pygame.K_q)) and self.player.rect.x >= 0 :
            self.player.move_left()
        if (self.pressed.get(self.game_controls.down) or self.pressed.get(pygame.K_s)) and self.player.rect.y + self.player.rect.height<=  self.screen.screen.get_height()-50:
            self.player.move_down()
        if (self.pressed.get(self.game_controls.up) or self.pressed.get(pygame.K_z)) and self.player.rect.y >= 0 :
            self.player.move_up()


    #Check collision
    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    #Spawn enemy
    def spawn_enemy(self, screen):
        enemy_number = random.randint(1, 2)

        for i in range(0, enemy_number):

            enemy_spawn = random.randint(0,2)
            
            "We didn't finish the levels so we just made 2 of them playable, the others are playable but get the same enemies than the space ones"
            # if(self.planete == 0):
            #     if enemy_spawn == 0:
            #         # Ennemi de collision
            #         enemy = Asteroid(self, self.difficulty, enemy_spawn, (200,184), screen)
            #     elif enemy_spawn == 1:
            #         # Ennemi one shot
            #         # Ennemi missiles
            #         enemy = Spaceship1(self, self.difficulty, enemy_spawn, (200,75), screen)
            #     elif enemy_spawn == 2:
            #         #enemmi wave missiles
            #         enemy = Spaceship2(self, self.difficulty, enemy_spawn, (200,75), screen)
            if(self.planete == 1):
                if enemy_spawn == 0:
                    #Collision enemy
                    enemy = RedBird(self, self.difficulty, enemy_spawn, (120,120), screen)

                elif enemy_spawn == 1:
                    # Enemy one shot
                    # Enemy missile
                    enemy = Helicopter(self, self.difficulty, enemy_spawn, (200,75), screen)
                elif enemy_spawn == 2:
                    #enemy wave missiles
                    # enemy = Spaceship2(self, self.difficulty, enemy_spawn, (200,75), screen)
                    enemy = Bomber(self, self.difficulty, 0, (200,120), screen)
            else:
                if enemy_spawn == 0:
                    #Collision enemy
                    enemy = Asteroid(self, self.difficulty, enemy_spawn, (200,184), screen)
                elif enemy_spawn == 1:
                    # Enemy one shot
                    # Enemy missile
                    enemy = Spaceship1(self, self.difficulty, enemy_spawn, (200,75), screen)
                elif enemy_spawn == 2:
                    #enemmi wave missiles
                    enemy = Spaceship2(self, self.difficulty, enemy_spawn, (200,75), screen)

            enemy.planete = self.planete
            self.all_enemy.add(enemy)


        

        