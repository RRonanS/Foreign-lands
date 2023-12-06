# Classes de objetos decorativos no mapa
import pygame
from codigos.variaveis import block_size, fps

try:
    dir = 'arquivos/imagens/'
    c = pygame.image.load(dir + 'decorativo/coin.png').convert_alpha()
    l = [c.subsurface((0, 0, 3, 16)), c.subsurface((11, 0, 12, 16)), c.subsurface((26, 0, 14, 16)),
         c.subsurface((43, 0, 12, 16)), c.subsurface(64, 0, 3, 16)]
    imgs = {
        'Casa':
            {
                i: pygame.image.load(dir+f'/vila/home{i}.png') for i in range(1, 6)
            },
        'Coin':
            l
    }
except pygame.error as E:
    print('[Erro] Problema ao carregar as imagens do decorativo.py', E)
    imgs = {}

class Coin(pygame.sprite.Sprite):
    """Representa uma moeda que pode ser coletada pelo jogador"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = 'decorativo'
        self.images = imgs['Coin']
        self.index = 0
        self.vel = 0.25 * (30/fps)
        self.value = 1
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def update(self):
        """Animação da moeda"""
        self.index += self.vel
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[int(self.index)]


class Casa(pygame.sprite.Sprite):
    def __init__(self, index, blocos=1):
        self.tipo = 'decorativo'
        self.index = index
        self.blocos = blocos
        self.bloqueia = False
        pygame.sprite.Sprite.__init__(self)
        img = imgs['Casa'][index]
        img = pygame.transform.scale(img, (block_size[0]*blocos, block_size[1]*blocos))
        self.image = img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def flip(self):
        self.image = pygame.transform.rotate(self.image, 180)

    def update(self):
        pass


class Portal(pygame.sprite.Sprite):
    """Classe para representar um portal entre cenarios"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = 'decorativo'
        self.destino = 0, 0
        self.coord_destino = 0, 0

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
