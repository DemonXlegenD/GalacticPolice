import pygame
import pygame_widgets
import sys
#import the class Game from the file game.py
from game import Game
#import everything from the file music.py
from music import *
#import everything from the file screen.py
from screen import *




#définir une clock
clock = pygame.time.Clock()
fps_game = 100

#Initialize Pygame
pygame.init()

#Creation of the game variable
game = Game()

musique_8()
#Game loop
running = True

while running:

    # draw a scrolling background and give it a different speed depending on the game screen
    if game.is_playing and not game.is_paused:
        #Scroll background with a speed of 5
        game.screen.scrolling(5)
    elif game.is_playing and game.is_paused:
        #Scroll background with a speed of 0 when the game is paused
        game.screen.scrolling(0)
        
    else:
        #Scroll background with a speed of 2
        game.screen.scrolling(2)
    
#  ------------------------------------------- Game Related -------------------------------------------  #
    
    #--------- Play, Pause, Game Over Screens --------#
    
    #The user is playing to the game
    if (game.is_playing and not game.is_paused):
        #Update the game with each turn of the loop
        game.update() 
    #The user pauses the game  
    elif(game.is_playing and game.is_paused):
        game.show_pause()

    #The game is over
    elif((not game.is_playing) and game.is_gameover):

        #Show a Game Over image that goes from top to bottom
        game.screen.end_screen()

        #When the image is out of the screen, displays the screen where the player must enter a nickname 
        if(game.screen.gameover_rect.y > game.screen.height + 300):
            game.is_gameover = False
            game.load_score.check_update()
            game.screen.gameover_rect.y = -700

    #Display the screen where the player must enter a nickname 
    elif((not game.is_playing) and (not game.is_gameover) and game.name_needed):
        game.entername(game.screen.screen)    

    #--------- Settings screen --------#

    elif((not game.is_playing) and game.are_buttons_settings_shown()):

        #Display the three buttons
        game.to_show_settings()

        #Display the slider to change the fps
        if(game.buttons_settings[2].is_shown):
            game.screen.slider_fps_visible = True
            game.screen.slider_volume_visible = False
            game.show_gameplay()
        
        #Display the slider to change the volume of the musics
        elif(game.buttons_settings[4].is_shown):
            game.screen.slider_fps_visible = False
            game.screen.slider_volume_visible = True
            game.show_audio()
        
        #Display the commands
        elif(game.buttons_settings[6].is_shown):
            game.screen.slider_fps_visible = False
            game.screen.slider_volume_visible = False
            game.show_controls()
        
    #--------- Levels screen --------#

    #Show the screen with the planetes and the space which correspond to different levels
    elif(not game.is_playing and game.are_buttons_planete_shown()):
        game.show_planetes()

    #--------- Difficulties screen --------#

    #Show the screen with the difficulties
    elif(not game.is_playing and game.are_buttons_difficulty_shown()):
        game.show_game_modes()
       
    #--------- Credits screen --------#
    elif(not game.is_playing and game.start_vid):
        #Show the credits
        
        game.show_credits()
        game.credits()

        if(game.vid.val == "eof"):
            game.start_vid = False
            game.vid.close()
           
    #--------- Main menu screen --------#
    else:
        #Reset everything
        game.screen.change_bg(f"PygameAssets/space/bgspace.jpg")
        game.show_menu()
        game.name_needed = False
        game.inputbox.clear()
        game.load_score.updated = False
        game.screen.show_screen()
        
        #Display the scores
        for i in range(0,6):
            game.screen.screen.blit(game.load_score.draw_score(i), game.load_score.score_rect)
    
    #--------- Display buttons --------#

    #All the buttons are shown only if the variable is_shown is True
    game.show_buttons()

    
    #Draw the Screen
    pygame.display.flip()

    #--------- Loop Events --------#

    for event in pygame.event.get():
        #The cross at the top of the screen or Alt + F4 is pressed
        if event.type == pygame.QUIT:
            pygame.quit()
            print("Closing the game")
            sys.exit()

        
        #A key is pressed
        if event.type == pygame.KEYDOWN:
            if game.is_playing:
                game.pressed[event.key] = True

                #Detect if the space key is pressed to launch our projectile
                if event.key == game.game_controls.fire:
                    game.player.launch_projectile()
                #Detect if the ctrl key is pressed to launch our ult
                if event.key == game.game_controls.ult:
                    game.player.ultimate(game.ult_event)
                #Detect if the alt key is pressed to launch bomb
                if event.key == game.game_controls.smart_bomb:
                    game.player.smart_bomb()

                #Detect if the escape key is pressed in the game to pause or resume the game
                if event.key == game.game_controls.escape:
                    game.is_paused = not game.is_paused
                    if(not game.is_paused):
                        game.start()

            #Detect if the escape key is pressed to come back
            if event.key == game.game_controls.escape and game.button_back.is_shown:
                game.screen.change_bg(f"PygameAssets/space/bgspace.jpg")
                if(game.are_buttons_difficulty_shown()):
                    game.show_planetes()
                elif(game.are_buttons_planete_shown() or game.are_buttons_settings_shown()):
                    game.show_menu()
            if event.key == game.game_controls.escape and game.start_vid:
                # Si on appuie sur echape pendant la lecture de la vidéo, on revient au menu principal
                game.vid.close()
                game.start_vid = False
                

        #A key is released
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
            
        #A mouse button is pressed
        elif (event.type == pygame.MOUSEBUTTONDOWN):

            #Detect if the button QUIT is pressed to close the game
            if (game.button_quit.button_rect.collidepoint(event.pos) and game.button_quit.is_shown):
                pygame.quit()
                print("Closing the game")
                sys.exit()
            
            #Detect if the button PLAY is pressed to display the levels
            elif (game.button_play.button_rect.collidepoint(event.pos) and game.button_play.is_shown):
                game.show_planetes()

            #Detect if the button SETTINGS is pressed to display the settings
            elif(game.buttons_settings[0].button_rect.collidepoint(event.pos) and game.buttons_settings[0].is_shown):
                game.to_show_settings()

            #Detect if the button RETURN is pressed to come back
            elif(game.button_back.button_rect.collidepoint(event.pos) and game.button_back.is_shown):
                musique_8()
                game.screen.change_bg(f"PygameAssets/space/bgspace.jpg")
                if(game.are_buttons_difficulty_shown()):
                    game.show_planetes()
                elif(game.are_buttons_planete_shown() or game.are_buttons_settings_shown()):
                    game.show_menu()
                elif(game.start_vid):
                    game.vid.close()
                    game.show_menu()
                    game.start_vid = False

            #Detect if the button MENU is pressed to display the main menu screen
            elif(game.button_menu.button_rect.collidepoint(event.pos) and game.button_menu.is_shown):
                #Reset the game  
                game.game_reset()
                game.show_menu()
                game.screen.change_bg(f"PygameAssets/space/bgspace.jpg")
                game.is_paused = False

            #Display the video if the button credits is used and is shown
            elif(game.button_credits.button_rect.collidepoint(event.pos) and game.button_credits.is_shown):
                game.vid.restart()
                game.start_vid = True

            #Display the levels if they have to be shown
            elif (game.are_buttons_planete_shown()):
                i = 0
                #Detect if the space level is pressed 
                if(game.button_space.button_rect.collidepoint(event.pos)):
                    musique_1()
                    game.screen.change_bg(f"PygameAssets/space/bgspace.jpg")
                    game.show_game_modes() 

                #Detect if a planete is pressed 
                for planete in game.buttons_planetes:   

                    if (planete.button_rect.collidepoint(event.pos) and game.are_buttons_planete_shown()):
                                   
                        #Functions for the different musics
                        globals()[f"planete_{i}"]()
                        game.screen.change_bg(f"PygameAssets/space/planetes/planete{i}map.png")
                        game.show_game_modes()
                        game.planete = i+1
                    i += 1
            #Check if the settings are shown
            elif(game.are_buttons_settings_shown()):
                for i in range(1,6,2):

                    #Detect if a button from settings is pressed to display the settings related to it
                    if(game.buttons_settings[i].button_rect.collidepoint(event.pos) and game.buttons_settings[i].is_shown):
                        game.reset_show_settings()
                        game.buttons_settings[i+1].is_shown = True

            #Check if the difficulties are shown
            elif(game.are_buttons_difficulty_shown()):

                for i in range(0,4):

                    #Detect if a button from difficulties is pressed to start the game harder or easier for the player
                    if (game.buttons_difficulties[i].button_rect.collidepoint(event.pos) and game.buttons_difficulties[i].is_shown):
                        game.create_player(i+1)
                        game.start() 
                 
           

        #Detect if the volume slider is modified to change the volume
        if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION) and game.screen.slider_volume_visible:
            game.screen.slider_volume.listen(event)
            pygame_widgets.update([game.screen.slider_volume])
            volume_choisi = game.screen.slider_volume.getValue() / 100
            game.screen.text_volume.setText(game.screen.slider_volume.getValue()) 
            volume(volume_choisi)
        #Detect if the fps slider is modified to change the fps
        if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION) and game.screen.slider_fps_visible:
            game.screen.slider_fps.listen(event)
            pygame_widgets.update([game.screen.slider_fps])
            fps_choisi = game.screen.slider_fps.getValue()
            game.screen.text_fps.setText(game.screen.slider_fps.getValue()+60)
            fps_game = fps_choisi + 60
            
    #fix the number of fps on the clock
    
    clock.tick_busy_loop(fps_game)  
