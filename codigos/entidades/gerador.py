# Este arquivo inclui as funções geradoras das entidades do jogo
from .npcs import Mercador, Mago
from ..itens.itens import Pocao_vida, Pocao_vidaGrande, Pocao_dano, Pocao_vidaGigante, \
    Pocao_regen, Pocao_velocidade
from ..outros.armazenamento import ler_inimigos
from ..variaveis import screen_size
from random import randint
from codigos.entidades import spawner
import sys

width, height = screen_size

monstros = sys.modules['codigos.entidades.monstros']


def get_mercadores():
    """Gera os mercadores para o jogo"""
    m1 = Mercador((width*3.5, height//2))
    m1.mercadorias.append(Pocao_vida())
    m1.mercadorias.append(Pocao_vidaGrande())

    m2 = Mercador((width * -0.20, height * -1.5))
    m2.mercadorias.append(Pocao_vidaGrande())
    m2.mercadorias.append(Pocao_vidaGigante())
    m2.mercadorias.append(Pocao_regen())
    m2.mercadorias.append(Pocao_dano())

    m3 = Mercador((width * -4.2, height * -4.5))
    m3.mercadorias.append(Pocao_velocidade())
    m3.mercadorias.append(Pocao_vidaGigante(valor=25))
    m3.mercadorias.append(Pocao_dano(valor=60))
    return [m1, m2, m3]


def get_npcs():
    """Gera os npcs do jogo"""
    return [Mago((width//2, height//2))]


def get_inimigos(inimigos):
    """Função para gerar os inimigos do jogo com base no json de inimigos lido"""
    gerador = ler_inimigos(boss=False)

    def aux(classe, cenario, pos=(-1, -1), randomize=False):
        """Função auxiliar para criar um inimigo de tal classe em determinado cenario"""
        inimigo = classe()
        cenario = cenario[0], cenario[1]
        if pos == (-1, -1):
            inimigo.rect.centerx = randint((cenario[0] * width)+inimigo.rect.w, ((1 + cenario[0]) * width)-inimigo.rect.w)
            inimigo.rect.centery = randint((cenario[1] * height)+(inimigo.rect.h), ((1 + cenario[1]) * height) - (inimigo.rect.h))
        else:
            rx, ry = randint(int(0.1 * width), int(0.4 * width)), randint(int(0.1 * height), int(0.4 * height))
            inimigo.rect.centerx, inimigo.rect.centery = (width * (1 + cenario[0]) - pos[0]), \
                                                         (height * (1 + cenario[1]) - pos[1])
            if randomize:
                inimigo.rect.centerx += rx
                inimigo.rect.centery += ry
            # Correção de posição fora da tela
            inimigo.rect.centery = min((height * (1 + cenario[1])) - inimigo.rect.h//2, inimigo.rect.centery)
            inimigo.rect.centery = max(inimigo.rect.centery, (height * (cenario[1])))
            inimigo.rect.centerx = min(inimigo.rect.centerx, (width * (1 + cenario[0]))-inimigo.rect.w//2)
            inimigo.rect.centerx = max(inimigo.rect.centerx, width * cenario[0])
        inimigos.add(inimigo)

    for key in gerador:
        for item in gerador[key]:
            for i in range(item[2]):
                do_rand = False  # Evita que entidades spawnem coladas
                if item[2] > 1:
                    do_rand = True
                if key.startswith('Spawner'):
                    aux(getattr(spawner, key), item[0], item[1], do_rand)
                else:
                    aux(getattr(monstros, key), item[0], item[1], do_rand)
