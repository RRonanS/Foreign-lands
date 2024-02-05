# Este arquivo possui os construtores para todos monstros usados no jogo
import pygame.sprite
from .projetil import Projetil
from ..variaveis import screen_size, exp_mult, fps
from random import randint, random
from codigos.entidades.gerenciador_imagens import imagens as imagens_todas
import codigos.itens.itens as itens
from codigos.ambiente.sons import monstros_sounds

width, height = screen_size
imagens = imagens_todas['monstros']
sounds = monstros_sounds


class Monstro(pygame.sprite.Sprite):
    """Classe pai para representar todas entidades"""

    def __init__(self):
        from codigos.variaveis import fps
        pygame.sprite.Sprite.__init__(self)
        self.visao = 0.3
        self.vel = 2 * (30 / fps)
        self.coin_drop = (1, 1)
        self.tipo = 'monster'
        self.voa = False
        self.drops = []
        self.diretorio = 'arquivos/imagens/monstros/'
        self.images = {}
        self.is_boss = False
        self.has_spell = False
        self.ataque_critico = False
        self.vel_real = self.vel
        self.slowed = False
        self.anim_mult = 0.3 * (30 / fps)
        self.droprate = {'Pocao_vida': 0.01}
        self.sounds = {}

    def drop(self, sorte=0):
        """Gera os drops referentes a tal inimigo"""
        from ..mapa.decorativo import Coin
        moeda = Coin()
        val = randint(self.coin_drop[0], int(self.coin_drop[1]*(1 + (sorte/50))))
        moeda.value = val
        x, y = self.rect.centerx, self.rect.centery
        moeda.rect.centerx, moeda.rect.centery = x, y
        drops = [moeda]
        for key in self.droprate:
            # Drop de itens
            if self.droprate[key] + sorte/100 > random():
                classe = getattr(itens, key)
                obj = classe()
                obj.as_drop()
                obj.rect.centerx, obj.rect.centery = x, y
                drops.append(obj)
                if self.droprate[key] + sorte/100 > 1 and self.droprate[key] > random():
                    # Chance de dropar um segundo item
                    classe = getattr(itens, key)
                    obj = classe()
                    obj.as_drop()
                    obj.rect.centerx, obj.rect.centery = x, y
                    drops.append(obj)
        return drops

    def play_sound(self, sound):
        """Toca algum som relacionado ao inimigo"""
        from codigos.variaveis import efeitos
        if sound in self.sounds and efeitos:
            self.sounds[sound].play()
        return

    def slow(self, percent):
        """Diminui a velocidade da entidade, -1 reseta"""
        if percent == -1 and self.slowed:
            self.slowed = False
            self.vel = self.vel_real
        elif not self.slowed:
            self.vel_real = self.vel
            self.slowed = True
            self.vel = (1-percent) * self.vel


