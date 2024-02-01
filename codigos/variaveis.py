# Variáveis de jogo
import json

screen_size = 704, 448
# Precisa implicar que alterar screen size altera char size  e block size
char_size = (96, 96)
block_size = 64, 64
tamanho_barra_itens = 0.3
dificuldade = 1
exp_mult = 1
exigencia_niveis = 0.7  # Define a taxa de aumento do custo de xp para subir de nivel
musica, efeitos, volume = False, False, 0.0
imortal = False
colide = True  # Se o personagem colide com entidades
colide_tolerancia = 32
info = True
load = False  # Se deve carregar os dados json ao iniciar
console = True  # Se deve dar acesso ao console de comandos do jogo

# Desempenho
fps = 30
update_range = (screen_size[0], screen_size[1])  # Distancia de atualizacao dos inimigos
draw_range = (screen_size[0], screen_size[1])  # Distancia de visao dos inimigos

# O quanto acrescenta ao por ponto em tal skill
acrescimos = {'vida': 5, 'dano': 2, 'velocidade': 2 * (30 / fps), 'sorte': 5, 'inteligencia': 10}

cenarios_arq = 'dados/cenarios_data.json'
monstros_arq = 'dados/monstros_data.json'

idioma = 'portugues'
versao = 0.21
devs = ['RRonan']
update = '23/10/2023'


def load_config():
    """Carrega dados do arquivo configuração"""
    global idioma, efeitos, musica, volume, load, fps, console, cenarios_arq, monstros_arq
    try:
        with open('dados/configuracao.json', 'r') as arq:
            data = json.load(arq)
            if data['idioma']:
                idioma = data['idioma']
            if data['sons']:
                if data['sons']['efeitos']:
                    efeitos = True
                else:
                    efeitos = False
                if data['sons']['musica']:
                    musica = True
                else:
                    musica = False
                if data['sons']['volume']:
                    volume = data['sons']['volume']
            if data['console']:
                console = data['console']
            else:
                console = False
            if data['fps']:
                fps = data['fps']
            if data['load_save']:
                load = True
            else:
                load = False
            if data['cenario_load']:
                cenarios_arq = data['cenario_load']
            if data['monstros_load']:
                monstros_arq = data['monstros_load']
    except:
        print('[Erro] Arquivo configuracao.json não encontrado na pasta dados')


load_config()
