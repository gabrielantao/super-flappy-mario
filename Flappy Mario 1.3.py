#-------------------------------------------------------------------------------
# Name:        Flappy Mario v1.4
# Purpose:
#
# Author:      Gabriel
#
# Created:     12/07/2014
# Copyright:   (c) Gabriel 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
import random
import csv
import pygame
from pygame.locals import *
pygame.init()

WIDTH = 1000
HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
GND_HEIGHT = 80 # altura do chao
# TODO: alterar quando modular o delta tempo (time-based)
GRAVITY = 1 # valor da gravidade 

# cria o clock
clock = pygame.time.Clock()

# inicializa screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Flappy Mario v1.4")

# carrega imagens e large_font
background = pygame.image.load("images/parallax.png")
ground  = pygame.image.load("images/ground.png")
score_img = pygame.image.load("images/mario_score.png")
game_title = pygame.image.load("images/game_title.png")
start_button = pygame.image.load("images/start_button.png")
mario_hammer = pygame.image.load("images/mario_hammer.png")
crush = pygame.image.load("images/crush.png")
get_ready = pygame.image.load("images/get_ready.png")
score_gameover = pygame.image.load("images/score_game_over.png")
medals = pygame.image.load("images/medals.png")
mario_sprite = pygame.image.load("images/mario_sprite.png")
signature = pygame.image.load("images/signature.png")
pipe_img = pygame.image.load("images/pipe.png")
level_img = pygame.image.load("images/level.png")
cursor_img = pygame.image.load("images/cursor.png")
play_again = pygame.image.load("images/play_again.png")

large_font = pygame.font.Font("fonts/Super_Mario_World.ttf", 32)
small_font = pygame.font.Font("fonts/Super_Mario_World.ttf", 20)

# cria vetores
scroll = -5

