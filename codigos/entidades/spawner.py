from ..variaveis import fps
from pygame.sprite import Group
from random import randint


class Spawner:
    """"Classe para representar um spawner de monstros"""
    def __init__(self, classe):
        self.timer = 0 # Tempo em segundos para spawnar
        self.remaining = self.timer
        self.monster = None
        self.qtd = 0
        self.spawn_pos = 0, 0 # Centro do spawn
        self.variaton_pos = 0, 0 # Variação dado o centro
        self.classe = classe # Classe do monstro

    def update(self):
        """"Executa o processo do spawner"""
        if self.remaining <= 0:
            self.remaining = self.timer
            self.spawnar()
        else:
            self.remaining -= 1/fps

    def spawnar(self):
        """"Gera as entidades no jogo"""
        grupo = Group()
        for i in range(self.qtd):
            monstro = self.classe()
            monstro.rect.center = self.spawn_pos
            grupo.add(monstro)
            s1, s2 = randint(0, 1), randint(0, 1)
            dx, dy = randint(0, self.variaton_pos[0]), randint(0, self.variaton_pos[1])
            if s1 == 0:
                monstro.rect.centerx += dx
            else:
                monstro.rect.centerx -= dx
            if s2 == 0:
                monstro.rect.centery += dy
            else:
                monstro.rect.centery -= dy
        return grupo
