import math

import pygame.sprite
from codigos.variaveis import fps, screen_size

width, height = screen_size


class Projetil(pygame.sprite.Sprite):
    """Classe para representar projeteis"""
    def __init__(self, images, vel=1, dano=0, anim_freq=0.2*(30/fps), dir=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.dir = [dir[0], dir[1]]  # Index 0 indica a direção x, index 1 a direção y
        self.angulo = self.calcular_angulo()
        self.index, self.anim_freq = 0, anim_freq
        self.tipo = 'projetil'
        self.vel = vel
        self.dano = dano
        self.images = images
        self.image = pygame.transform.rotate(self.images[self.index], -self.angulo)
        self.rect = self.image.get_rect()

    def update(self):
        if self.try_kill():
            return 0
        self.index = self.index + self.anim_freq
        if self.index >= len(self.images):
            self.index = 0
        self.image = pygame.transform.rotate(self.images[int(self.index)], -self.angulo)
        self.mover()

    def mover(self):
        """Move o projetil dado seu vetor"""
        if self.dir[0] < 0:
            self.rect.centerx += self.vel
        elif self.dir[0] > 0:
            self.rect.centerx -= self.vel

        if self.dir[1] < 0:
            self.rect.centery += self.vel
        elif self.dir[1] > 0:
            self.rect.centery -= self.vel

    def colidiu(self, personagem):
        """Projetil colide com jogador"""
        personagem.vida -= self.dano
        self.kill()

    def try_kill(self):
        """Retorna se a entidade deve morrer"""
        if self.rect.centerx < 0 or self.rect.centerx > width:
            self.kill()
            return True
        if self.rect.centery < 0 or self.rect.centery > height:
            self.kill()
            return True
        return False

    def calcular_angulo(self):
        """Retorna o angulo do projetil"""
        angle = math.atan2(self.dir[1], self.dir[0])
        angle_degrees = math.degrees(angle)
        return angle_degrees
