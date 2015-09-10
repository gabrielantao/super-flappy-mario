#-------------------------------------------------------------------------------
# Name:        Flappy Mario v1.3
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
import pygame
from pygame.locals import *
from vetores import *
pygame.init()

LARGURA = 1000
ALTURA = 600
BRANCO = (255,255,255)
PRETO = (0,0,0)
LACUNAX = 300 # espaço horizontal para que o sprite possa passar
LACUNAY = 120 # espaço vertical para que o sprite possa passar

# cria o clock
clock = pygame.time.Clock()

# inicializa janela
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Super Flappy Mario v1.3")

# carrega imagens e fonte
fundo = pygame.image.load("images/parallax.png")
solo  = pygame.image.load("images/solo.png")
placar = pygame.image.load("images/placar.png")
marioflappy = pygame.image.load("images/Super Flappy Mario TM.png")
botao_start = pygame.image.load("images/start.png")
mario_martelo = pygame.image.load("images/mario martelo.png")
batida = pygame.image.load("images/efeito batida.png")
get_ready = pygame.image.load("images/get ready.png")
placar_gameover = pygame.image.load("images/placar game over.png")
medalhas = pygame.image.load("images/medalhas.png")
mario_sprite = pygame.image.load("images/mario sprite.png")
assinatura = pygame.image.load("images/assinatura.png")
tubo = pygame.image.load("images/tubo.png")

fonte = pygame.font.Font("fonts/Super Mario World font.ttf", 32)
fonte2 = pygame.font.Font("fonts/Super Mario World font.ttf", 20)

# cria vetores
gravidade  = Vetor(0,1)
velocidade = Vetor(0,0)
scroll = Vetor(-5, 0)

# cria contadores para animações
contador_martelo = 0


# cria rect que detecta a colisão
bloco = pygame.Rect(50,200,40,40)

# variavel para posição do solo
pos_solo = 0

# cria lista de obstaculos (rects)
lista_obstaculos = []

#cria o modo em que o jogo está rodando
# 1 modo inicial; 2 preparação para o jogo; 3 rodando jogo; 4 game over
modo_jogo = 1

# cria pontuação e record
pontuacao = 0
record = 0

# função geadora de obstáculos
def gera_obstaculos():
    global lista_obstaculos
    aleatorio = random.randrange(0, ALTURA-LACUNAY-80, 20)
    obstaculo_cima = pygame.Rect(LARGURA, 0, 100, aleatorio)
    if aleatorio != ALTURA-LACUNAY-80:
        obstaculo_baixo = pygame.Rect(LARGURA, aleatorio+LACUNAY, 100, (ALTURA-(aleatorio+LACUNAY))-80)
    else:
        obstaculo_baixo = None
    lista_obstaculos.append([obstaculo_cima, obstaculo_baixo])

# desenha obstaculos
def desenha_obstaculos():
    global lista_obstaculos
    for obstaculo in lista_obstaculos:
##        pygame.draw.rect(janela, PRETO, obstaculo[0], 4) # obstaculo de cima
##        pygame.draw.rect(janela, PRETO, obstaculo[1], 4) # obstaculo de baixo
        janela.blit(pygame.transform.flip(tubo,False,True), obstaculo[0].topleft, (0,400-obstaculo[0].height,100, obstaculo[0].height))
        janela.blit(tubo, obstaculo[1].topleft,(0, 0, 100, obstaculo[1].height))


# movimenta os obstaculos
def movimenta_obstaculos():
    global lista_obstaculos
    for obstaculo in lista_obstaculos:
        obstaculo[0].x += scroll.i # obstaculo de cima
        obstaculo[1].x += scroll.i # obstaculo de baixo

# detectar colisão
def detecta_colisao():
    global lista_obstaculos, modo_jogo
    if bloco.colliderect(lista_obstaculos[0][0]) == True or bloco.colliderect(lista_obstaculos[0][1]):
        modo_jogo = 4


# atualiza a pontuação e desenha o placar
def atualiza_pontuacao():
    global lista_obstaculos, pontuacao, fonte
    if lista_obstaculos[0][0].x == -50:
        pontuacao += 1
    janela.blit(placar, (LARGURA/2-50,10))
    texto = fonte.render(str(pontuacao), True, BRANCO)
    janela.blit(texto, (LARGURA/2-20,28))

