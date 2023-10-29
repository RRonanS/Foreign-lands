import pygame.sprite
from ..variaveis import exigencia_niveis, fps, screen_size
from ..ambiente.sons import espadas, levelup
from random import choice
from codigos.entidades.gerenciador_imagens import imagens

images = imagens['personagem']

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

    def __init__(self, pos=(0, 0)):
        from codigos.variaveis import fps
        width, height = pos
        self.height, self.width = width, height
        pygame.sprite.Sprite.__init__(self)

        # Variáveis gerais
        self.niveis = [0, 15]
        for i in range(2, 50):
            self.niveis.append(int(self.niveis[i-1]+(exigencia_niveis*self.niveis[i-1])))

        self.revividas = 0
        self.nivel = 1
        self.inventario = []
        self.tipo = 'personagem'
        self.vel, self.vel_max = 7 * (30/fps), 15
        self.acesso = []
        self.desbloqueio = []
        self.pulo_altura = 50
        self.diag_nerf = 1.5
        self.vida_max, self.vida = 10, 10
        self.dano = 5
        self.animar_freq = self.animar_freq_backup = 0.30 * (30/fps)
        self.coins, self.pontos, self.sorte, self.exp = 0, 0, 0, 0
        self.buffs = {}
        self.curando = False
        self.cura_vel = 0

        # Armazenamento das imagens do personagem
        self.images = images

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
        from codigos.variaveis import efeitos
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
        """Se possível, aumenta o nível do personagem, retorna True se há um novo nível, False senão"""
        from codigos.variaveis import efeitos
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
        self.verificar_buffs()
        self.curar()
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
                self.morte()
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
        if self.animar and self.vida > 0:
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
        if self.vida_max > self.vida > 0:
            self.vida = min(self.vida+qtd, self.vida_max)
            return True
        return False

    def aumentar_vel(self, qtd, tempo):
        """Aumenta temporariamente a velocidade do personagem"""
        if self.vel < self.vel_max and self.vida > 0:
            self.vel = min(self.vel_max, self.vel + qtd)
            self.buffs['vel'] = {'valor': qtd, 'tempo_restante': tempo}
            return True
        return False

    def aumentar_dano(self, qtd, tempo):
        """Aumenta temporariamente o dano do personagem"""
        self.dano += qtd
        self.buffs['dano'] = {'valor': qtd, 'tempo_restante': tempo}
        return True

    def regenerar_vida(self, qtd, tempo):
        """Regenera a vida do personagem lentamente"""
        from codigos.variaveis import fps
        if self.vida == self.vida_max:
            return False
        self.curando = True
        self.cura_vel = qtd / fps
        return True

    def curar(self):
        """Cura o personagem com base na regeneracao"""
        if self.sector == 'death':
            self.curando = False
            return False
        if self.curando:
            if self.vida < self.vida_max:
                self.vida = min(self.vida_max, self.vida+self.cura_vel)
            else:
                self.curando, self.cura_vel = False, 0

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

    def verificar_buffs(self):
        """Verifica o vetor de buffs temporarios, removendo efeitos expirados"""
        for effect in list(self.buffs):
            if self.buffs[effect]['tempo_restante'] <= 0:
                setattr(self, effect, getattr(self, effect)-self.buffs[effect]['valor'])
                del self.buffs[effect]
                print('efeito expirado')
            else:
                self.buffs[effect]['tempo_restante'] = self.buffs[effect]['tempo_restante'] - (1/fps)

    def morte(self):
        """Funcao chamada quando o personagem for morto"""
        self.animar = False
        self.sector = 'death'
        self.animar_freq = 0
        self.index = len(self.images['death']) - 1

    def reviver(self):
        """Funcao chamada para reviver o personagem"""
        self.animar, self.sector, self.animar_freq, self.index = True, 'idle', self.animar_freq_backup, 0
        self.vida = self.vida_max

    def get_custoreviver(self):
        """Retorna quantos coins custará para reviver"""
        return 50 * (2 * (1+self.revividas))

    def reviver_custo(self):
        """Revive o personagem com custo de coins"""
        c = self.get_custoreviver()
        if self.coins >= c:
            self.coins -= c
            self.revividas += 1
            self.reviver()
            return True
        return False

    def is_dead(self):
        """Retorna se o personagem está morto"""
        if self.sector == 'death':
            return True
        return False