class Esqueleto(Monstro):
    """Herda da classe pai e representa um esqueleto"""

    class sprite_espada(pygame.sprite.Sprite):
        """Classe chamada apenas durante ataques para calculo de colisão da espada"""

        def __init__(self, img, pos, flip, index=6, offsets=(0, 0)):
            pygame.sprite.Sprite.__init__(self)
            if index >= len(img):
                index = len(img) - 1
            self.image = img[index]
            self.rect = self.image.get_rect()
            self.rect.topleft = pos.topleft[0], pos.topleft[1]
            self.rect.width += offsets[0]
            self.rect.height += offsets[1]
            if flip:
                self.mask = pygame.mask.from_surface(pygame.transform.flip(
                    img[index], True, False
                ))
            else:
                self.mask = pygame.mask.from_surface(img[index])

    def __init__(self):
        Monstro.__init__(self)
        self.droprate = {'Pocao_vida': 0.02}

        # variáveis da entidade
        self.vida, self.vida_max = 10, 10
        self.dano, self.peso = 3, 2
        self.random_walk_mult = 0.02
        self.exp = 15 * exp_mult
        self.anim_mult = 0.37 * (30 / fps)

        self.sector, self.index = 'idle', 0

        # Chamada e armazenamento das imagens do monstro
        self.images = imagens['esqueleto']

        self.sounds = sounds['esqueleto']

        # Varíaveis de funcionamento
        self.image = self.images[self.sector][self.index]
        self.rect = self.image.get_rect()
        self.rect.bottomright = screen_size
        self.mask = pygame.mask.from_surface(self.images['idle'][0])
        self.dir = 0, 0
        self.flip, self.ataque, self.dead, self.busy = False, False, False, False
        self.animar = True

    def atacar(self):
        """Caso possível, executa um ataque"""
        if self.sector != 'attack' and self.animar:
            self.sector = 'attack'
            self.animar = False

    def ataque_sprite(self):
        """Gera a sprite usada no cálculo de colisoes"""
        return self.sprite_espada(self.images['attack'], self.rect, self.flip, offsets=(32, 32))

    def update_especifico(self):
        """Update especifico para ser editado em subclasses, representando atualizações individuais"""
        pass

    def update_especifico2(self):
        """Update especifico pós atualização de setor"""
        pass

    def rand_walk(self):
        """Gera um valor aleatorio de movimento para a entidade"""
        if random() <= self.random_walk_mult:
            nao_move = randint(0, 3)
            if nao_move == 0:
                # Gera os valores de movimentação aleatoria
                vai_x, vai_y = randint(0, 1), randint(0, 1)
                dx = dy = 0
                if vai_x:
                    dx = randint(1, width // 2)
                if vai_y:
                    dy = randint(1, height // 2)
                self.dir = dx, dy

    def update(self):
        self.update_especifico()
        if self.dir[0] == 0 and self.dir[1] == 0:
            self.sector = 'idle'
        if self.vida <= 0:
            self.animar = False
            self.sector = 'death'

        # Parte das animações
        self.index += self.anim_mult
        if self.index >= len(self.images[self.sector]):
            self.index = 0
            if self.sector == 'attack' or self.sector == 'cast':
                self.sector = 'idle'
                self.animar = True
                self.ataque = True
            elif self.sector == 'walk' and self.dir[0] == -1:
                self.sector = 'idle'
            elif self.sector == 'death':
                self.vel = 0
                self.dead = True

        self.update_especifico2()

        if self.flip:
            img = pygame.transform.flip(self.images[self.sector][int(self.index)],
                                        True, False)
        else:
            img = self.images[self.sector][int(self.index)]
        self.image = img

    def mover(self, ver_func, ver_func2, entidades):
        """Dado o vetor de dir do objeto, as verificacoes de validade do chao e as entidades do jogo,
         avança para uma nova posição válida,se essa existir """
        if self.animar:
            self.sector = 'walk'
            if self.dir[0] != 0:
                # Movimentação no eixo x
                sinal = -1
                self.flip = False
                if self.dir[0] < 0:
                    sinal = +1
                    self.flip = True
                self.rect.centerx += self.vel * sinal
                # Verifica se a posição nova é válida
                if not self.voa:
                    if not (ver_func(self.rect.center)) or ver_func2(self.rect):
                        self.rect.centerx -= self.vel*sinal

            if self.dir[1] != 0:
                # Movimentação no eixo y
                sinal = -1
                if self.dir[1] < 0:
                    sinal = 1
                self.rect.centery += self.vel * sinal
                # Verifica se a nova posição é válida
                if not self.voa:
                    if not (ver_func(self.rect.center)) or ver_func2(self.rect):
                        self.rect.centery -= self.vel*sinal
            # Arredondamento do restante do movimento
            if abs(self.dir[0]) < self.vel:
                self.dir = 0, self.dir[1]
            if abs(self.dir[1]) < self.vel:
                self.dir = self.dir[0], 0


class Olho(Esqueleto):
    """Representa o monstro Olho, herda do esquelto, mudando apenas imagens
     e varíaveis gerais"""

    def __init__(self):
        Esqueleto.__init__(self)
        self.droprate = {'Pocao_vida': 0.03, 'Pocao_vidaGrande': 0.01}
        self.coin_drop = (1, 2)

        self.vida_max, self.vida = 15, 15
        self.dano, self.vel, self.peso = 5, 3 * (30 / fps), 3
        self.visao = 0.5
        self.exp = 25 * exp_mult
        self.voa = True
        self.anim_mult = 0.25 * (30 / fps)

        self.sounds = sounds['olho']

        self.images = imagens['olho']

        self.image = self.images[self.sector][self.index]


class Goblin(Esqueleto):
    """Representa o monstro Goblin, herda do esquelto, mudando apenas imagens
     e varíaveis gerais"""

    def __init__(self):
        Esqueleto.__init__(self)
        self.droprate = {'Pocao_vida': 0.05, 'Pocao_vidaGrande': 0.02}
        self.coin_drop = (2, 3)

        self.vida_max, self.vida = 30, 30
        self.dano, self.peso, self.vel = 8, 5 * (30 / fps), 2 * (30 / fps)
        self.visao = 0.25
        self.exp = 50 * exp_mult
        self.anim_mult = 0.32 * (30 / fps)

        self.sounds = sounds['goblin']

        self.images = imagens['goblin']

        self.image = self.images[self.sector][self.index]
        self.mask = pygame.mask.from_surface(self.images['attack']
                                             [len(self.images['attack']) - 1])
        self.rect = self.image.get_rect()


class Cogumelo(Esqueleto):
    """Representa o monstro Cogumelo, herda do esquelto, mudando apenas imagens
     e varíaveis gerais"""

    def __init__(self):
        Esqueleto.__init__(self)
        self.droprate = {'Pocao_vida': 0.08, 'Pocao_vidaGrande': 0.04, 'Pocao_dano': 0.02}
        self.coin_drop = (3, 5)

        self.vida_max, self.vida = 40,  40
        self.dano, self.vel, self.peso = 9, 2 * (30 / fps), 8
        self.visao = 0.20
        self.exp = 200 * exp_mult
        self.anim_mult = 0.4 * (30 / fps)

        self.sounds = sounds['cogumelo']

        self.images = imagens['cogumelo']

        self.image = self.images[self.sector][self.index]
        self.mask = pygame.mask.from_surface(self.images['attack']
                                             [len(self.images['attack']) - 1])

    def ataque_sprite(self):
        """Retorna a sprite usada no calculo de colisões"""
        return self.sprite_espada(self.images['attack'], self.rect, self.flip, 7)


class BringerDeath(Esqueleto):
    """Monstro bringer of death"""
    class SpellSprite(pygame.sprite.Sprite):
        """Sprite do seu spell"""
        def __init__(self, images, dmg):
            pygame.sprite.Sprite.__init__(self)
            self.imgs = images
            self.end = False
            self.dmg = dmg
            self.sector = 0
            self.vel = 0.15 * (30 / fps)
            self.image = images[self.sector]
            self.rect = self.image.get_rect()
            self.anim_mult = 0.3 * (30 / fps)

        def update(self):
            self.sector += self.vel
            if self.sector >= len(self.imgs):
                # Fim da sprite, sinaliza na variavel end para causar o dano
                self.end = True
                self.sector = 0
            else:
                self.image = self.imgs[int(self.sector)]

    def __init__(self):
        Esqueleto.__init__(self)
        self.droprate = {'Pocao_vida': 0.20, 'Pocao_vidaGrande': 0.10,
                         'Pocao_velocidade': 0.05, 'Pocao_dano': 0.02}
        self.coin_drop = (10, 20)
        self.has_spell = True
        self.spelling = False

        self.vida_max, self.vida = 100, 100
        self.dano, self.vel, self.peso = 7, 2.5 * (30 / fps), 10
        self.visao = 0.25
        self.exp = 2000 * exp_mult
        self.spell_cooldown, self.spell_total = 0,  15 * fps
        self.spell_range = 2  # Range quadrado em * tamanho do monstro
        self.spell_dmg = 5

        self.sounds = sounds['bringerdeath']

        self.images = imagens['bringerdeath']

        self.image = self.images[self.sector][self.index]
        self.mask = pygame.mask.from_surface(self.images['attack']
                                             [len(self.images['attack']) - 1])

    def spell(self):
        """Funcao para lancar o spell"""
        self.spell_cooldown = self.spell_total
        self.spelling = True

    def atacar(self):
        """Caso possível, executa um ataque ou lança spell"""
        if self.sector != 'attack' and self.animar:
            if self.spell_cooldown == 0:
                self.sector = 'cast'
            else:
                self.sector = 'attack'
            self.animar = False

    def update_especifico(self):
        """Updates especificos do monstro"""
        if self.sector == 'cast' and self.index + self.anim_mult >= len(self.images[self.sector]):
            self.spell()
        self.spell_cooldown = max(0, self.spell_cooldown-1)

    def get_spell(self):
        """Retorna uma sprite responsavel pelo spell"""
        return self.SpellSprite(self.images['spell'], self.spell_dmg)


class Executor(Esqueleto):
    """Monstro executor, invocado pelo boss executioner"""
    def __init__(self):
        Esqueleto.__init__(self)

        self.droprate = {'Pocao_vida': 0.10}
        self.coin_drop = (1, 5)

        self.vida_max, self.vida = 10, 10
        self.dano, self.vel, self.peso = 2, 3 * (30 / fps), 1
        self.visao = 0.7
        self.exp = 50 * exp_mult
        self.voa = True
        self.anim_mult = 0.25 * (30 / fps)

        self.images = imagens['executor']

        self.image = self.images[self.sector][self.index]


class Shooter(Esqueleto):
    """Classe base para monstros que disparam projeteis, recebe como parametro o grupo
    para adicionar os projetis"""
    class sprite_colide(pygame.sprite.Sprite):
        """Sprite para detectar colisao"""
        def __init__(self, img, rect):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.centerx, self.rect.centery = rect.centerx, rect.centery
            self.mask = pygame.mask.from_surface(self.image)

    def __init__(self):
        Esqueleto.__init__(self)
        self.pr_vel = 1
        self.visao_ataque = 1

    def update_especifico2(self):
        """Override do método, verifica se está atacando para gerar a sprite do projetil"""
        if self.ataque:
            self.ataque = False
            projetil = self.gerar_projetil(self.dir)
            if projetil is not None:
                projetil.rect.center = self.rect.center
                grupo = None
                for gp in self.groups():
                    # Busca o menor grupo(tecnicamente o grupo que está em update)
                    if grupo is None:
                        grupo = gp
                    else:
                        if len(gp) < len(grupo):
                            grupo = gp
                grupo.add(projetil)

    def gerar_projetil(self, dir):
        """Retorna uma instancia do projetil da classe"""
        return None

    def ataque_sprite(self):
        m = pygame.transform.scale(self.images['attack'][0],
                                   (width*self.visao_ataque, height*self.visao_ataque))
        return self.sprite_colide(m, self.rect)


class Golem(Shooter):
    """Monstro golem"""
    def __init__(self):
        Shooter.__init__(self)

        self.droprate = {'Pocao_vida': 0.5, 'Pocao_vidaGrande': 0.25,
                         'Pocao_velocidade': 0.10, 'Pocao_dano': 0.10,
                         'Pocao_vidaGigante': 0.08, 'Pocao_regen': 0.05}
        self.coin_drop = (15, 30)

        self.vida_max, self.vida = 120, 120
        self.dano, self.vel, self.peso = 8, 2 * (30 / fps), 10
        self.visao = 0.7
        self.visao_ataque = 0.5
        self.anim_mult *= 0.8
        self.exp = 3000 * exp_mult
        self.sector, self.index = 'idle', 0
        self.pr_vel = 2
        self.images = imagens['golem']

        self.image = self.images[self.sector][self.index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.images['attack']
                                             [len(self.images['attack']) - 1])

    def gerar_projetil(self, dir):
        """Gera projetil especifico do golem"""
        return Projetil(imagens_todas['projetis']['golem'], self.pr_vel, self.dano, dir=dir)


class Lobo(Esqueleto):
    """Monstro lobo"""
    def __init__(self):
        Esqueleto.__init__(self)

        self.droprate = {'Pocao_vida': 0.3, 'Pocao_vidaGrande': 0.10,
                         'Pocao_velocidade': 0.2, 'Pocao_dano': 0.30,
                         'Pocao_vidaGigante': 0.02, 'Pocao_regen': 0.02}
        self.coin_drop = (10, 20)

        self.vida_max, self.vida = 50, 50
        self.dano, self.vel, self.peso = 4, 3.5 * (30 / fps), 1
        self.visao = 0.3
        self.exp = 1000 * exp_mult
        self.anim_mult = 0.15 * (30 / fps)

        self.images = imagens['lobo']

        self.image = self.images[self.sector][self.index]
        self.rect = self.image.get_rect()

        self.rect.width -= 8  # Ajustes para colisao
        self.rect.height -= 8

        self.mask = pygame.mask.from_surface(self.images['attack']
                                             [len(self.images['attack']) - 1])

    def update_especifico2(self):
        """Muda a inversao"""
        if self.sector == 'walk':
            self.flip = not self.flip
        if self.dir[1] != 0 and self.dir[0] == 0:
            self.flip = False

    def ataque_sprite(self):
        """Gera o sprite de deteccao de colisoes"""
        m = pygame.transform.scale(self.images['attack'][0],
                                   (self.images['attack'][0].get_width()*2,
                                    self.images['attack'][0].get_height()*2))
        return self.sprite_espada([m], self.rect, self.flip, 0)
