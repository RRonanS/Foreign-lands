# Módulo para armazenar as classes dos itens adicionados ao jogo
import pygame.sprite
from codigos.ambiente.textuais import fonte1, amarelo

dir = 'arquivos/imagens/itens/'
imagens = {'vida': pygame.transform.scale(pygame.image.load(dir+'pocao_vida.png').convert_alpha(), (32, 32))}
diretorios = {'vida': dir+'pocao_vida.png'}


class Item(pygame.sprite.Sprite):
    def __init__(self, sprite=False, icon=None):
        pygame.sprite.Sprite.__init__(self)
        self.valor = 0
        self.quantidade = 1
        self.tipo = ''
        self.nome = ''
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


class Pocao(Item):
    """Classe genérica para um item poção, ou seja pode ser consumido em troca de determinado efeito"""
    def __init__(self, sprite=False, icon=None):
        Item.__init__(self, sprite, icon)
        self.atributo = ''
        self.img = ''
        self.tipo = 'pocao'
        self.bonus = 0

    def usar(self, personagem):
        """Override do metodo usar"""
        if self.atributo != '' and self.quantidade > 0:
            func = getattr(personagem, self.atributo)
            do = func(self.bonus)
            if do:
                self.quantidade -= 1
                self.create_sprite(self.img, False)
        if self.quantidade <= 0:
            self.kill()


class Pocao_vida(Pocao):
    """Subclasse específica referente a uma poção de vida, que ao consumida aumenta a vida atual do personagem"""
    def __init__(self):
        Pocao.__init__(self)
        self.atributo = 'aumentar_vida'
        self.nome = 'Poção de cura'
        self.img_sg = diretorios['vida']
        self.img = imagens['vida']
        self.bonus = 10
        self.valor = 10
        self.classe = 'Pocao_vida'
        self.create_sprite(self.img)
