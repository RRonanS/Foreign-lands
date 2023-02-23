from pygame import image, transform
from codigos.variaveis import screen_size as size

width, height = size

background1 = image.load('arquivos/imagens/background.jpg')
background1 = transform.scale(background1, (width, height))
background2 = image.load('arquivos/imagens/background2.jpg')
background2 = transform.scale(background2, (width, height))
backgrounds = {0: background1, 1: background2}
