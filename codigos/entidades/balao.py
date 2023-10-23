import pygame

from codigos.ambiente.textuais import branco, preto, fonte1
from codigos.variaveis import fps, screen_size

width, height = screen_size
text_size = 20, 20
cara = 40  # Max caracteres por linha(so funciona com auto)
m_item = 3  # Max colunas por fala(so funciona com auto)


class Balao(pygame.sprite.Sprite):
    """Classe para representar um balão de fala"""

    def __init__(self, pos, texto, auto=False):
        r"""Recebe a posição do balão, o texto a ser mostrado e se deve
        automaticamente quebrar o texto. Formatos textuais:
        / indica quebra de frase e \ quebra de linha"""
        pygame.sprite.Sprite.__init__(self)
        from codigos.variaveis import fps
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
