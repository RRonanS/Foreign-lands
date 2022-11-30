import pygame.sprite

dir = 'arquivos/imagens/decorativo/'


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        sheet = pygame.image.load(dir+'coin.png')
        self.images = []
        self.images.append(sheet.subsurface((0, 0, 3, 16)))
        self.images.append(sheet.subsurface((11, 0, 12, 16)))
        self.images.append(sheet.subsurface((26, 0, 14, 16)))
        self.images.append(sheet.subsurface((43, 0, 12, 16)))
        self.images.append(sheet.subsurface(64, 0, 3, 16))
        self.index = 0
        self.vel = 0.25
        self.value = 1
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def update(self):
        self.index += self.vel
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[int(self.index)]

