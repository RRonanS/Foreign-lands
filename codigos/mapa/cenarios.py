# Este arquivo gera e armazena os cenários do jogo
from codigos.variaveis import screen_size
from codigos.mapa.chao import Chao
import json


width, height = screen_size


def gerar_cenarios(cenarios):
    with open('dados/cenarios_data.json', 'r') as json_file:
        data = json.load(json_file)
    for key in data:
        a = key.split()
        tupla = int(a[0]), int(a[1])
        try:
            if not data[key]['copia']['valor']:
                chao = Chao(data[key])
            else:
                data[key]['blocos'] = data[data[key]['copia']['fonte']]['blocos']
                chao = Chao(data[key])
            cenarios[tupla] = chao
            chao.acesso = data[key]['acesso']
            chao.lock = data[key]['lock']
            chao.background = data[key]['background']
        except Exception as e:
            print('[Erro] na criação do cenário', tupla[0], str(tupla[1]) + ':', e)
