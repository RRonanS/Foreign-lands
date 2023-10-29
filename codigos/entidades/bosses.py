import random

import pygame.mask
from .monstros import Esqueleto, Executor
from ..variaveis import char_size, exp_mult, screen_size, fps
from random import randint
from codigos.entidades.gerenciador_imagens import imagens
from codigos.ambiente.sons import monstros_sounds

imagens = imagens['bosses']
sounds = monstros_sounds

width, height = screen_size


class Boss1(Esqueleto):
    """Boss esqueleto gigante"""
    def __init__(self):
        Esqueleto.__init__(self)

        self.tipo = 'boss'
        self.is_boss = True
        self.lock = 9, 0  # Cenario do boss a bloquear saida do player
        self.unlocks = []  # Cenarios a serem desbloqueados para acesso
        for x in range(5):  # Desbloqueia o canto superior direito do mapa
            for y in range(-5, 0):
                self.unlocks.append((x, y))

        self.vida, self.vida_max = 80, 80
        self.dano, self.peso = 8, 10
        self.vel, self.default_vel = 1, 1
        self.vel_boost, self.boost_time = 3, 20
        self.boost_left = 0
        self.exp = 500*exp_mult
        self.coin_drop = (30, 30)
        self.droprate = {'Pocao_vidaGrande': 0.50, 'Pocao_velocidade': 1}
        self.anim_mult = 0.25 * (30 / fps)

        self.images = imagens['boss1']
        self.sounds = sounds['boss1']

        self.mask = pygame.mask.from_surface(self.images['idle'][0])
        self.rect = self.images['idle'][0].get_rect()
        self.rect.bottomleft = (width//2, height)

    def update_especifico(self):
        if self.boost_left == 0:
            self.vel = self.default_vel
            if randint(1, 100) <= 2:
                self.vel = self.vel_boost
                self.boost_left = self.boost_time
        else:
            self.boost_left -= 1


class Boss2(Esqueleto):
    """Boss2, Executioner"""
    def __init__(self):
        Esqueleto.__init__(self)
        self.tipo = 'boss'
        self.is_boss = True

        self.spells_chance = 0.5  # Numero menor, menos chance do spell ser um summon
        self.spell_range = 2
        self.has_spell = True
        self.spelling = False
        self.spell_cooldown, self.spell_total = 0,  10 * fps
        self.spell_dmg = 10

        self.lock = 5, -5  # Cenario do boss a bloquear saida do player
        self.unlocks = []  # Cenarios a serem desbloqueados para acesso
        for x in range(-5, 0, 1):  # Desbloqueia o canto esquerdo do mapa
            for y in range(-5, 5, 1):
                self.unlocks.append((x, y))

        self.vida, self.vida_max = 200, 200
        self.dano, self.peso = 10, 20
        self.dano_critico = 15
        self.vel = 2
        self.visao = 0.25
        self.exp = 5000*exp_mult
        self.coin_drop = (100, 100)
        self.droprate = {'Pocao_vidaGrande': 1, 'Pocao_velocidade': 1, 'Pocao_dano': 1}
        self.anim_mult = 0.25 * (30 / fps)

        self.images = imagens['executioner']
        self.mask = pygame.mask.from_surface(self.images['idle'][0])
        self.rect = self.images['idle'][0].get_rect()

    def spell(self):
        """Funcao para lancar o spell, invoca um executor ou faz ataque especial"""
        if self.sector == 'summon':
            self.spell_cooldown = self.spell_total
            obj = Executor()
            obj.rect.centerx = random.choice([self.rect.topleft[0], self.rect.topright[0]])
            obj.rect.centery = random.choice([self.rect.topleft[1], self.rect.bottomleft[1]])
            grupos = self.groups()
            for grupo in grupos:
                grupo.add(obj)
        else:
            self.ataque = True
            self.ataque_critico = True
        self.sector, self.index, self.animar = 'idle', 0, True

    def update_especifico(self):
        """Update especifico do boss"""
        if (self.sector == 'summon' or self.sector == 'skill') \
                and self.index + self.anim_mult >= len(self.images[self.sector]):
            self.spell()
        self.spell_cooldown = max(0, self.spell_cooldown-1)

    def atacar(self):
        """Caso possível, executa um ataque ou lança spell"""
        if self.sector != 'attack' and self.animar:
            if self.spell_cooldown == 0:
                val = random.random()
                if val > self.spells_chance:
                    self.sector = 'summon'
                else:
                    self.sector = 'skill'
            else:
                self.sector = 'attack'
            self.animar = False


class Boss3(Esqueleto):
    """Boss3"""
    def __init__(self):
        Esqueleto.__init__(self)
        self.tipo = 'boss'
        self.is_boss = True

        self.lock = -8, 0  # Cenario do boss a bloquear saida do player
        self.unlocks = []  # Cenarios a serem desbloqueados para acesso

        self.vida, self.vida_max = 800, 800
        self.dano, self.peso = 14, 20
        self.dano_critico = 17
        self.vel = 2
        self.visao = 0.7
        self.exp = 10000*exp_mult
        self.coin_drop = (200, 300)
        self.droprate = {'Pocao_vida': 0.8, 'Pocao_vidaGrande': 0.50,
                         'Pocao_velocidade': 0.4, 'Pocao_dano': 0.40,
                         'Pocao_vidaGigante': 0.2, 'Pocao_regen': 0.3}
        self.anim_mult = 0.5 * (30 / fps)

        self.images = imagens['demon']
        self.mask = pygame.mask.from_surface(self.images['idle'][0])
        self.rect = self.images['idle'][0].get_rect()

    def update_especifico2(self):
        """Inverte o flip da imagem"""
        if self.sector == 'walk':
            if self.flip:
                self.flip = False
            else:
                self.flip = True


def boss_group(lis, ini, grupo):
    """Recebe a lista de sprites, a lista de inimigos e gera os bosses do jogo"""
    boss1 = Boss1()
    boss1.rect.centerx = int(width*9.5)
    boss1.rect.centery = height//2

    boss2 = Boss2()
    boss2.rect.centerx = int(width*5.5)
    boss2.rect.centery = -height*4.5

    boss3 = Boss3()
    boss3.rect.centerx = int(-1*width*7.5)
    boss3.rect.centery = height//2

    grupo.add(boss1)
    lis.add(boss1)
    ini.add(boss1)

    grupo.add(boss2)
    lis.add(boss2)
    ini.add(boss2)

    grupo.add(boss3)
    lis.add(boss3)
    ini.add(boss3)
