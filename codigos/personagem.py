import pygame.sprite
from .auxiliares import img_load
from .variaveis import char_size, exigencia_niveis, efeitos
from .sons import espadas, levelup
from random import choice


class Personagem(pygame.sprite.Sprite):
    '''Objeto para representar o personagem do jogo'''
    class sprite_espada(pygame.sprite.Sprite):
        '''Classe para representar a posição da espada do personagem, sendo chamada
        apenas durante ataques'''
        def __init__(self, player_pos, images, flip):
            pygame.sprite.Sprite.__init__(self)
            self.image = images[0]
            self.rect = self.image.get_rect()
            self.rect = player_pos
            if flip:
                self.mask = pygame.mask.from_surface(pygame.transform.flip(
                    images[1], True, False))
            else:
                self.mask = pygame.mask.from_surface(images[1])

    def __init__(self, height):
        self.height = height
        dir = 'arquivos/imagens/Knight/'
        pygame.sprite.Sprite.__init__(self)

        # Variáveis gerais
        self.niveis = [0, 15]
        for i in range(2, 30):
            self.niveis.append(self.niveis[i-1]*exigencia_niveis)
        self.nivel = 1
        self.vel = 7
        self.pulo_altura = 50
        self.vida_max, self.vida = 10, 10
        self.dano = 5
        self.animar_freq = 0.3
        self.coins, self.pontos, self.sorte, self.exp = 0, 0, 0, 0

        # Armazenamento das imagens do personagem
        self.images = {'idle': [], 'run': [], 'attack': [], 'jump': [],
                       'jump_fall': []}
        idle = pygame.image.load(dir+'_Idle.png')
        run = pygame.image.load(dir+'_Run.png')
        attack = pygame.image.load(dir+'_Attack.png')
        jump = pygame.image.load(dir+'_Jump.png')
        jump_fall = pygame.image.load(dir+'_JumpFallInbetween.png')
        death = pygame.image.load(dir+'_Death.png')
        foot = pygame.image.load(dir+'-foot.png')
        self.images['idle'] = img_load(idle, (120, 80), char_size)
        self.images['run'] = img_load(run, (120, 80), char_size)
        self.images['attack'] = img_load(attack, (120, 80), char_size)
        self.images['jump'] = img_load(jump, (120, 80), char_size)
        self.images['jump_fall'] = img_load(jump_fall, (120, 80), char_size)
        self.images['death'] = img_load(death, (120, 80), char_size)
        self.images['foot'] = img_load(foot, (120, 80), char_size)

        # Varíaveis de funcionamento
        self.index = 0
        self.sector = 'idle'
        self.animar = True
        self.flip = False
        self.ataque = False
        self.pulo_atual = 0
        self.pulo, self.descida = False, False
        self.mask = pygame.mask.from_surface(self.images['idle'][0])
        self.image = self.images[self.sector][self.index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, height-10)

    def correr(self):
        '''Faz a animação do personagem correndo'''
        if self.sector != 'run' and self.animar:
            self.sector, self.index = 'run', 0

    def idle(self):
        '''Faz animação do personagem parado'''
        if self.sector != 'idle' and self.animar:
            self.sector, self.index = 'idle', 0

    def attack(self):
        '''Se possível, faz o personagem atacar'''
        if self.sector != 'attack' and self.animar:
            if efeitos:
                choice(espadas).play()
            self.sector, self.index = 'attack', 0
            self.animar = False

    def pular(self):
        '''Faz o personagem executar um pulo'''
        if not self.pulo and not self.descida and self.animar:
            self.pulo = True
            self.sector = 'jump'

    def upar(self):
        '''Se possível, aumenta o nível do personagem'''
        while self.exp >= self.niveis[self.nivel]:
            if efeitos:
                levelup.play()
            self.exp -= self.niveis[self.nivel]
            self.nivel += 1
            self.vida = self.vida_max
            self.pontos += 1

    def sprite_ataque(self):
        return self.sprite_espada(self.rect, self.images['attack'], self.flip)

    def update(self):
        if self.vida <= 0:
            self.animar = False
            self.sector = 'death'
        # Parte responsável pela animação do personagem
        self.index += self.animar_freq
        if self.index >= len(self.images[self.sector]):
            self.index = 0
            if self.sector == 'attack':
                self.sector = 'idle'
                self.animar = True
                self.ataque = True
            if self.pulo and self.descida:
                self.sector = 'jump_fall'
            if self.sector == 'jump_fall' and not self.descida:
                self.sector = 'idle'
            if self.sector == 'jump' and not self.pulo:
                self.sector = 'idle'
            if self.sector == 'death':
                self.animar = False
                self.animar_freq, self.vel, self.dano = 0, 0, 0
                self.index = len(self.images['death'])-1
        if self.pulo:
            if not self.descida:
                self.pulo_atual += self.vel
                self.rect.y -= self.vel
            else:
                if self.pulo_atual <= 0 and self.descida:
                    self.descida, self.pulo = False, False
                self.rect.y += self.vel
                self.pulo_atual -= self.vel
            if self.pulo_altura <= self.pulo_atual:
                self.descida = True
        if self.flip:
            img = pygame.transform.flip(self.images[self.sector][int(self.index)],
                                        True, False)
        else:
            img = self.images[self.sector][int(self.index)]
        self.image = img