# faz scroll do solo e imprime na tela
 # faz scroll do solo se a pos_solo for menor que sua largura entao seta ela pra zero e recomeça
def scroll_solo():
    global pos_solo, scroll
    pos_solo += scroll.i
    if pos_solo < -LARGURA:
        pos_solo = 0
    janela.blit(solo,  (0+pos_solo,459))
    janela.blit(solo,  (LARGURA+pos_solo,459))

# reseta parametros
def reset():
    global bloco, pos_solo, lista_obstaculos, pontuacao, velocidade
    bloco.y = 200
    pos_solo = 0
    lista_obstaculos = []
    pontuacao = 0
    velocidade = Vetor(0,0)

# desenha o sprite adequado do mario trocando-o de acordo com a velocidade do rect
def desenha_mario(frame = None):
    global mario_sprite, velocidade
    # se for passado um frame especifico do mario_sprite desenha se nao for desenha de acordo com a velocidade
    if frame != None:
        janela.blit(mario_sprite,(bloco.left, bloco.top-20), (40*frame,0,40,60))
    else:
        if velocidade.j <= 0:
            janela.blit(mario_sprite,(bloco.left, bloco.top-20), (0,0,40,60))
        if 0 < velocidade.j < 15:
            janela.blit(mario_sprite,(bloco.left, bloco.top-20), (40,0,40,60))
        if 15 < velocidade.j < 24:
            janela.blit(mario_sprite,(bloco.left, bloco.top-20), (80,0,40,60))
        if velocidade.j > 24:
            janela.blit(mario_sprite,(bloco.left, bloco.top-20), (120,0,40,60))

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # Gerencia a troca de modos de jogo quando o espaço é apertado
            if event.key == K_SPACE:
                if modo_jogo   == 1:
                    modo_jogo = 2
                elif modo_jogo == 2:
                    modo_jogo = 3
                elif modo_jogo == 3:
                    velocidade.j = -12
            # Gerencia a troca de modos de jogo quando o enter é apertado
            if event.key == K_RETURN or event.key == K_KP_ENTER :
                if modo_jogo   == 1:
                    modo_jogo = 2
                elif modo_jogo == 2:
                    modo_jogo = 3
                elif modo_jogo == 4:
                    modo_jogo = 1
                    reset()
    #-------------------------------------------------------------------------------------------
    # GERENCIA OS MODOS DE JOGO!!!
    # 1 modo inicial; 2 preparação para o jogo; 3 rodando jogo; 4 game over

#---------------------------------
    # MODO DE JOGO 1: MODO INICIAL
    if modo_jogo == 1: #
        janela.fill(BRANCO)
        janela.blit(fundo, (0,0))
        # faz scroll do solo se a pos_solo for menor que sua largura entao seta ela pra zero e recomeça
        pos_solo += scroll.i
        if pos_solo < -LARGURA:
            pos_solo = 0
        # desenha os dois solos
        janela.blit(solo,  (0+pos_solo,459))
        janela.blit(solo,  (LARGURA+pos_solo,459))
        # desenha o logo e o botao
        janela.blit(marioflappy,  (50,50))
        janela.blit(botao_start, (LARGURA/2-50, 400))

        # assinatura
        janela.blit(assinatura,(250,550))


        pygame.display.update()

#-------------------------------------------------
    # MODO DE JOGO 2: MODO DE INSTRUÇÃO (GET READY)
    elif modo_jogo == 2:
        janela.fill(BRANCO)
        janela.blit(fundo, (0,0))
        # faz scroll do solo se a pos_solo for menor que sua largura entao seta ela pra zero e recomeça
        pos_solo += scroll.i
        if pos_solo < -LARGURA:
            pos_solo = 0
        # desenha os dois solos
        janela.blit(solo,  (0+pos_solo,459))
        janela.blit(solo,  (LARGURA+pos_solo,459))
        # desenha animação com mario batendo e, as instruções e mario voando parado.
        contador_martelo += 1
        if contador_martelo > 25 :
            contador_martelo = 0
        if contador_martelo % 5:
            i = contador_martelo/5
        janela.blit(get_ready,  (300,100))
        if i == 4:
            pygame.draw.rect(janela, (255,0,0), (450,410,90,20),4)
            janela.blit(batida,  (430,370))
