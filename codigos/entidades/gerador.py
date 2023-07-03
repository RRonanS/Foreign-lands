# Este arquivo inclui as funções geradoras das entidades do jogo
from .npcs import Mercador, Mago
from ..itens.itens import Pocao_vida, Pocao_vidaGrande
from ..variaveis import screen_size, char_size
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
    """Função para gerar os inimigos do jogo"""
    gerador = {'Esqueleto':
                   [[(1, 0), (width // 2, height - char_size[1]), 2],
                    [(2, 0), (width // 2, height - char_size[1]), 3],
                    [(3, 0), (width // 2, height - char_size[1]), 5],
                    [(4, 0), (width // 2, height - char_size[1]), 7],
                    [(5, 0), (width // 2, height - char_size[1]), 10]],
               'Olho':
                   [[(3, 0), (width // 2, height - char_size[1]), 1],
                    [(5, 0), (width // 2, height - char_size[1]), 2],
                    [(6, 0), (width // 2, height - char_size[1]), 5],
                    [(7, 0), (width // 2, height - char_size[1]), 5],
                    [(4, -1), (width // 2, height - char_size[1]), 3],
                    [(5, -1), (width // 2, height - char_size[1]), 3],
                    [(0, -2), (width // 2, height - char_size[1]), 5],
                    [(1, -2), (width // 2, height - char_size[1]), 5],
                    [(2, -2), (width // 2, height - char_size[1]), 5],
                    [(3, -2), (width // 2, height - char_size[1]), 5],
                    [(4, -2), (width // 2, height - char_size[1]), 5],
                    [(5, -2), (width // 2, height - char_size[1]), 5]
                    ],
               'Goblin':
                   [[(6, 0), (width // 2, height - char_size[1]), 2],
                    [(7, 0), (width // 2, height - char_size[1]), 3],
                    [(8, 0), (width // 2, height - char_size[1]), 4]
                    ],
               'Cogumelo':
                   [
                    [(0, -1), (-1, -1), 3],
                    [(1, -1), (-1, -1), 3],
                    [(2, -1), (-1, -1), 3],
                    [(3, -1), (-1, -1), 3],
                    [(4, -1), (-1, -1), 3],
                    [(5, -1), (-1, -1), 3],
                    [(0, -2), (-1, -1), 5],
                    [(1, -2), (-1, -1), 5],
                    [(2, -2), (-1, -1), 5],
                    [(3, -2), (-1, -1), 5],
                    [(4, -2), (-1, -1), 5],
                    [(5, -2), (-1, -1), 5],
                    [(0, -3), (-1, -1), 7],
                    [(1, -3), (-1, -1), 7],
                    [(2, -3), (-1, -1), 7],
                    [(3, -3), (-1, -1), 7],
                    [(4, -3), (-1, -1), 7],
                    [(5, -3), (-1, -1), 7],
                   ],
               'BringerDeath':
               [
                   [(0, -5), (-1, -1), 1],
                   [(1, -5), (-1, -1), 1],
                   [(2, -5), (-1, -1), 1],
                   [(3, -5), (-1, -1), 1],
                   [(4, -5), (-1, -1), 1],
               ]
               }

    def aux(classe, cenario, pos=(-1, -1)):
        """Função auxiliar para cliar um inimigo de tal classe em determinado cenario"""
        inimigo = classe()
        cenario = cenario[0], cenario[1]
        if pos == (-1, -1):
            inimigo.rect.centerx = randint(cenario[0] * width, (1 + cenario[0]) * width)
            inimigo.rect.centery = randint(cenario[1] * height, (1 + cenario[1]) * height)
        else:
            r = randint(0, width // 2)
            inimigo.rect.centerx, inimigo.rect.centery = (width * (1 + cenario[0]) - pos[0]) + r, (
                        (1 + cenario[1]) * pos[1])
        inimigos.add(inimigo)

    for key in gerador:
        for item in gerador[key]:
            for i in range(item[2]):
                aux(getattr(monstros, key), item[0], item[1])
