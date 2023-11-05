# Esse arquivo escreve os dados de um dicionário no json de monstros
import json
from random import randint
import jsbeautifier
from codigos.variaveis import screen_size, char_size

width, height = screen_size
options = jsbeautifier.default_options()
options.indent_size = 2
options.max_preserve_newlines = True

gerador = {'Esqueleto':
               [[(1, 0), (-1, -1), 2],
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
               ],
           "Lobo":
               [
                    [(-1, 0), (width // 2, height // 2), 3],
                    [(-1, -1), (width // 2, height // 2), 3],
                    [(-1, 1), (width // 2, height // 2), 3]
               ],
           "Golem":
               [
                    [(-3, 0), (-1, -1), 2],
                    [(-3, 1), (-1, -1), 2],
                    [(-3, -1), (-1, -1), 2],
               ],
           'Boss1':
               [
                   [(9, 0), (width // 2, height // 2), 1, True]
               ],
           'Boss2':
               [
                   [(5, -5), (width // 2, height // 2), 1, True]
               ],
           'Boss3':
               [
                   [(-8, 0), (width // 2, height // 2), 1, True]
               ]
           }

inimigos = {}
cont = 1

for key in gerador:
    for item in gerador[key]:
        qtd = item[2]
        if item[1][0] == -1:
            p_x = randint(0, width)
        else:
            p_x = item[1][0]
        if item[1][1] == -1:
            p_y = randint(0, height)
        else:
            p_y = item[1][1]
        pos = (item[0][0] * width) + p_x, (item[0][1] * height) + p_y
        inimigos[str(cont)] = {
            "pos": [pos[0], pos[1]],
            "tipo": key,
            "quantidade": qtd
        }
        if len(item) > 3:
            inimigos[str(cont)]['boss'] = item[3]
        cont += 1
data = {
    "inimigos": inimigos
}

print('[Jogo] Escrevendo monstros base no arquivo dados/monstros_data.json')
with open('dados/monstros_data.json', 'w') as arq:
    arq.write((jsbeautifier.beautify(json.dumps(data), options)))
