from ..variaveis import fps, exp_mult
from random import randint
from codigos.entidades.monstros import Esqueleto, Cogumelo, Olho
from codigos.entidades.gerenciador_imagens import imagens

imagens = imagens['monstros']

# Adicionar limite de qntd viva

class Spawner(Esqueleto):
    """"Classe para representar um spawner de monstros"""
    def __init__(self, classe):
        Esqueleto.__init__(self)
        self.vida = self.vida_max = 350
        self.timer = 10  # Tempo em segundos para spawnar(Constante)
        self.remaining = self.timer  # Tempo restante até spawnar
        self.tipo = 'spawner'
        self.qtd = 1  # Quantidade que spawna por vez
        self.variaton_pos = 64, 64 # Variação dado o centro
        self.classe = classe # Classe do monstro a ser spawnado
        self.vel = 0
        self.images = imagens['spawner']
        self.exp = 500 * exp_mult
        self.coin_drop = (5, 10)

    def update_especifico2(self):
        """Override do método para chamar suas funcionalidades"""
        self.remaining = max(self.remaining - (1/fps), 0)
        self.flip = False

    def spawnar(self, grupo):
        """Gera os monstros e adiciona no grupo passado como parametro"""
        for i in range(self.qtd):
            monstro = self.classe()
            monstro.rect.center = self.rect.center
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
        self.reset_timer()

    def atacar(self):
        """Override do ataque da super, faz nada"""
        pass

    def reset_timer(self):
        """Reseta o tempo para spawnar"""
        self.remaining = self.timer

class Spawner_esqueleto(Spawner):
    """Spawner de esqueleto"""
    def __init__(self):
        Spawner.__init__(self, Esqueleto)
        self.qtd = 2
        self.timer = 10

class Spawner_cogumelo(Spawner):
    """Spawner de cogumelo"""
    def __init__(self):
        Spawner.__init__(self, Cogumelo)
        self.vida = self.vida_max = 700
        self.qtd = 2
        self.timer = 10
        self.exp = 1000 * exp_mult
        self.coin_drop = (20, 30)

class Spawner_olho(Spawner):
    """Spawner de olho"""
    def __init__(self):
        Spawner.__init__(self, Olho)
        self.vida = self.vida_max = 1000
        self.qtd = 5
        self.timer = 10
        self.exp = 2000 * exp_mult
        self.coin_drop = (20, 100)