class Game:
    """
    1 modo inicial; 
    2 preparacao para o jogo (get ready); 
    3 rodando jogo; 
    4 game over (placar e medalha)
    """
    def __init__(self):
        self.pipe_list = []
        self.game_mode = 1
        self.score = 0    #pontos
        self.best_score = 0 
        self.ground_pos = 0
        self.mario_rect = pygame.Rect(50,200,40,40)  
        self.mario_speed = 0  
        self.level = 0 
        
    # cria dos rects dos tubos
    # obs: modula gaps (vertical e horizontal)
    def create_pipe(self):
        if self.level == 0:
            self.gap_width = 400
            gap_height = 200 
        elif self.level == 1:
            self.gap_width = 300
            gap_height = 140
        elif self.level == 2:
            self.gap_width = random.randrange(250, 401, 50)
            gap_height = 140
        elif self.level == 3:
            self.gap_width = random.randrange(200, 301, 50)
            gap_height = random.randrange(120, 201, 40)
        width = pipe_img.get_width()
        height = random.randrange(0, HEIGHT - gap_height, 20)
        up_pipe = pygame.Rect(WIDTH, 0, width, height)
        down_pipe = pygame.Rect(WIDTH, height + gap_height, width, HEIGHT - height - gap_height - GND_HEIGHT)
        self.pipe_list.append([up_pipe, down_pipe])

    # seleciona velocidade dos tubos
    # obs: modula velocidade
    # TODO: ativar ele no loop de controle de selecao de dificuldade
    # TODO: ajustar valores da velocidade (-1,-2,-3) 
    def set_scroll_speed(self):
        if self.level == 0 or self.level == 1:
            self.scroll_speed = -1
        elif self.level == 2:
            self.scroll_speed = -2
        elif self.level == 3:
            self.scroll_speed = -3
            
    # movimenta os tubos
    def scroll_pipe(self):
        for pipe in self.pipe_list:
            pipe[0].x += scroll 
            pipe[1].x += scroll 
            
    # desenha os tubos
    def draw_pipe(self):
        width = pipe_img.get_width()
        height = pipe_img.get_height()
        for pipe in self.pipe_list:
            screen.blit(pygame.transform.flip(pipe_img, False, True), pipe[0].topleft, (0, height - pipe[0].height, width, pipe[0].height))
            screen.blit(pipe_img, pipe[1].topleft, (0, 0, width, pipe[1].height))
       
    # detectar colisao com o primeiro da lista
    def collision_detect(self):
        # colide com um tubo (cima, baixo) e chao
        return self.mario_rect.colliderect(self.pipe_list[0][0]) or \
        self.mario_rect.colliderect(self.pipe_list[0][1]) or \
        (self.mario_rect.bottom + self.mario_speed) >= (HEIGHT - GND_HEIGHT)
         
    # atualiza a pontos e desenha o score
    def update_score(self):
        if self.pipe_list[0][0].x == -50: #conseguiu passar pelo tubo
            self.score += 1
       
    # desenha pontos
    def draw_score(self):
        screen.blit(score_img, (WIDTH/2  - 50, 10))
        texto = large_font.render(str(self.score), True, WHITE)
        screen.blit(texto, (WIDTH/2 - 20, 28))
        
    # desliza o ground e parallax
    def scroll_ground(self):
        self.ground_pos += scroll
        if self.ground_pos < -WIDTH:
            self.ground_pos = 0
        
    # desenha o chao
    def draw_ground(self):
        screen.blit(ground,  (self.ground_pos, 460)) 
        screen.blit(ground,  (WIDTH + self.ground_pos, 460))
 
    # desenha o sprite adequado do mario trocando-o de acordo com a speed do rect
    def draw_mario(self, live=True):
        if live:
            if self.mario_speed <= 0:
                screen.blit(mario_sprite, (self.mario_rect.left, self.mario_rect.top-20), (0,0,40,60))
            if 0 < self.mario_speed < 15:
                screen.blit(mario_sprite, (self.mario_rect.left, self.mario_rect.top-20), (40,0,40,60))
            if 15 < self.mario_speed < 24:
                screen.blit(mario_sprite, (self.mario_rect.left, self.mario_rect.top-20), (80,0,40,60))
            if self.mario_speed > 24:
                screen.blit(mario_sprite, (self.mario_rect.left, self.mario_rect.top-20), (120,0,40,60))
        else:
            screen.blit(mario_sprite, (self.mario_rect.left, self.mario_rect.top-20), (160,0,40,60))
            
    # desenha o parallax 
    def draw_parallax(self):
        screen.blit(background, (0, 0))
        
    # reseta parametros
    def reset(self):
        self.mario_rect.y = 200
        self.ground_pos = 0
        self.pipe_list = []
        self.score = 0
        self.mario_speed =  0
        
    def start(self):
        hammer_counter = 0
        cursor1_pos = 0
        cursor2_pos = 0
        while True:
            clock.tick(30)
            screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    # gerencia a troca de modos de jogo quando o espaco eh apertado
                    if event.key == K_SPACE:
                        if self.game_mode == 2:
                            self.game_mode = 3
                        elif self.game_mode == 3:
                            self.mario_speed -= 13
                    # gerencia a troca de modos de jogo quando o enter eh apertado
                    if event.key == K_RETURN or event.key == K_KP_ENTER :
                        if self.game_mode == 1:
                            self.level = cursor1_pos
                            self.set_scroll_speed()
                            self.game_mode = 2
                        elif self.game_mode == 4:
                            if cursor2_pos == 0: #PLAY AGAIN? <YES>
                                self.game_mode = 2
                            else: #PLAY AGAIN? <NO>
                                self.game_mode = 1
                                cursor2_pos = 0
                            self.reset()
                    if event.key == K_UP:
                        if self.game_mode == 1 and cursor1_pos > 0:
                            cursor1_pos -= 1
                        if self.game_mode == 4 and cursor2_pos > 0:
                            cursor2_pos -= 1
                    if event.key == K_DOWN:
                        if self.game_mode == 1 and cursor1_pos < 3:
                            cursor1_pos += 1
                        if self.game_mode == 4 and cursor2_pos < 1:
                            cursor2_pos += 1
                        
        #-----------------------------------------------------------------------
        # GERENCIA OS MODOS DE JOGO
        # 1 modo inicial; 2 preparacao para o jogo; 3 rodando jogo; 4 game over
        #-----------------------------------------------------------------------
            # MODO DE JOGO 1: MODO INICIAL
            if self.game_mode == 1: 
                self.draw_parallax()
                self.draw_ground()
                self.scroll_ground()              
                # desenha o titulo, level e assinatura
                screen.blit(game_title,  (50, 50))
                screen.blit(level_img, (400,300))
                screen.blit(signature, (250, 550))
                screen.blit(cursor_img, (370, 300 + 25*cursor1_pos)) 
           
            # MODO DE JOGO 2: PREPARACAO (GET READY)
            elif self.game_mode == 2:
                self.draw_parallax()
                self.draw_ground()
                self.draw_mario()
                self.scroll_ground()
                # desenha instrucoes
                screen.blit(get_ready,  (300, 100))
                # desenha animacao do mario
                # TODO: ajustar o tempo da animacao do martelo
                if hammer_counter > 25:
                    screen.blit(crush,  (430, 370))
                    hammer_counter = 0
                screen.blit(mario_hammer,  (420, 390), (60*(hammer_counter//5), 0, 60, 100))
                hammer_counter += 1
        
            # MODO DE JOGO 3: RODANDO O JOGO EM SI
            elif self.game_mode == 3:
                # TODO: AQUI MUDAR OS VALORES DAS DISTANCIAS PARA MODULAR A DIFICULDADE
                # TODO: ajustar os criterios as medidas de como adiciona os tubos 
                # gera obstaculos 
                if len(self.pipe_list) == 0 or self.pipe_list[-1][0].x == (WIDTH - self.gap_width):
                    self.create_pipe()
                # remove obstaculos que 
                if self.pipe_list[0][0].x < -pipe_img.get_width():
                    self.pipe_list.remove(self.pipe_list[0])
                self.draw_parallax()
                self.draw_pipe()
                self.draw_ground()
                self.draw_mario() 
                # desenha placar
                screen.blit(score_img, (WIDTH/2 - 50, 10))
                text = large_font.render(str(self.score), True, WHITE)
                screen.blit(text, (WIDTH/2 - 20, 28))
                self.scroll_ground()
                self.scroll_pipe()
                self.update_score()
                # atualiza posicao do mario e do rect 
                self.mario_speed += GRAVITY
                self.mario_rect.top += self.mario_speed
                # restricao do limite superior
                if (self.mario_rect.top + self.mario_speed) <= 0: 
                    self.mario_speed = 0
                if self.collision_detect():
                    self.game_mode = 4
        
            # MODO DE JOGO 4: TELA DE PONTUACAO E GAME OVER
            elif self.game_mode == 4:
                self.draw_parallax()
                self.draw_pipe()
                self.draw_ground()
                self.draw_mario(False)
                # quando a animacao acaba desenha game over e o score
                if self.mario_rect.bottom >= HEIGHT - GND_HEIGHT:
                    # para o personagem no chao
                    self.mario_speed = 0
                    self.mario_rect.bottom = HEIGHT - GND_HEIGHT
                    # desenha o placar
                    screen.blit(score_gameover,  (WIDTH/2 - 200, 100))
                    # mostra o score e o best score
                    text = large_font.render(str(self.score), True, BLACK)
                    screen.blit(text, (600, 210))
                    if self.score > self.best_score:
                        self.best_score = self.score
                    text = large_font.render(str(self.best_score), True, BLACK)
                    screen.blit(text, (600, 290))
                   ### text = small_font.render("press enter to play again", True, BLACK)
                   ### screen.blit(text, (300, 550))
                    # mostra medalha correspondente 20, 40, 60, 80
                    # TODO: mecher na modulacao da dificuldade (sistema de recompensa)
                    if self.score > 20 : #bronze
                        screen.blit(medals, (340, 225), (0,0,80,100))
                    if self.score > 40: #prata
                        screen.blit(medals, (340, 225), (80,0,80,100))
                    if self.score > 60: #ouro
                        screen.blit(medals, (340, 225), (160,0,80,100))
                    if self.score > 80: #diamante
                        screen.blit(medals, (340, 225), (240,0,80,100))
                    # desenha o play again
                    screen.blit(play_again, (300, 400))
                    screen.blit(cursor_img, (580, 405 + 30*cursor2_pos))
                else:
                    self.mario_speed += GRAVITY
                    self.mario_rect.top += self.mario_speed
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.start()
