# Este arquivo possui os construtores para todos monstros usados no jogo e funções
# para gerar monstros pelo mapa
import pygame.sprite
from .auxiliares import img_load
from .variaveis import char_size, screen_size, exp_mult
from random import choice, randint, random
from .decorativo import Coin


width, height = screen_size


class Monstro(pygame.sprite.Sprite):
    '''Classe pai para representar todas entidades'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.visao = 0.3
        self.vel = 2
        self.coin_drop = (1, 1)
        self.tipo = 'Monster'
        self.drops = []
        self.diretorio = 'arquivos/imagens/monstros/'
        self.images = {}
        self.is_boss = False

    def drop(self):
        moeda = Coin()
        val = randint(self.coin_drop[0], self.coin_drop[1])
        moeda.value = val
        x, y = self.rect.centerx, self.rect.centery
        moeda.rect.centerx, moeda.rect.centery = x, y
        return moeda


class Esqueleto(Monstro):
    '''Herda da classe pai e representa um esqueleto'''
    class sprite_espada(pygame.sprite.Sprite):
        '''Classe chamada apenas durante ataques para calculo de colisão da espada'''
        def __init__(self, img, pos, flip, index=6):
            pygame.sprite.Sprite.__init__(self)
            self.image = img[index]
            self.rect = self.image.get_rect()
            self.rect = pos
            if flip:
                self.mask = pygame.mask.from_surface(pygame.transform.flip(
                    img[index], True, False
                ))
            else:
                self.mask = pygame.mask.from_surface(img[index])

    def __init__(self):
        Monstro.__init__(self)

        # variáveis da entidade
        self.vida, self.vida_max = 10, 10
        self.dano, self.peso = 2, 2
        self.random_walk_mult = 0.02
        self.exp = 15*exp_mult

        sprite_size = 150, 150
        self.sector, self.index = 'idle', 0
        self.diretorio += 'Skeleton/'
        # Chamada e armazenamento das imagens do monstro
        idle = pygame.image.load(self.diretorio+'Idle.png')
        attack = pygame.image.load(self.diretorio+'Attack.png')
        walk = pygame.image.load(self.diretorio+'Walk.png')
        dead = pygame.image.load(self.diretorio+'Death.png')
        self.images['idle'] = img_load(idle, sprite_size, char_size, True)
        self.images['attack'] = img_load(attack, sprite_size, char_size, True)
        self.images['walk'] = img_load(walk, sprite_size, char_size, True)
        self.images['death'] = img_load(dead, sprite_size, char_size, True)

        # Varíaveis de funcionamento
        self.image = self.images[self.sector][self.index]
        self.rect = self.image.get_rect()
        self.rect.bottomright = screen_size
        self.mask = pygame.mask.from_surface(self.images['idle'][0])
        self.dir = (-1, self.vel)
        self.flip, self.ataque, self.dead, self.busy = False, False, False, False
        self.animar = True
        self.left = [0, 0, 0]

    def atacar(self):
        '''Caso possível, executa um ataque'''
        if self.sector != 'attack' and self.animar:
            self.sector = 'attack'
            self.animar = False

    def ataque_sprite(self):
        return self.sprite_espada(self.images['attack'], self.rect, self.flip)

    def update_especifico(self):
        pass

    def update(self):
        self.update_especifico()
        if self.busy:
            if self.left[0] <= 0 and self.left[1] <= 0:
                self.busy = False
        if self.vida <= 0:
            self.animar = False
            self.sector = 'death'
        # Parte responsável por movimentar a entidade aleatoriamente
        if self.dir[0] != -1 and not self.busy:
            if random() <= 3*self.random_walk_mult:
                self.dir = -1, self.dir[1]
        if random() <= self.random_walk_mult:
            d = randint(0, 5)
            sinal = choice((0, 1))
            if sinal == 0:
                v = -self.vel
            else: v = self.vel
            if d <= 3:
                self.dir = (0, v)
            else:
                self.dir = (1, v)

        # Parte das animações
        self.index += 0.2
        if self.index >= len(self.images[self.sector]):
            self.index = 0
            if self.sector == 'attack':
                self.sector = 'idle'
                self.animar = True
                self.ataque = True
            elif self.sector == 'walk' and self.dir[0] == -1:
                self.sector = 'idle'
            if self.sector == 'death':
                self.vel = 0
                self.dead = True

        if self.flip:
            img = pygame.transform.flip(self.images[self.sector][int(self.index)]
                                        , True, False)
        else:
            img = self.images[self.sector][int(self.index)]
        self.image = img


class Olho(Esqueleto):
    '''Representa o monstro Olho, herda do esquelto, mudando apenas imagens
     e varíaveis gerais'''
    def __init__(self):
        Esqueleto.__init__(self)

        self.vida_max, self.vida = 7, 7
        self.dano, self.vel, self.peso = 3, 3, 3
        self.visao = 0.5
        self.exp = 20*exp_mult

        sprite_size = 150, 150
        self.diretorio = self.diretorio.replace('Skeleton/', 'Flying eye/')

        attack = pygame.image.load(self.diretorio+'Attack.png')
        flight = pygame.image.load(self.diretorio+'Flight.png')
        dead = pygame.image.load(self.diretorio+'Death.png')
        self.images = {'idle': img_load(flight, sprite_size, char_size, True),
                       'attack': img_load(attack, sprite_size, char_size, True),
                       'walk': img_load(flight, sprite_size, char_size, True),
                       'death': img_load(dead, sprite_size, char_size, True)}
        self.image = self.images[self.sector][self.index]


class Goblin(Esqueleto):
    '''Representa o monstro Goblin, herda do esquelto, mudando apenas imagens
     e varíaveis gerais'''
    def __init__(self):
        Esqueleto.__init__(self)

        self.vida_max, self.vida = 13, 13
        self.dano, self.peso, self.vel = 4, 5, 1
        self.visao = 0.25
        self.exp = 25*exp_mult
        size = char_size[0]*1.5, char_size[1]*1.5

        sprite_size = 150, 150
        self.diretorio = self.diretorio.replace('Skeleton/', 'Goblin/')

        attack = pygame.image.load(self.diretorio+'Attack.png')
        idle = pygame.image.load(self.diretorio+'Idle.png')
        run = pygame.image.load(self.diretorio+'Run.png')
        dead = pygame.image.load(self.diretorio+'Death.png')
        self.images = {'idle': img_load(idle, sprite_size, size, True),
                       'attack': img_load(attack, sprite_size, size, True),
                       'walk': img_load(run, sprite_size, size, True),
                       'death': img_load(dead, sprite_size, size, True)}
        self.image = self.images[self.sector][self.index]
        self.mask = pygame.mask.from_surface(self.images['attack']
                                             [len(self.images['attack']) - 1])
        self.rect = self.image.get_rect()


class Cogumelo(Esqueleto):
    '''Representa o monstro Cogumelo, herda do esquelto, mudando apenas imagens
     e varíaveis gerais'''
    def __init__(self):
        Esqueleto.__init__(self)

        self.vida_max, self.vida = 20, 20
        self.dano, self.vel, self.peso = 5, 2, 8
        self.visao = 0.20
        self.exp = 30*exp_mult

        sprite_size = 150, 150
        size = char_size[0]*1.5, char_size[1]*1.5
        self.diretorio = self.diretorio.replace('Skeleton/', 'Mushroom/')

        attack = pygame.image.load(self.diretorio+'Attack.png')
        idle = pygame.image.load(self.diretorio+'Idle.png')
        run = pygame.image.load(self.diretorio+'Run.png')
        dead = pygame.image.load(self.diretorio+'Death.png')
        self.images = {'idle': img_load(idle, sprite_size, size, True),
                       'attack': img_load(attack, sprite_size, size, True),
                       'walk': img_load(run, sprite_size, size, True),
                       'death': img_load(dead, sprite_size, size, True)}
        self.image = self.images[self.sector][self.index]
        self.mask = pygame.mask.from_surface(self.images['attack']
                                             [len(self.images['attack']) - 1])

    def ataque_sprite(self):
        return self.sprite_espada(self.images['attack'], self.rect, self.flip, 7)


def gerar_inimigos(dificuldade, cenarios, inimigos):
    '''Recebe uma tupla cenários, indicando o cenário inicial e final onde serão
    gerados inimigos, gera os inimigos os adicionando no sprite Group inimigos'''
    def inimigo_from_nivel(x):
        if x == 0:
            return Esqueleto()
        elif x == 1:
            return Olho()
        elif x == 2:
            return Goblin()
        elif x == 3:
            return Cogumelo()
    nivel = [1, 0, 0, 0]
    acrescimos = [0.5, 0.25, 0.1, 0.07]
    maximos = [4, 3, 2, 2]
    for i in range(cenarios[0], cenarios[1]):
        posx = randint((i * width) + 150, (i * width) + width)
        for j in range(len(nivel)):
            if nivel[j] >= 1:
                for i in range(int(nivel[j])):
                    inimigo = inimigo_from_nivel(j)
                    inimigo.rect.x = posx
                    inimigos.add(inimigo)
            if nivel[j] < maximos[j]:
                nivel[j] += acrescimos[j]
