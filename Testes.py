# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 17:06:44 2015

@author: gabrielantao
"""

import sys
import pygame
from pygame.locals import *
pygame.init()
from Classes import *


mainClock = pygame.time.Clock()

# cria janela
window = pygame.display.set_mode((800,600))
pygame.display.set_caption("Modulo de testes")


win = Window(window, 100,100,400,400)
label_2 = Label("texto.com", 60, 90, style="style1")
##label_1.mouse_abled = False
label_1 = Label("Meu Texto", -10, -5, style="style2")
win.add(label_1, label_2)
##win.add(label_1)


while True:
    mainClock.tick(30)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    window.fill((255,255,255))

##    label_2.text = pygame.mouse.get_pos()

    win.update()
    win.draw()


    pygame.display.update()
