import pygame
from pygame import mixer

#initialize the mixer
pygame.init()
pygame.mixer.init()

#One function for one music
def musique_1():
        mixer.music.load('musique/background.mp3')
        mixer.music.play(-1)
def planete_0():
        mixer.music.load("musique/planete0.mp3")
        mixer.music.play(-1)
def planete_1():
        mixer.music.load("musique/planete1.mp3")
        mixer.music.play(-1)
def planete_2():
        mixer.music.load("musique/planete2.mp3")
        mixer.music.play(-1)
def planete_3():
        mixer.music.load("musique/planete3.mp3")
        mixer.music.play(-1)
def planete_4():
        mixer.music.load("musique/planete4.mp3")
        mixer.music.play(-1)
def planete_5():
        mixer.music.load("musique/planete5.mp3")
        mixer.music.play(-1)
def planete_6():
        mixer.music.load("musique/planete6.mp3")
        mixer.music.play(-1)
def musique_8():
        mixer.music.load('musique/musique_menu.mp3')
        mixer.music.play(-1)

#Change the volume
def volume(volume):
        mixer.music.set_volume(volume)