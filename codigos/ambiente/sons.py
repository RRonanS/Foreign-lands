# Este arquivo é usado para chamar e armazenar os efeitos sonoros do jogo
import pygame.mixer
from codigos.variaveis import volume

pygame.mixer.init()

dir = 'arquivos/sons/efeitos/'
espada1 = pygame.mixer.Sound(dir+'sword1.wav')
espada2 = pygame.mixer.Sound(dir+'sword2.wav')
espada3 = pygame.mixer.Sound(dir+'sword3.wav')
espadas = espada1, espada2, espada3

levelup = pygame.mixer.Sound(dir+'levelup.mp3')
levelup.set_volume(volume*0.5)

mercador_saudar = pygame.mixer.Sound(dir+'mercador.mp3')

monstros_sounds = {
    'esqueleto':
        {
            'death': pygame.mixer.Sound(dir+'skeletondeath.mp3')
        },
    'boss1':
        {
            'death': pygame.mixer.Sound(dir+'boss1death.mp3'),
            'find': pygame.mixer.Sound(dir+'risadaboss.mp3')
        },
    'goblin':
        {
          'death': pygame.mixer.Sound(dir+'goblindeath.mp3')
        },
    'olho':
        {
            'find': pygame.mixer.Sound(dir+'olhowalk.mp3'),
            'hit': pygame.mixer.Sound(dir+'olhohit.mp3')
        },
    'cogumelo':
        {

        },
    'bringerdeath':
        {

        }
}

efeitos_cenarios = {
    1: pygame.mixer.Sound(dir+'scare1.mp3'),
    2: pygame.mixer.Sound(dir+'scare2.mp3'),
    3: pygame.mixer.Sound(dir + 'scare3.mp3')
}
