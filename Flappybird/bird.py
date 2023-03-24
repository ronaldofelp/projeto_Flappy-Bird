import pygame
import os
import random


# CONSTANTES
TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSAROS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png' ))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png' ))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png' ))),
]


pygame.font.init()

FONTE_PONTOS = pygame.font.SysFont('arial', 50)


# Objetos

class Passaro:

    IMGS = IMAGENS_PASSAROS
    # animações da rotação
    ROTACAO_MAXIMA = 25 
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]



    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y
  
    def mover(self):
        # calcular o deslocamento 
        self.tempo += 1
        deslocamento = 1.5 *(self.tempo**2) + self.velocidade * self.tempo
        # restringir o deslocamento 
        if deslocamento > 16:
            deslocamento = 16

        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # angulo do passaro 

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA

        else:

            if self.angulo > - 90:
                self.angulo -= self.VELOCIDADE_ROTACAO

        
    def desenhar(self, tela):
        # definir quaal imagem do passaro usar 
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]

        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]

        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]

        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]

        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]


        # se o passaro tiver caindo | não baater asas

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2
        
        # desenhar imagem

        imagem_rotacionada = pygame.transform.ratate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.angulo))
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)


    def get_mask(self):
        pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5
    
    def __init__(self,x):
        self.x = x
        self.altura = 0
        self.pos_top = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE  = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_top = self.altura - self.CANO_TOPO.get_height()
        self.pos_base =  self.altura + self.DISTANCIA


