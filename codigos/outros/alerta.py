from time import sleep

import pygame.sprite
from codigos.ambiente.textuais import fonte2, roxo_claro
from codigos.variaveis import screen_size
from threading import Thread

width, height = screen_size


class Alerta(pygame.sprite.Sprite):
    """Classe para representar um alerta textual temporário na tela"""
    def kill_thread(self):
        """Thread para matar o objeto após determinado tempo"""
        sleep(self.tempo)
        self.kill()

    def __init__(self, texto, tempo=5, cor=roxo_claro, fonte=fonte2):
        pygame.sprite.Sprite.__init__(self)
        self.font = fonte
        self.tempo = tempo
        self.image = self.font.render(texto, True, cor)
        self.rect = self.image.get_rect()
        self.rect.center = width//2, self.image.get_height()
        t_kill = Thread(target=self.kill_thread)
        t_kill.start()
