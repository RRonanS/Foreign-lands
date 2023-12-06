# Este arquivo inclui as funções geradoras das entidades do jogo
from .npcs import Mercador
from ..itens.itens import Pocao_vida, Pocao_vidaGrande
from ..outros.armazenamento import ler_inimigos
from ..variaveis import screen_size
from random import randint
import sys
width, height = screen_size
monstros = sys.modules['codigos.entidades.monstros']


def get_mercadores():
    """Gera os mercadores para o jogo"""
    m1 = Mercador((width*3.5, height//2))
    m1.mercadorias.append(Pocao_vida())
    m1.mercadorias.append(Pocao_vidaGrande())
    return [m1]


def get_npcs():
    """Gera os npcs do jogo"""
    return []
    #  return [Mago((width//2, height//2))]


def get_inimigos(inimigos):
    """Função para gerar os inimigos do jogo com base no json de inimigos lido"""
    gerador = ler_inimigos(boss=False)

    def aux(classe, cenario, pos=(-1, -1), radomize=False):
        """Função auxiliar para cliar um inimigo de tal classe em determinado cenario"""
        inimigo = classe()
        cenario = cenario[0], cenario[1]
        if pos == (-1, -1):
            inimigo.rect.centerx = randint(cenario[0] * width, (1 + cenario[0]) * width)
            inimigo.rect.centery = randint(cenario[1] * height, (1 + cenario[1]) * height)
        else:
            rx, ry = randint(int(0.1 * width), int(0.4 * width)), randint(int(0.1 * height), int(0.4 * height))
            inimigo.rect.centerx, inimigo.rect.centery = (width * (1 + cenario[0]) - pos[0]), \
                                                         (height * (1 + cenario[1]) - pos[1])
            if radomize:
                inimigo.rect.centerx += rx
                inimigo.rect.centery += ry
        inimigos.add(inimigo)

    for key in gerador:
        for item in gerador[key]:
            for i in range(item[2]):
                do_rand = False  # Evita que entidades spawnem coladas
                if item[2] > 1:
                    do_rand = True
                aux(getattr(monstros, key), item[0], item[1], do_rand)
