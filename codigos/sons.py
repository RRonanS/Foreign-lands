# Este arquivo é usado para chamar e armazenar os efeitos sonoros do jogo
import pygame.mixer

pygame.mixer.init()

dir = 'arquivos/sons/efeitos/'
espada1 = pygame.mixer.Sound(dir+'sword1.wav')
espada2 = pygame.mixer.Sound(dir+'sword2.wav')
espada3 = pygame.mixer.Sound(dir+'sword3.wav')
espadas = espada1, espada2, espada3

levelup = pygame.mixer.Sound(dir+'levelup.mp3')
