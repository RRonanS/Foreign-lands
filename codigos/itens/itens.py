# Módulo para armazenar as classes dos itens adicionados ao jogo
import pygame.sprite
from codigos.ambiente.textuais import fonte1, amarelo, preto, fonte0
from codigos.outros.tradutor import Tradutor

dir = 'arquivos/imagens/itens/'
imagens = {
    'vida': pygame.transform.scale(pygame.image.load(dir + 'pocao_vida.png').convert_alpha(), (32, 32)),
    'vidagrande': pygame.transform.scale(pygame.image.load(dir + 'pocao_vida2.png').convert_alpha(), (32, 32)),
    'velocidade': pygame.transform.scale(pygame.image.load(dir + 'pocao_velocidade.png').convert_alpha(), (32, 32)),
    'dano': pygame.transform.scale(pygame.image.load(dir + 'pocao_dano.png').convert_alpha(), (32, 32)),
    'vidagigante': pygame.transform.scale(pygame.image.load(dir + 'pocao_vida3.png').convert_alpha(), (32, 32)),
    'regen': pygame.transform.scale(pygame.image.load(dir + 'pocao_regeneracao.png').convert_alpha(), (32, 32))
}
diretorios = {'vida': dir + 'pocao_vida.png',
              'vidagrande': dir + 'pocao_vida2.png',
              'velocidade': dir + 'pocao_velocidade.png',
              'dano': dir + 'pocao_dano.png',
              'vidagigante': dir + 'pocao_vida3.png',
              'regen': dir + 'pocao_regeneracao.png'}

tradutor = Tradutor()
def tl(frase):
    return tradutor.traduzir(frase)

class Item(pygame.sprite.Sprite):
    def __init__(self, sprite=False, icon=None):
        pygame.sprite.Sprite.__init__(self)
        self.valor = 0
        self.quantidade = 1
        self.tipo = ''
        self.nome = ''
        self.tool = 'Esse é um Item'
        if sprite:
            self.create_sprite(icon)

    def usar(self, personagem):
        """Método para quando o personagem clicar para usar o item"""
        pass

    def create_sprite(self, img, set_rect=True):
        """Método para exibir o item clicavel na tela"""
        self.image = pygame.surface.Surface((32, 32), pygame.SRCALPHA, 32)
        if set_rect:
            self.rect = self.image.get_rect()
        pygame.draw.line(self.image, (0, 0, 0), (0, 0), (32, 0))
        pygame.draw.line(self.image, (0, 0, 0), (0, 0), (0, 32))
        pygame.draw.line(self.image, (0, 0, 0), (31, 0), (31, 31))
        pygame.draw.line(self.image, (0, 0, 0), (0, 31), (31, 31))
        qnt = fonte1.render(f'{self.quantidade}', True, amarelo)
        self.image.blit(img, (0, 0))
        self.image.blit(qnt, (0, 0))

    def as_drop(self):
        """Metodo chamado quando o item será mostrado como drop"""
        try:
            self.image = pygame.transform.scale(self.img, (16, 16))
            self.rect = self.image.get_rect()
        except:
            raise ValueError('Problema ao criar icone de item:', self)

    def get_tooltip(self):
        """Retorna um objeto de texto com a tooltip do item"""
        texto = fonte0.render(tl(self.tool), True, preto)
        return texto


class Pocao(Item):
    """Classe genérica para um item poção, ou seja pode ser consumido em troca de determinado efeito"""

    def __init__(self, sprite=False, icon=None):
        Item.__init__(self, sprite, icon)
        self.atributo = ''
        self.img = ''
        self.tipo = 'pocao'
        self.bonus = 0
        self.timer = None
        self.tool = 'Esta é uma poção'

    def usar(self, personagem):
        """Override do metodo usar"""
        if self.atributo != '' and self.quantidade > 0:
            func = getattr(personagem, self.atributo)
            if self.timer is None:
                do = func(self.bonus)
            else:
                do = func(self.bonus, self.timer)
            if do:
                self.quantidade -= 1
                self.create_sprite(self.img, False)
        if self.quantidade <= 0:
            self.kill()


class Pocao_vida(Pocao):
    """Subclasse específica referente a uma poção de vida, que ao consumida aumenta a vida atual do personagem"""

    def __init__(self, valor=15):
        # Do_menu indica se ela é um exibivel de menu
        Pocao.__init__(self)
        self.atributo = 'aumentar_vida'
        self.nome = 'pocao de cura'
        self.img_sg = diretorios['vida']
        self.img = imagens['vida']
        self.bonus = 10
        self.valor = valor
        self.classe = 'Pocao_vida'
        self.create_sprite(self.img)

    def get_tooltip(self):
        return fonte0.render(tl(f'Cura {self.bonus} de vida'), True, preto)


class Pocao_vidaGrande(Pocao_vida):
    """Pocao de vida maior"""

    def __init__(self, valor=27):
        Pocao_vida.__init__(self)
        self.img_sg = diretorios['vidagrande']
        self.img = imagens['vidagrande']
        self.nome = 'pocao de cura G'
        self.classe = 'Pocao_vidaGrande'
        self.bonus = 20
        self.valor = valor
        self.create_sprite(self.img)


class Pocao_vidaGigante(Pocao_vida):
    """Pocao de vida gigante"""

    def __init__(self, valor=35):
        Pocao_vida.__init__(self)
        self.img_sg = diretorios['vidagigante']
        self.img = imagens['vidagigante']
        self.nome = 'pocao de cura G+'
        self.classe = 'Pocao_vidaGigante'
        self.bonus = 30
        self.valor = valor
        self.create_sprite(self.img)


class Pocao_velocidade(Pocao):
    """Pocao que aumenta temporariamente a velocidade do jogador"""
    def __init__(self, valor=50):
        Pocao.__init__(self)
        self.timer = 60  # Em segundos
        self.bonus = 2
        self.valor = valor
        self.classe = 'Pocao_velocidade'
        self.atributo = 'aumentar_vel'
        self.img_sg = diretorios['velocidade']
        self.img = imagens['velocidade']
        self.create_sprite(self.img)
        self.tool = 'Aumenta a velocidade temporariamente'
        self.nome = 'pocao de velocidade'


class Pocao_dano(Pocao):
    """Pocao que aumenta temporariamente o dano do jogador"""
    def __init__(self, valor=100):
        Pocao.__init__(self)
        self.timer = 30  # Em segundos
        self.classe = 'Pocao_dano'
        self.bonus = 3
        self.valor = valor
        self.atributo = 'aumentar_dano'
        self.img_sg = diretorios['dano']
        self.img = imagens['dano']
        self.create_sprite(self.img)
        self.tool = 'Aumenta o dano temporariamente'
        self.nome = 'Poção de força'


class Pocao_regen(Pocao):
    """Pocao de regeneração, recupera vida ao longo do tempo"""
    def __init__(self, valor= 70):
        Pocao.__init__(self)
        self.classe = 'Pocao_regen'
        self.timer = 999
        self.bonus = 0.5  # Em pontos de vida por segundo
        self.valor = valor
        self.atributo = 'regenerar_vida'
        self.img_sg = diretorios['regen']
        self.img = imagens['regen']
        self.create_sprite(self.img)
        self.tool = 'Lentamente regenera a vida'
        self.nome = 'Poção de regeneração'
