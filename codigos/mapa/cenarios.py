# Este arquivo gera e armazena os cenários do jogo
from codigos.variaveis import screen_size, cenarios_arq
from codigos.mapa.chao import Chao
import json


width, height = screen_size


def gerar_cenarios(cenarios, arq=cenarios_arq):
    """Recebe um dicionário, o preenche com os dados dos cenários lidos no json"""
    with open(arq, 'r') as json_file:
        data = json.load(json_file)
    for key in data:
        tupla = tuple(map(int, key.split()))
        try:
            if not data[key]['copia']['valor']:
                chao = Chao(data[key])
            else:
                data[key]['blocos'] = data[data[key]['copia']['fonte']]['blocos']
                chao = Chao(data[key])
                chao.copia = True
                fonte = data[key]['copia']['fonte'].split(' ')
                chao.fonte = f'{fonte[0]} {fonte[1]}'
            cenarios[tupla] = chao
            chao.acesso = data[key]['acesso']
            chao.lock = data[key]['lock']
            chao.background = data[key]['background']
        except Exception as e:
            print('[Erro] na criação do cenário', tupla[0], str(tupla[1]) + ':', e)
