# Este arquivo possui os construtores para todos monstros usados no jogo e funções
# para gerar monstros pelo mapa
import pygame.sprite
from ..outros.auxiliares import img_load
from ..variaveis import char_size, screen_size, exp_mult, fps
from random import randint, random
from ..mapa.decorativo import Coin

width, height = screen_size


class Monstro(pygame.sprite.Sprite):
    """Classe pai para representar todas entidades"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.visao = 0.3
        self.vel = 2 * (30 / fps)
        self.coin_drop = (1, 1)
        self.tipo = 'monster'
        self.voa = False
        self.drops = []
        self.diretorio = 'arquivos/imagens/monstros/'
        self.images = {}
        self.is_boss = False
        self.anim_mult = 0.2 * (30 / fps)

    def drop(self):
        """Gera os drops referentes a tal inimigo"""
        moeda = Coin()
        val = randint(self.coin_drop[0], self.coin_drop[1])
        moeda.value = val
        x, y = self.rect.centerx, self.rect.centery
        moeda.rect.centerx, moeda.rect.centery = x, y
        return moeda


class Esqueleto(Monstro):
    """Herda da classe pai e representa um esqueleto"""

    class sprite_espada(pygame.sprite.Sprite):
        """Classe chamada apenas durante ataques para calculo de colisão da espada"""

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
        self.exp = 15 * exp_mult

        sprite_size = 150, 150
        self.sector, self.index = 'idle', 0
        self.diretorio += 'Skeleton/'
        # Chamada e armazenamento das imagens do monstro
        idle = pygame.image.load(self.diretorio + 'Idle.png').convert_alpha()
        attack = pygame.image.load(self.diretorio + 'Attack.png').convert_alpha()
        walk = pygame.image.load(self.diretorio + 'Walk.png').convert_alpha()
        dead = pygame.image.load(self.diretorio + 'Death.png').convert_alpha()
        self.images['idle'] = img_load(idle, sprite_size, char_size, True)
        self.images['attack'] = img_load(attack, sprite_size, char_size, True)
        self.images['walk'] = img_load(walk, sprite_size, char_size, True)
        self.images['death'] = img_load(dead, sprite_size, char_size, True)

        # Varíaveis de funcionamento
        self.image = self.images[self.sector][self.index]
        self.rect = self.image.get_rect()
        self.rect.bottomright = screen_size
        self.mask = pygame.mask.from_surface(self.images['idle'][0])
        self.dir = 0, 0
        self.flip, self.ataque, self.dead, self.busy = False, False, False, False
        self.animar = True

    def atacar(self):
        """Caso possível, executa um ataque"""
        if self.sector != 'attack' and self.animar:
            self.sector = 'attack'
            self.animar = False

    def ataque_sprite(self):
        """Gera a sprite usada no cálculo de colisoes"""
        return self.sprite_espada(self.images['attack'], self.rect, self.flip)

    def update_especifico(self):
        """Update especifico para ser editado em subclasses, representando atualizações individuais"""
        pass

    def rand_walk(self):
        """Gera um valor aleatorio de movimento para a entidade"""
        if random() <= self.random_walk_mult:
            nao_move = randint(0, 3)
            if nao_move == 0:
                # Gera os valores de movimentação aleatoria
                vai_x, vai_y = randint(0, 1), randint(0, 1)
                dx = dy = 0
                if vai_x:
                    dx = randint(1, width // 2)
                if vai_y:
                    dy = randint(1, height // 2)
                self.dir = dx, dy

    def update(self):
        self.update_especifico()
        if self.dir[0] == 0 and self.dir[1] == 0:
            self.sector = 'idle'
        if self.vida <= 0:
            self.animar = False
            self.sector = 'death'

        # Parte das animações
        self.index += self.anim_mult
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
            img = pygame.transform.flip(self.images[self.sector][int(self.index)],
                                        True, False)
        else:
            img = self.images[self.sector][int(self.index)]
        self.image = img

    def mover(self, ver_func, ver_func2):
        """Dado o vetor de dir do objeto e as verificacoes de validade do chao, avança para uma nova posição válida,
        se essa existir """
        if self.animar:
            self.sector = 'walk'
            if self.dir[0] != 0:
                # Movimentação no eixo x
                sinal = -1
                self.flip = False
                if self.dir[0] < 0:
                    sinal = +1
                    self.flip = True
                self.rect.centerx += self.vel * sinal
                # Verifica se a posição nova é válida
                if not self.voa:
                    if not (ver_func(self.rect.center)) or ver_func2(self.rect):
                        self.rect.centerx -= self.vel*sinal

            if self.dir[1] != 0:
                # Movimentação no eixo y
                sinal = -1
                if self.dir[1] < 0:
                    sinal = 1
                self.rect.centery += self.vel * sinal
                # Verifica se a nova posição é válida
                if not self.voa:
                    if not (ver_func(self.rect.center)) or ver_func2(self.rect):
                        self.rect.centery -= self.vel*sinal
            # Arredondamento do restante do movimento
            if abs(self.dir[0]) < self.vel:
                self.dir = 0, self.dir[1]
            if abs(self.dir[1]) < self.vel:
                self.dir = self.dir[0], 0


class Olho(Esqueleto):
    """Representa o monstro Olho, herda do esquelto, mudando apenas imagens
     e varíaveis gerais"""

    def __init__(self):
        Esqueleto.__init__(self)

        self.vida_max, self.vida = 15, 15
        self.dano, self.vel, self.peso = 3, 3 * (30 / fps), 3
        self.visao = 0.5
        self.exp = 20 * exp_mult
        self.voa = True

        sprite_size = 150, 150
        self.diretorio = self.diretorio.replace('Skeleton/', 'Flying eye/')

        attack = pygame.image.load(self.diretorio + 'Attack.png').convert_alpha()
        flight = pygame.image.load(self.diretorio + 'Flight.png').convert_alpha()
        dead = pygame.image.load(self.diretorio + 'Death.png').convert_alpha()
        self.images = {'idle': img_load(flight, sprite_size, char_size, True),
                       'attack': img_load(attack, sprite_size, char_size, True),
                       'walk': img_load(flight, sprite_size, char_size, True),
                       'death': img_load(dead, sprite_size, char_size, True)}
        self.image = self.images[self.sector][self.index]


class Goblin(Esqueleto):
    """Representa o monstro Goblin, herda do esquelto, mudando apenas imagens
     e varíaveis gerais"""

    def __init__(self):
        Esqueleto.__init__(self)

        self.vida_max, self.vida = 20, 20
        self.dano, self.peso, self.vel = 5, 5 * (30 / fps), 1
        self.visao = 0.25
        self.exp = 35 * exp_mult
        size = char_size[0] * 1.5, char_size[1] * 1.5

        sprite_size = 150, 150
        self.diretorio = self.diretorio.replace('Skeleton/', 'Goblin/')

        attack = pygame.image.load(self.diretorio + 'Attack.png').convert_alpha()
        idle = pygame.image.load(self.diretorio + 'Idle.png').convert_alpha()
        run = pygame.image.load(self.diretorio + 'Run.png').convert_alpha()
        dead = pygame.image.load(self.diretorio + 'Death.png').convert_alpha()
        self.images = {'idle': img_load(idle, sprite_size, size, True),
                       'attack': img_load(attack, sprite_size, size, True),
                       'walk': img_load(run, sprite_size, size, True),
                       'death': img_load(dead, sprite_size, size, True)}
        self.image = self.images[self.sector][self.index]
        self.mask = pygame.mask.from_surface(self.images['attack']
                                             [len(self.images['attack']) - 1])
        self.rect = self.image.get_rect()


class Cogumelo(Esqueleto):
    """Representa o monstro Cogumelo, herda do esquelto, mudando apenas imagens
     e varíaveis gerais"""

    def __init__(self):
        Esqueleto.__init__(self)

        self.vida_max, self.vida = 25, 25
        self.dano, self.vel, self.peso = 7, 2 * (30 / fps), 8
        self.visao = 0.20
        self.exp = 50 * exp_mult

        sprite_size = 150, 150
        size = char_size[0] * 1.5, char_size[1] * 1.5
        self.diretorio = self.diretorio.replace('Skeleton/', 'Mushroom/')

        attack = pygame.image.load(self.diretorio + 'Attack.png').convert_alpha()
        idle = pygame.image.load(self.diretorio + 'Idle.png').convert_alpha()
        run = pygame.image.load(self.diretorio + 'Run.png').convert_alpha()
        dead = pygame.image.load(self.diretorio + 'Death.png').convert_alpha()
        self.images = {'idle': img_load(idle, sprite_size, size, True),
                       'attack': img_load(attack, sprite_size, size, True),
                       'walk': img_load(run, sprite_size, size, True),
                       'death': img_load(dead, sprite_size, size, True)}
        self.image = self.images[self.sector][self.index]
        self.mask = pygame.mask.from_surface(self.images['attack']
                                             [len(self.images['attack']) - 1])

    def ataque_sprite(self):
        """Retorna a sprite usada no calculo de colisões"""
        return self.sprite_espada(self.images['attack'], self.rect, self.flip, 7)


class Spawner:
    def __init__(self):
        pass

