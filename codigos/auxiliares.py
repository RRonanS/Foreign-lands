# Este arquivo contém funções auxiliares usadas pelo programa
import pygame.transform
from .variaveis import screen_size

pygame.display.set_mode(screen_size)

def img_load(sheet, size, resize=(32, 32), flip=False):
    '''Leitura linear de uma sprite sheet, retorna uma lista de imagens'''
    imagens = []
    for i in range(32):
        try:
            img = sheet.subsurface((size[0]*i, 0), size)
            img = pygame.transform.scale(img, resize)
            img = img.convert_alpha()
            if flip:
                img = pygame.transform.flip(img, True, False)
            imagens.append(img)
        except:
            break
    return imagens
