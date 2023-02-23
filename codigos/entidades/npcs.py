from math import sqrt
from random import randint, choice
import pygame.sprite
from codigos.ambiente.textuais import fonte1, preto, branco
from codigos.variaveis import screen_size, fps
from codigos.outros.auxiliares import img_load

width, height = screen_size
text_size = 20, 20
cara = 40  # Max caracteres por linha(so funciona com auto)
m_item = 3  # Max colunas por fala(so funciona com auto)

imagens = {
    'Mago': {
        'idle':
            img_load(pygame.image.load('arquivos/imagens/mago/Idle.png').convert_alpha(), (48, 48), (48, 48)),
        'walk':
            img_load(pygame.image.load('arquivos/imagens/mago/Walk.png').convert_alpha(), (48, 48), (48, 48)),
        'special':
            img_load(pygame.image.load('arquivos/imagens/mago/Special.png').convert_alpha(), (48, 48), (48, 48))
    },
    'Mercador':{
        'idle':
            None
            #img_load(pygame.image.load('arquivos/imagens/mercador/mercador.png').convert_alpha(), (48, 48), (48, 48))
    }
}


class Balao(pygame.sprite.Sprite):
    """Classe para representar um balão de fala"""

    def __init__(self, pos, texto, auto=False):
        r"""Recebe a posição do balão, o texto a ser mostrado e se deve
        automaticamente quebrar o texto. Formatos textuais:
        / indica quebra de frase e \ quebra de linha"""
        pygame.sprite.Sprite.__init__(self)
        self.textos = []
        self.tipo = 'balao'

        # Quebra do texto em partes
        if auto:
            item = []
            for i in range(0, len(texto), cara):
                item.append(texto[i:min(i + cara, len(texto) - 1) + 1])
                if len(item) >= m_item:
                    self.textos.append(item)
                    item = []
        else:
            i, j = 0, 0
            item = []
            for j in range(len(texto)):
                if texto[j] == '/':
                    item.append(texto[i:j])
                    self.textos.append(item)
                    item = []
                    i = j + 1
                if texto[j] in r'\'':
                    item.append(texto[i:j])
                    i = j + 1
            try:
                self.textos.append([texto[i:j + 1]])
            except:
                pass

        self.anim_val = 0.015 * (30 / fps)
        self.pos = pos
        self.font = fonte1
        self.i, self.timer, self.t_i, self.w, self.h = 0, 0, 0, 0, 0
        self.surfaces = []
        for x in self.textos[self.t_i]:
            textSurf = self.font.render(x, 1, preto, branco)
            self.w = max(self.w, textSurf.get_width())
            self.h += textSurf.get_height()
            self.surfaces.append(textSurf)
        self.image = pygame.Surface((self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos

    def update(self):
        """Exibição do texto por tempo determinado"""
        self.timer += self.anim_val
        self.image.fill(branco)
        if self.timer >= 1:
            self.timer = 0
            self.t_i += 1
            if self.t_i >= len(self.textos):
                self.kill()
            else:
                self.surfaces, self.w, self.h = [], 0, 0
                for x in self.textos[self.t_i]:
                    textSurf = self.font.render(x, 1, preto, branco)
                    self.w = max(self.w, textSurf.get_width())
                    self.h += textSurf.get_height()
                    self.surfaces.append(textSurf)
                self.image = pygame.Surface((self.w, self.h))
                self.rect = self.image.get_rect()
                self.rect.bottomleft = self.pos
        for i in range(len(self.surfaces)):
            self.image.blit(self.surfaces[i], [0, i * (self.h // len(self.surfaces))])


class Npc(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = {}
        self.tipo = 'npc'
        self.nivel = 1
        self.vida, self.vida_max = 1, 1
        self.falando = False
        self.visao = 200

    def proximidade(self, entidade):
        """Trigger de proximidade"""
        pass


class Mago(Npc):
    def __init__(self, pos):
        Npc.__init__(self)
        self.anim_rate = 0.2 * (30 / fps)
        self.vida, self.vida_max = 100, 100
        self.nivel = 30
        self.visao = 100
        self.speed = 5 * (30 / fps)
        self.status = 'idle'
        self.cont = 0
        self.images['idle'] = imagens['Mago']['idle']
        self.images['walk'] = imagens['Mago']['walk']
        self.images['special'] = imagens['Mago']['special']

        self.image = self.images[self.status][self.cont]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos
        self.fala = Balao((0, 0), '')
        self.falando = False

    def update(self):
        self.cont += self.anim_rate
        if self.cont >= len(self.images[self.status]):
            self.cont = 0

        if self.falando and len(self.fala.groups()) == 0:
            # Ou seja, a fala acabou, ande ate sumir
            if self.status == 'special' and self.cont == 0:
                self.status = 'walk'
            elif self.status != 'walk':
                self.status = 'special'
            if self.status == 'walk':
                self.rect.x += self.speed
            if self.rect.bottomleft[0] >= width:
                self.kill()

        self.image = self.images[self.status][int(self.cont)]

    def saudar(self):
        texto = 'Olá viajante,\sabe onde está?' \
                r'/Está onde outrora fora\a terra sagrada' \
                '/Porém as trevas veem tomando\conta do nosso paraiso' \
                '/Tome cuidado para não\ser mais uma de suas vítimas' \
                '/Ande sempre pela luz'
        self.fala = Balao((self.rect.x, self.rect.topleft[1] + 10), texto)
        for grupo in self.groups()[1:]:
            grupo.add(self.fala)
        self.falando = True

    def proximidade(self, entidade):
        """Trigger de proximidade"""
        if abs(sqrt((self.rect.x - entidade.rect.x) ** 2 + (self.rect.y - entidade.rect.y) ** 2)) <= self.visao:
            if not self.falando:
                self.saudar()


class Villager(Npc):
    """Classe para representar um npc villager"""

    def __init__(self, pos):
        Npc.__init__(self)
        # Pode se movimentar na distancia range em relacao a base
        self.range = 0, 0
        self.base = 0, 0
        self.vel = 5
        self.dir = '', 0, 0  # Indica em quanto ele vai andar em qual direcao
        self.esperando = 0  # Tempo idle
        self.atividade = 0.5  # Proporcao do quanto ele vai se movimentar
        self.image = imagens['Mago']['idle'][0]

        self.anim_rate = 0.033
        self.index, self.sector = 0, ''
        # Carregar as imagens
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        atividade = randint(1, 10)
        if atividade <= self.atividade * 10 and self.dir[1] <= 0:
            self.esperando = randint(0, 10) * self.atividade
            self.dir = '', 0, 0
        if self.esperando == 0 and self.dir[1] <= 0:
            self.andar()
        else:
            self.esperando -= 1 / fps
            if self.esperando <= 0:
                self.esperando = 0
        self.mover()
        # Anime e faça se mover

    def andar(self):
        """Faz ele andar aleatoriamente"""
        d = randint(0, 1)
        if d == 0:
            d = 'centerx'
            v = randint(0, self.base[0])
            sinal = choice([-1, 1])
            if abs(self.rect.centerx - self.base[0]) <= self.range[0]:
                sinal = -1
        else:
            d = 'centery'
            v = randint(0, self.base[1])
            sinal = choice([-1, 1])
            if abs(self.rect.centery - self.base[1]) <= self.range[1]:
                sinal = -1
        self.dir = d, v, sinal

    def mover(self):
        """A partir do vetor dir movimenta a entidade"""
        if self.dir[0] != '' and self.dir[1] > 0:
            setattr(getattr(self, 'rect'), self.dir[0], getattr(getattr(self, 'rect'), self.dir[0])
                    + (self.vel * self.dir[2]))
            self.dir = self.dir[0], self.dir[1] - self.vel, self.dir[2]


class Mercador(Npc):
    def __init__(self, pos):
        Npc.__init__(self)
        self.image = imagens['Mago']['idle'][0]
        self.nome = 'Nome'
        self.mercadorias = []
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.visao = 70

    def update(self):
        pass

    def falar(self):
        texto = 'E'
        self.fala = Balao((self.rect.x, self.rect.topleft[1] + 10), texto)
        for grupo in self.groups()[1:]:
            grupo.add(self.fala)
        self.falando = True

    def proximidade(self, entidade):
        """Trigger de proximidade"""
        if abs(sqrt((self.rect.x - entidade.rect.x) ** 2 + (self.rect.y - entidade.rect.y) ** 2)) <= self.visao:
            if not self.falando:
                # self.falar()
                pass
            elif self.falando and len(self.fala.groups()) == 0:
                # self.falar()
                pass


"""
Mercador:
    Npc estático(ou móvel) que quando o player estiver proximo dele emite 
    uma mensagem indicando uma tecla X a ser pressionada. Quando o jogador 
    pressionar X, abre uma tela com os itens que o mercador vende
    Itens:
        Objetos que podem ser adquiridos pelo jogador em troca de moedas
        Quais itens adiciono?
    
"""
