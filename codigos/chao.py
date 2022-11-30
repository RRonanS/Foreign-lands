# Este arquivo possui os construtores de objetos para o chão do jogo
import pygame.sprite
from random import randint
from .variaveis import screen_size, block_size

width, height = screen_size

dir = 'arquivos/imagens/blocos/'
decdir = 'arquivos/imagens/decorativo/'


class Terra(pygame.sprite.Sprite):
    '''Classe para representar um bloco de terra(podendo variar a imagem dele)'''
    def __init__(self, pos, num=0, flip=False):
        '''Recebe a posição da diagonal superior esquerda do bloco e caso queira
        um bloco específico passe o número dele como parâmetro'''
        pygame.sprite.Sprite.__init__(self)
        if num == 0:
            num = randint(1, 4)
        img = pygame.image.load(dir+f'terra{num}'+'.png')
        if flip:
            img = pygame.transform.rotate(img, 90)
        img = pygame.transform.scale(img, block_size)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.mask = pygame.mask.from_surface(self.image)


class Chao:
    '''Classe para representar o chão do jogo, faz a união de diversos blocos'''
    def __init__(self, tam, bloco_id=0, tipo=0):
        self.grupo = pygame.sprite.Group()
        self.bloco_id, self.tipo = bloco_id, tipo
        xi, xf, yi, yf = tam
        for i in range(xi, xf, block_size[0]):
            for j in range(yi, yf, -block_size[1]):
                bloco = Terra((i, j-block_size[1]), bloco_id)
                self.grupo.add(bloco)

    def add_bloco(self, pos, bloco_id=-1):
        if bloco_id == -1:
            bloco_id = self.bloco_id
        i, j = pos
        bloco = Terra((i, j-block_size[1]), bloco_id)
        for x in pygame.sprite.spritecollide(bloco, self.grupo, False):
            if x.rect == bloco.rect:
                x.kill()
        self.grupo.add(bloco)
        return self

    def add_coluna(self, x):
        for i in range(0, height, block_size[1]):
            bloco = Terra((x, i), self.bloco_id, True)
            self.grupo.add(bloco)
        return self

    def add_linha(self, y):
        for i in range(0, width, block_size[0]):
            bloco = Terra((i, y), self.bloco_id)
            self.grupo.add(bloco)
        return self