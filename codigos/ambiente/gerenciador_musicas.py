from random import random, randint
import pygame
from time import sleep
from codigos.ambiente.sons import efeitos_cenarios


class GerenciadorMusica:
    """Classe responsável por controlar as musicas e efeitos de fundo dos cenarios do jogo"""
    def __init__(self):
        self.musicas = {
            1: 'arquivos/sons/musicas/The_Old_Tower_Inn.mp3',
            2: 'arquivos/sons/musicas/darkpiano.mp3',
            3: 'arquivos/sons/musicas/death.mp3',
            4: 'arquivos/sons/musicas/boss1.mp3',
            5: 'arquivos/sons/musicas/mushroom.mp3'
        }
        self.volume_mult = {
            1: 1,
            2: 1.5,
            3: 1,
            4: 2,
            5: 1
        }

        # Organiza efeitos sonoros que podem ocorrer dado determinado cenario
        self.cenarios_efeitos = {
            '0 -5': {
                'efeitos':
                    {
                        1: {'chance': 0.1},
                        2: {'chance': 0.05},
                        3: {'chance': 0.15}
                    }
            },
            '1 -5': {
                'efeitos':
                    {
                        1: {'chance': 0.1},
                        2: {'chance': 0.05},
                        3: {'chance': 0.15}
                    }
            },
            '2 -5': {
                'efeitos':
                    {
                        1: {'chance': 0.1},
                        2: {'chance': 0.05},
                        3: {'chance': 0.15}
                    }
            },
            '3 -5': {
                'efeitos':
                    {
                        1: {'chance': 0.1},
                        2: {'chance': 0.05},
                        3: {'chance': 0.15}
                    }
            },
            '4 -5': {
                'efeitos':
                    {
                        1: {'chance': 0.1},
                        2: {'chance': 0.05},
                        3: {'chance': 0.15}
                    }
            },
            '5 -5': {
                'efeitos':
                    {
                        1: {'chance': 0.1},
                        2: {'chance': 0.05},
                        3: {'chance': 0.15}
                    }
            }
        }

        self.playing = 0
        self.cenario = 0, 0
        self.effect_thread_run = True

    def run(self, cenario):
        """Executa o gerenciamento das musicas do jogo"""
        from codigos.variaveis import musica, volume
        x, y = cenario[0], cenario[1]
        self.cenario = cenario
        old = self.playing
        if musica:
            if self.playing != 5 and y <= -1:
                pygame.mixer.music.load(self.musicas[5])
                self.playing = 5
            elif x <= 5 and y == 0 and self.playing != 1:
                pygame.mixer.music.load(self.musicas[1])
                self.playing = 1
            elif x >= 8 and y == 0 and self.playing != 4:
                pygame.mixer.music.load(self.musicas[4])
                self.playing = 4
            elif self.playing != 2 and y == 0 and 5 < x < 8:
                pygame.mixer.music.load(self.musicas[2])
                self.playing = 2

            if old != self.playing:
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(volume*self.volume_mult[self.playing])

    def effect_thread(self):
        """Thread responsavel por efeitos sonoros aleatorios ao fundo"""
        from codigos.variaveis import musica
        if not musica:
            return
        while self.effect_thread_run:
            sleep(1)
            if randint(1, 5) == 5:
                x, y = self.cenario
                cenario = f'{x} {y}'
                if cenario in self.cenarios_efeitos:
                    for efeito in self.cenarios_efeitos[cenario]['efeitos']:
                        if random() <= self.cenarios_efeitos[cenario]['efeitos'][efeito]['chance']:
                            efeitos_cenarios[efeito].play()
                            break

    def play_death(self):
        """Toca o som quando o jogador morre"""
        from codigos.variaveis import musica, volume
        if self.playing != 3 and musica:
            pygame.mixer.music.load(self.musicas[3])
            self.playing = 3
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(volume)

    def stop(self):
        """Desativa o modulo"""
        pygame.mixer.music.stop()
        self.effect_thread_run = False
