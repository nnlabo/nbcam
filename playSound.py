# coding: UTF-8

import pygame.mixer
import time

#Play Okaerinasai Sound
pygame.mixer.init(frequency = 44100) 
pygame.mixer.music.load("okaerinasai.wav") 
#pygame.mixer.music.load("keikoku.mp3") 
pygame.mixer.music.play(1)
time.sleep(3)
pygame.mixer.music.stop()