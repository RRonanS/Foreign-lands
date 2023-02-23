import pygame.sprite
from ..outros.auxiliares import img_load
from ..variaveis import char_size, exigencia_niveis, efeitos, fps, screen_size
from ..ambiente.sons import espadas, levelup
from random import choice


width, height = screen_size


class Personagem(pygame.sprite.Sprite):
    """Objeto para representar o personagem do jogo"""
    class sprite_espada(pygame.sprite.Sprite):
        """Classe para representar a posição da espada do personagem, sendo chamada
        apenas durante ataques"""
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

    def __init__(self, pos):
        width, height = pos
        self.height, self.width = width, height
        dir = 'arquivos/imagens/Knight/'
        pygame.sprite.Sprite.__init__(self)

        # Variáveis gerais
        self.niveis = [0, 15]
        for i in range(2, 50):
            self.niveis.append(self.niveis[i-1]*exigencia_niveis)
        self.nivel = 1
        self.inventario = []
        self.tipo = 'personagem'
        self.vel = 7 * (30/fps)
        self.acesso = []
        self.desbloqueio = []
        self.pulo_altura = 50
        self.diag_nerf = 1.5
        self.vida_max, self.vida = 10, 10
        self.dano = 5
        self.animar_freq = 0.3 * (30/fps)
        self.coins, self.pontos, self.sorte, self.exp = 100, 0, 0, 0

        # Armazenamento das imagens do personagem
        self.images = {'idle': [], 'run': [], 'attack': [], 'jump': [],
                       'jump_fall': []}
        idle = pygame.image.load(dir+'_Idle.png').convert_alpha()
        run = pygame.image.load(dir+'_Run.png').convert_alpha()
        attack = pygame.image.load(dir+'_Attack.png').convert_alpha()
        jump = pygame.image.load(dir+'_Jump.png').convert_alpha()
        jump_fall = pygame.image.load(dir+'_JumpFallInbetween.png').convert_alpha()
        death = pygame.image.load(dir+'_Death.png').convert_alpha()
        foot = pygame.image.load(dir+'-foot.png').convert_alpha()
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
        self.rect.bottomleft = (width, height-10)

    def correr(self):
        """Faz a animação do personagem correndo"""
        if self.sector != 'run' and self.animar:
            self.sector, self.index = 'run', 0

    def idle(self):
        """Faz animação do personagem parado"""
        if self.sector != 'idle' and self.animar:
            self.sector, self.index = 'idle', 0

    def attack(self):
        """Se possível, faz o personagem atacar"""
        if self.sector != 'attack' and self.animar:
            if efeitos:
                choice(espadas).play()
            self.sector, self.index = 'attack', 0
            self.animar = False

    def pular(self):
        """Faz o personagem executar um pulo"""
        if not self.pulo and not self.descida and self.animar:
            self.pulo = True
            self.sector = 'jump'

    def upar(self):
        """Se possível, aumenta o nível do personagem"""
        while self.exp >= self.niveis[self.nivel]:
            if efeitos:
                levelup.play()
            self.exp -= self.niveis[self.nivel]
            self.nivel += 1
            self.vida = self.vida_max
            self.pontos += 1

    def sprite_ataque(self):
        """Retorna a sprite utilizada no calculo de colisoes"""
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

    def mover(self, dir, ver_func, ver_func2):
        """Função para movimentação do personagem, recebe o vetor dir
        a função de verificação do chão e a função de verificação de bloqueio,
        retorna qual, se houver, mudança deve ser feito nos cenarios"""
        if self.animar:
            if dir[0] == 0:
                mod = ['centerx']
            elif dir[0] == 1:
                mod = ['centery']
            elif dir[0] == 2:
                mod = ('centerx', 'centery')
                dir = dir[0], dir[1]//self.diag_nerf, dir[2]//self.diag_nerf
            else:
                return None
            cont = 1
            for x in mod:
                # Atualiza posição
                setattr(getattr(self, 'rect'), x, getattr(getattr(self, 'rect'), x) + dir[cont])
                cont += 1
            if not(ver_func(self.rect.center)) or ver_func2(self.rect):
                # Nova posição inválida, retorna
                cont = 1
                for x in mod:
                    setattr(getattr(self, 'rect'), x, getattr(getattr(self, 'rect'), x) - dir[cont])
                    cont += 1
            self.correr()
            if dir[1] <= 0:
                self.flip = True
            else:
                self.flip = False
            # Retorno da mudança de cenario
            if self.rect.center[0] < 0:
                return 0, -1
            elif self.rect.topleft[1] < 0:
                # 96 < BL < height
                return 1, -1
            elif self.rect.bottomright[0] > width:
                return 0, 1
            elif self.rect.bottomleft[1] > height:
                return 1, 1
            else:
                return None

    def aumentar_vida(self, qtd):
        """Aumenta a vida do personagem em qtd pontos"""
        if self.vida < self.vida_max:
            self.vida = min(self.vida+qtd, self.vida_max)
            return True
        return False

    def add_item(self, obj):
        """Adciona um item ao inventario"""
        for i in range(len(self.inventario)):
            if type(self.inventario[i]) == type(obj):
                self.inventario[i].quantidade += obj.quantidade
                self.inventario[i].create_sprite(self.inventario[i].img)
                return True
        self.inventario.append(obj)
        obj.create_sprite(obj.img)
        return True
