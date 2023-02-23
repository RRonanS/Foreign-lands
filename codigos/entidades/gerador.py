# Este arquivo inclui as funções geradoras das entidades do jogo
from .npcs import Mercador, Mago
from ..itens.itens import Pocao_vida
from ..variaveis import screen_size, char_size
from random import randint
import sys
width, height = screen_size
monstros = sys.modules['codigos.entidades.monstros']


def get_mercadores():
    """Gera os mercadores para o jogo"""
    m1 = Mercador((width*3.5, height//2))
    m1.mercadorias.append(Pocao_vida())
    return [m1]


def get_npcs():
    """Gera os npcs do jogo"""
    return [Mago((width//2, height//2))]


def get_inimigos(inimigos):
    """Função para gerar os inimigos do jogo"""
    gerador = {'Esqueleto':
                   [[(1, 0), (width // 2, height - char_size[1]), 1],
                    [(2, 0), (width // 2, height - char_size[1]), 1],
                    [(3, 0), (width // 2, height - char_size[1]), 2],
                    [(4, 0), (width // 2, height - char_size[1]), 3],
                    [(5, 0), (width // 2, height - char_size[1]), 4],
                    [(6, 0), (width // 2, height - char_size[1]), 3],
                    [(7, 0), (width // 2, height - char_size[1]), 4],
                    [(8, 0), (width // 2, height - char_size[1]), 3],
                    [(0, 1), (width // 2, height - char_size[1]), 1],
                    [(0, -1), (width // 2, height - char_size[1]), 1],
                    [(1, 1), (width // 2, height - char_size[1]), 2],
                    [(-1, 1), (width // 2, height - char_size[1]), 2],
                    [(-1, -1), (width // 2, height - char_size[1]), 2]],
               'Olho':
                   [[(3, 0), (width // 2, height - char_size[1]), 1],
                    [(5, 0), (width // 2, height - char_size[1]), 2],
                    [(7, 0), (width // 2, height - char_size[1]), 2],
                    [(2, 2), (width // 2, height - char_size[1]), 1],
                    [(-2, 2), (width // 2, height - char_size[1]), 1],
                    [(2, -2), (width // 2, height - char_size[1]), 1],
                    [(-2, -2), (width // 2, height - char_size[1]), 2]],
               'Goblin':
                   [[(5, 0), (width // 2, height - char_size[1]), 1],
                    [(8, 0), (width // 2, height - char_size[1]), 2]
                    ],
               'Cogumelo':
                   [[(0, 1), (-1, -1), 4],
                    [(0, 2), (width // 2, height - char_size[1]), 5],
                    [(1, 1), (width // 2, height - char_size[1]), 2],
                    [(-1, 1), (width // 2, height - char_size[1]), 2],
                    [(-1, -1), (width // 2, height - char_size[1]), 2]]
               }

    def aux(classe, cenario, pos=(-1, -1)):
        """Função auxiliar para cliar um inimigo de tal classe em determinado cenario"""
        inimigo = classe()
        cenario = cenario[0], -1 * cenario[1]
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
