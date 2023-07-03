# Variáveis de jogo
screen_size = 704, 448
# Precisa implicar que alterar screen size altera char size  e block size
char_size = (96, 96)
block_size = 64, 64
tamanho_barra_itens = 0.3
dificuldade = 1
exp_mult = 1
exigencia_niveis = 0.7  # Define a taxa de aumento do custo de xp para subir de nivel
musica, efeitos, volume = True, True, 0.3
imortal = False
colide = True  # Se o personagem colide com entidades
colide_tolerancia = 32
info = True
load = True  # Se deve carregar os dados json ao iniciar
console = True  # Se deve dar acesso ao console de comandos do jogo

# Desempenho
fps = 30
update_range = (screen_size[0], screen_size[1])  # Distancia de atualizacao dos inimigos
draw_range = (screen_size[0], screen_size[1])  # Distancia de visao dos inimigos

# O quanto acrescenta ao por ponto em tal skill
acrescimos = {'vida': 5, 'dano': 2, 'velocidade': 2 * (30 / fps), 'sorte': 5}

idioma = 'portugues'
versao = 0.2
devs = ['RRonan']
update = '03/07/2023'
