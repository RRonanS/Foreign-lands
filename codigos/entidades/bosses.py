import pygame.mask
from .monstros import Esqueleto
from ..variaveis import char_size, exp_mult, screen_size
from random import randint


width, height = screen_size


class Boss1(Esqueleto):
    """Boss esqueleto gigante"""
    def __init__(self):
        Esqueleto.__init__(self)
        self.tipo = 'boss'
        self.is_boss = True
        self.lock = 9, 0 # Cenario do boss a bloquear saida do player
        self.unlocks = [(-1, 0)] # Cenarios a serem desbloqueados para acesso

        self.vida, self.vida_max = 75, 75
        self.dano, self.peso = 7, 10
        self.vel, self.default_vel = 1, 1
        self.vel_boost, self.boost_time = 3, 20
        self.boost_left = 0
        self.exp = 200*exp_mult
        self.coin_drop = (5, 10)
        size = int(char_size[0]*1.5), int(char_size[1]*1.5)
        for sec in self.images:
            for x in range(len(self.images[sec])):
                self.images[sec][x] = pygame.transform.scale(self.images[sec][x], size).convert_alpha()
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


def boss_group(lis, ini, grupo):
    """Recebe a lista de sprites, a lista de inimigos e gera os bosses do jogo"""
    boss1 = Boss1()
    boss1.rect.centerx = int(width*9.5)
    boss1.rect.centery = height//2
    grupo.add(boss1)
    lis.add(boss1)
    ini.add(boss1)
