from math import sqrt
from random import randint, choice
import pygame.sprite
from codigos.entidades.balao import Balao
from codigos.variaveis import screen_size, fps
from codigos.outros.tradutor import Tradutor
from codigos.entidades.gerenciador_imagens import imagens

width, height = screen_size
tradutor = Tradutor()


def trad(x):
    return tradutor.traduzir(x)


imagens = imagens['npcs']


class Npc(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = {}
        self.tipo = 'npc'
        self.nivel = 1
        self.vida, self.vida_max = 1, 1
        self.falando = False
        self.visao = 200

    def proximidade(self, entidade):
        """Trigger de proximidade"""
        pass


class Mago(Npc):
    def __init__(self, pos):
        Npc.__init__(self)
        from codigos.variaveis import fps
        self.anim_rate = 0.2 * (30 / fps)
        self.vida, self.vida_max = 100, 100
        self.nivel = 30
        self.visao = 100
        self.speed = 5 * (30 / fps)
        self.status = 'idle'
        self.cont = 0
        self.images['idle'] = imagens['Mago']['idle']
        self.images['walk'] = imagens['Mago']['walk']
        self.images['special'] = imagens['Mago']['special']
        self.texto = 'Olá viajante,\sabe onde está?' \
                r'/Está onde outrora fora\a terra sagrada' \
                '/Porém as trevas veem tomando\conta do nosso paraiso' \
                '/e só você é capaz de mudar isso' \
                '/mate todos os chefes e então me encontre na masmorra'

        self.image = self.images[self.status][self.cont]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos
        self.fala = Balao((0, 0), '')
        self.falando = False
        self.flip = False

    def update(self):
        self.cont += self.anim_rate
        if self.cont >= len(self.images[self.status]):
            self.cont = 0

        if self.falando and len(self.fala.groups()) == 0:
            # Ou seja, a fala acabou, ande ate sumir
            if self.status == 'special' and self.cont == 0:
                self.flip = True
                self.status = 'walk'
            elif self.status != 'walk':
                self.status = 'special'
            if self.status == 'walk':
                self.rect.x += self.speed
            if self.rect.bottomleft[0] >= width:
                self.kill()

        self.image = self.images[self.status][int(self.cont)]
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

    def saudar(self):
        """Método para iniciar a fala do npc"""
        texto = self.texto
        self.fala = Balao((self.rect.x, self.rect.topleft[1] + 10), texto)
        for grupo in self.groups()[1:]:
            grupo.add(self.fala)
        self.falando = True

    def proximidade(self, entidade):
        """Trigger de proximidade"""
        if abs(sqrt((self.rect.x - entidade.rect.x) ** 2 + (self.rect.y - entidade.rect.y) ** 2)) <= self.visao:
            if not self.falando:
                self.saudar()


class Villager(Npc):
    """Classe para representar um npc villager"""

    def __init__(self):
        Npc.__init__(self)
        # Pode se movimentar na distancia range em relacao a base
        self.range = 0, 0
        self.base = 0, 0
        self.vel = 5
        self.dir = '', 0, 0  # Indica em quanto ele vai andar em qual direcao
        self.esperando = 0  # Tempo idle
        self.atividade = 0.5  # Proporcao do quanto ele vai se movimentar
        self.image = imagens['Mago']['idle'][0]

        self.anim_rate = 0.033
        self.index, self.sector = 0, ''
        # Carregar as imagens
        self.rect = self.image.get_rect()

    def update(self):
        atividade = randint(1, 10)
        if atividade <= self.atividade * 10 and self.dir[1] <= 0:
            self.esperando = randint(0, 10) * self.atividade
            self.dir = '', 0, 0
        if self.esperando == 0 and self.dir[1] <= 0:
            self.andar()
        else:
            self.esperando -= 1 / fps
            if self.esperando <= 0:
                self.esperando = 0
        self.mover()

    def andar(self):
        """Faz ele andar aleatoriamente"""
        d = randint(0, 1)
        if d == 0:
            d = 'centerx'
            v = randint(0, self.base[0])
            sinal = choice([-1, 1])
            if abs(self.rect.centerx - self.base[0]) <= self.range[0]:
                sinal = -1
        else:
            d = 'centery'
            v = randint(0, self.base[1])
            sinal = choice([-1, 1])
            if abs(self.rect.centery - self.base[1]) <= self.range[1]:
                sinal = -1
        self.dir = d, v, sinal

    def mover(self):
        """A partir do vetor dir movimenta a entidade"""
        if self.dir[0] != '' and self.dir[1] > 0:
            setattr(getattr(self, 'rect'), self.dir[0], getattr(getattr(self, 'rect'), self.dir[0])
                    + (self.vel * self.dir[2]))
            self.dir = self.dir[0], self.dir[1] - self.vel, self.dir[2]


class Mercador(Npc):
    """Npc mercador, vende itens de seu inventário"""

    def __init__(self, pos):
        Npc.__init__(self)
        self.images = imagens['Mercador']
        self.sector = 'idle'
        self.index, self.anim_vel = 0, 0.5 / fps
        self.image = self.images[self.sector][0]
        self.nome = 'Nome'
        self.mercadorias = []
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos[0], pos[1]
        self.visao = 70
        self.fala = None

    def update(self):
        """Animações do npc"""
        if self.fala is not None:
            if len(self.fala.groups()) == 0 and self.sector == 'talk':
                # Parou de falar
                self.sector, self.index = 'idle', 0
                self.fala = None
                self.falando = False
        self.index += self.anim_vel
        if self.index >= len(self.images[self.sector]):
            self.index = 0
        self.image = self.images[self.sector][int(self.index)]

    def falar(self):
        """Abre o balão de fala"""
        texto = trad('ola viajante /<E> para interagir')
        self.fala = Balao((self.rect.x, self.rect.topleft[1]), texto)
        for grupo in self.groups()[1:]:
            grupo.add(self.fala)
        self.falando = True
        self.sector = 'talk'

    def proximidade(self, entidade):
        """Trigger de proximidade"""
        if abs(sqrt((self.rect.x - entidade.rect.x) ** 2 + (self.rect.y - entidade.rect.y) ** 2)) <= self.visao:
            if not self.falando:
                self.falar()
            elif self.falando and len(self.fala.groups()) == 0:
                self.falar()