##        pygame.draw.rect(janela, PRETO, (bloco.left, bloco.top, bloco.width, bloco.height),3)
        desenha_mario()
        janela.blit(mario_martelo,  (420,390), (60*i,0,60,100))

        pygame.display.update()

#-----------------------------------------
    # MODO DE JOGO 3: RODANDO O JOGO EM SI
    elif modo_jogo == 3:
        janela.fill(BRANCO)

        # checa os limites
        if (bloco.bottom + velocidade.j) >= (ALTURA - 80): # limite de baixo
            velocidade.j = 0
            bloco.bottom = ALTURA - 80
            modo_jogo = 4 # troca o modo de jogo (game over)
        elif (bloco.top + velocidade.j) <= 0: # limite de cima
            velocidade.j = 0
        else:
            velocidade = velocidade + gravidade
            bloco.top += velocidade.j  # atualiza o valor da velocidade e da posiçao do bloco

        # desenha fundo
        janela.blit(fundo, (0,0))

        # gera, desenha, remove e movimenta obstaculos e detecta colisões.
        if len(lista_obstaculos) == 0 or lista_obstaculos[-1][0].x == (LARGURA-LACUNAX):
            gera_obstaculos()
        if lista_obstaculos[0][0].x < -100: #remover os obstaculos que sairem da tela pela esquerda (fila)
            lista_obstaculos.remove(lista_obstaculos[0])
        desenha_obstaculos()
        movimenta_obstaculos()
        detecta_colisao()
        atualiza_pontuacao()


        # desenha um rect para simular a fisica
        desenha_mario()

        # faz scroll do solo se a pos_solo for menor que sua largura entao seta ela pra zero e recomeça
        pos_solo += scroll.i
        if pos_solo < -LARGURA:
            pos_solo = 0
        janela.blit(solo,  (0+pos_solo,459))
        janela.blit(solo,  (LARGURA+pos_solo,459))

        pygame.display.update()

#--------------------------------------------------
    # MODO DE JOGO 4: TELA DE PONTUAÇÃO E GAME OVER
    elif modo_jogo == 4:
        janela.fill(BRANCO)

        # faz animação quando o mario perde
        # checa os limites
        if (bloco.bottom + velocidade.j) >= (ALTURA - 80): # limite de baixo
            velocidade.j = 0
            bloco.bottom = ALTURA - 80
        else:
            velocidade = velocidade + gravidade
            bloco.top += velocidade.j # atualiza o valor da velocidade e da posiçao do bloco

        # desenha fundo
        janela.blit(fundo, (0,0))

        # desenha obstaculos onde estavam antes de perder
        desenha_obstaculos()

        # desenha o solo na mesma posição que parou anteriormente
        janela.blit(solo,  (0+pos_solo,459))
        janela.blit(solo,  (LARGURA+pos_solo,459))

        # desenha personagem a partir da posição do rect bloco
        desenha_mario(4)

        # quando a animação desenha game over e o placar
        if bloco.bottom == ALTURA - 80:
            # desenha o placar
            janela.blit(placar_gameover,  (LARGURA/2-200,100))

            # mostra o score e o best score
            texto = fonte.render(str(pontuacao), True, PRETO)
            janela.blit(texto, (600,210))
            if pontuacao > record:
                record = pontuacao
            texto = fonte.render(str(record), True, PRETO)
            janela.blit(texto, (600,290))
            texto = fonte2.render("press enter to play again", True, PRETO)
            janela.blit(texto, (300,550))

            # mostra medalha correspondente 20, 50, 100, 150
            if pontuacao > 20 :
                janela.blit(medalhas, (340,225), (0,0,80,100))
            if pontuacao > 50:
                janela.blit(medalhas, (340,225), (80,0,80,100))
            if pontuacao > 100:
                janela.blit(medalhas, (340,225), (160,0,80,100))
            if pontuacao > 150:
                janela.blit(medalhas, (340,225), (240,0,80,100))

        pygame.display.update()

# Termina aqui (testando)



