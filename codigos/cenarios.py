# Este arquivo gera e armazena os cenários do jogo
from .chao import Chao
from .variaveis import screen_size, block_size

width, height = screen_size
cenarios = {}

cenario0 = Chao((0, width, height, height-block_size[0]), 2, 0)
cenario0.add_coluna(0)
cenario0.add_bloco((0, height), 5)

cenario1 = Chao((0, width, height, height-block_size[0]), 0, 0)
cenario1.add_linha(height-block_size[1]*2)

cenario2 = Chao((0, width, height, height-block_size[0]), 0, 0)
cenario2.add_bloco((0, height-block_size[0]), 0)

cenarios[0] = cenario0
cenarios[1] = cenario1
cenarios[2] = cenario2

