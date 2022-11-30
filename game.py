import pygame
from pygame.locals import *
from sys import exit
from codigos.chao import Chao
from codigos.personagem import Personagem
from codigos.monstros import gerar_inimigos
from codigos.variaveis import screen_size, dificuldade, musica, imortal, char_size, block_size, full_screen
from codigos.cenarios import cenarios
from codigos.bosses import boss_group
from codigos.menu import level_up

pygame.init()

preto = 0, 0, 0
vermelho = 255, 0, 0
verde = 0, 255, 0
amarelo = 255, 255, 0

width, height = screen_size
size = screen_size

background1 = pygame.image.load('arquivos/imagens/background.jpg')
background1 = pygame.transform.scale(background1, (width, height-64))
background2 = pygame.image.load('arquivos/imagens/background2.jpg')
background2 = pygame.transform.scale(background2, (width, height-64))
backgrounds = {0: background1, 1: background2}
background = backgrounds[0]

if musica:
    pygame.mixer.music.load('arquivos/sons/musicas/The_Old_Tower_Inn.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)

chao_sprite = cenarios[0].grupo

inimigos = pygame.sprite.Group()
drops = pygame.sprite.Group()
lista_sprites = pygame.sprite.Group()
bosses = boss_group(lista_sprites, inimigos)

personagem = Personagem(height)
lista_sprites.add(personagem)
dir = (-1, personagem.vel)
# -1 não move, 0 x, 1 y,2 x e y, index 1->velocidade x, index 2 velocidade y

# Geração dos inimigos
gerar_inimigos(dificuldade, (0, 9), inimigos)
for sprite in inimigos.sprites():
    lista_sprites.add(sprite)

fonte1 = pygame.font.SysFont('arial', 12, True, True)
fonte2 = pygame.font.SysFont('arial', 20, True, True)
fonte3 = pygame.font.SysFont('arial', 30, True, True)

if not full_screen:
    tela = pygame.display.set_mode(size)
else:
    tela = pygame.display.set_mode((0, 0), FULLSCREEN)
pygame.display.set_caption('Game 1')
relogio = pygame.time.Clock()


def health_bar(target):
    '''Mostra na tela a barra de vida da entidade target'''
    size = 12
    pos = target.rect.center
    prop = target.vida/target.vida_max
    pygame.draw.line(tela, vermelho, pos, (pos[0]+size, pos[1]))
    if prop > 0:
        pygame.draw.line(tela, verde, pos, (pos[0]+int(size*prop), pos[1]))


def boss_lbl(target):
    pos = width//2, 0
    prop = target.vida/target.vida_max
    pygame.draw.line(tela, vermelho, pos, (pos[0], pos[1]+15), 300)
    if prop > 0:
        pygame.draw.line(tela, verde, pos, (pos[0], pos[1]+15), int(300*prop))


def level(target):
    '''Mostra o nível do jogador na tela'''
    nivel = target.nivel
    pos = target.rect.centerx-14, target.rect.centery-8
    formatado = fonte1.render(str(nivel), True, vermelho)
    tela.blit(formatado, pos)


def dados(target):
    '''Mostra dados do jogador na tela'''
    atual, restante = int(target.exp), int(target.niveis[target.nivel])
    formatado = fonte2.render(f'{atual}/{restante} XP', True, verde)
    if personagem.coins == 0 or personagem.coins>1:
        adj = 's'
    else: adj = ''
    budget = fonte2.render(f'{personagem.coins} coin{adj}', True, amarelo)
    tela.blit(formatado, (width-80, 0))
    tela.blit(budget, (width-80, 20))


if imortal:
    personagem.vida, personagem.vida_max = 10000, 10000
cenario = 0
personagem.rect.bottomleft = 0, height
while True:
    # Laço principal do jogo
    relogio.tick(30)
    tela.fill(preto)
    tela.blit(background, (0, 0))
    chao_sprite.draw(tela)
    for event in pygame.event.get():
        # Recebe os eventos da tela
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            # Clicou uma tecla
            if pygame.key.get_pressed()[K_w]:
                if pygame.key.get_pressed()[K_d]:
                    dir = (2, personagem.vel, -personagem.vel)
                elif pygame.key.get_pressed()[K_a]:
                    dir = (2, -personagem.vel, -personagem.vel)
                else:
                    dir = (1, -personagem.vel)
            elif pygame.key.get_pressed()[K_s]:
                if pygame.key.get_pressed()[K_d]:
                    dir = (2, personagem.vel, personagem.vel)
                elif pygame.key.get_pressed()[K_a]:
                    dir = (2, -personagem.vel, personagem.vel)
                else:
                    dir = (1, personagem.vel)
            elif pygame.key.get_pressed()[K_d]:
                dir = (0, personagem.vel)
            elif pygame.key.get_pressed()[K_a]:
                dir = (0, -personagem.vel)
            if pygame.key.get_pressed()[K_t]:
                personagem.attack()
            if pygame.key.get_pressed()[K_SPACE]:
                if dir[0] == 1:
                    dir = (-1, 0)
                personagem.pular()
            if pygame.key.get_pressed()[K_p]:
                level_up(personagem)
        elif event.type == KEYUP:
            # Soltou a tecla
            stop = False
            if event.key == K_d and dir == (0, personagem.vel):
                stop = True
            elif event.key == K_a and dir == (0, -personagem.vel):
                stop = True
            elif event.key == K_s and dir == (1, personagem.vel):
                stop = True
            elif event.key == K_w and dir == (1, -personagem.vel):
                stop = True
            else:
                if event.key in (K_d, K_a, K_s, K_w) and dir[0] == 2:
                    stop = True
            if stop:
                dir = (-1, 0)
                personagem.idle()

    # Movimento do personagem
    if dir[0] != -1 and personagem.animar:
        if dir[0] == 0:
            if -48 <= personagem.rect.bottomleft[0]+dir[1] <= width-48:
                # Move no eixo x
                personagem.rect.centerx += dir[1]
                personagem.correr()
                undo = True
                for x in chao_sprite.sprites():
                    if pygame.sprite.collide_mask(x, personagem):
                        undo = False
                        break
                if undo and not personagem.pulo:
                    personagem.rect.centerx -= dir[1]

        elif dir[0] == 1:
            # Move no eixo y
            if char_size[1]//2 <= personagem.rect.bottomleft[1]+dir[1] <= height:
                personagem.rect.centery += dir[1]
                personagem.correr()
                undo = True
                for x in chao_sprite.sprites():
                    if pygame.sprite.collide_mask(x, personagem):
                        undo = False
                        break
                if undo: personagem.rect.centery -= dir[1]

        elif dir[0] == 2:
            # Move em diagonal
            if -48 <= personagem.rect.bottomleft[0]+dir[1] <= width-48:
                # Move no eixo x
                personagem.rect.centerx += dir[1]
                personagem.correr()
            if height-64 <= personagem.rect.bottomleft[1]+dir[2] <= height:
                personagem.rect.centery += dir[2]
                personagem.correr()
            undo = True
            for x in chao_sprite.sprites():
                if pygame.sprite.collide_mask(x, personagem):
                    undo = False
                    break
            if undo:
                personagem.rect.centerx -= dir[1]
                personagem.rect.centery -= dir[2]

        if personagem.rect.bottomright[0] >= width:
            # Avança no cenário para direita
            cenario += 1
            if cenario == 10:
                background = backgrounds[1]
            if cenario not in cenarios:
                cenarios[cenario] = Chao((0, width, height, height-block_size[0]), 0, 0)
            chao_sprite = cenarios[cenario].grupo
            personagem.rect.x = 0
            for inimigo in inimigos.sprites():
                inimigo.rect.x = 0 + (inimigo.rect.x - width)
            for item in drops.sprites():
                item.rect.x = 0 + (item.rect.x - width)
        elif personagem.rect.bottomleft[0] <= 0 and cenario > 0:
            # Retorna no cenário para esquerda
            cenario -= 1
            if cenario == 9:
                background = backgrounds[0]
            chao_sprite = cenarios[cenario].grupo
            personagem.rect.x = width - 100
            for inimigo in inimigos.sprites():
                inimigo.rect.x = width + inimigo.rect.x
            for item in drops.sprites():
                item.rect.x = width + item.rect.x
        if dir[1] <= 0:
            personagem.flip = True
        else:
            personagem.flip = False

    lista_sprites.update()
    lista_sprites.draw(tela)

    for inimigo in inimigos.sprites():
        # Processos dos inimigos
        health_bar(inimigo)
        if pygame.sprite.collide_mask(inimigo, personagem.sprite_ataque()) is not None:
            if personagem.ataque:
                # Personagem atacou
                inimigo.vida -= personagem.dano
                personagem.ataque = False
        if pygame.sprite.collide_mask(inimigo.ataque_sprite(), personagem) is not None:
            # Colisão com player
            if personagem.vida >= 0:
                # Ataca o player
                inimigo.atacar()
            inimigo.dir = -1, 0
            if inimigo.ataque:
                # Atacou o player
                personagem.vida -= inimigo.dano
                inimigo.ataque = False
        elif inimigo.ataque:
            # Ataque inimigo errou o player
            inimigo.ataque = False

        if abs(personagem.rect.x-abs(inimigo.rect.x)) <= inimigo.visao*width \
                and personagem.vida >= 0 and not inimigo.busy:
            # Ir em direção do player
            if personagem.rect.x - inimigo.rect.x > 0:
                inimigo.dir = 0, inimigo.vel
            elif personagem.rect.x - inimigo.rect.x < 0:
                inimigo.dir = 0, -inimigo.vel
            if abs(personagem.rect.x - inimigo.rect.x) <= 32:
                if personagem.rect.y - inimigo.rect.y < 0:
                    inimigo.dir = 1, -inimigo.vel
                elif personagem.rect.y - inimigo.rect.y > 0:
                    inimigo.dir = 1, inimigo.vel

        if inimigo.busy:
            if inimigo.left[2] == 0:
                v = inimigo.vel
            else: v = -inimigo.vel
            if inimigo.left[0] > 0:
                inimigo.dir = (0, v)
                inimigo.left[0] -= inimigo.vel
            elif inimigo.left[1] > 0:
                inimigo.dir = (1, v)
                inimigo.left[0] -= inimigo.vel
        if inimigo.dir[0] != -1 and inimigo.animar:
            # Inimigo se move
            visao = inimigo.visao*width
            inimigo.sector = 'walk'
            if inimigo.dir[0] == 0:
                inimigo.rect.x += inimigo.dir[1]
                if inimigo.dir[1] >= 0: inimigo.flip = True
                else: inimigo.flip = False
                undo = True
                for x in chao_sprite.sprites():
                    if pygame.sprite.collide_mask(x, inimigo):
                        undo = False
                        break
                if undo and not -100 <inimigo.rect.x > width-100:
                    inimigo.busy = True
                    if personagem.rect.y-inimigo.rect.y > 0:
                        sinal = 0
                    else: sinal = 1
                    inimigo.left = [0, min(visao, abs(personagem.rect.y-inimigo.rect.y)), sinal]
                    inimigo.rect.x -= inimigo.dir[1]
            elif inimigo.dir[0] == 1 and inimigo.rect.bottomleft[1] + inimigo.dir[1] <= height:
                inimigo.rect.y += inimigo.dir[1]
                undo = True
                for x in chao_sprite.sprites():
                    if pygame.sprite.collide_mask(x, inimigo):
                        undo = False
                        break
                if undo:
                    inimigo.busy = True
                    if personagem.rect.x-inimigo.rect.x > 0:
                        sinal = 0
                    else: sinal = 1
                    inimigo.left = [min(visao, abs(personagem.rect.x-inimigo.rect.x)), 0, sinal]
                    inimigo.rect.y -= inimigo.dir[1]

        if inimigo.dead:
            # Inimigo morreu
            personagem.exp += inimigo.exp
            inimigo.kill()
            drop = inimigo.drop()
            lista_sprites.add(drop)
            drops.add(drop)
            personagem.upar()
    if personagem.ataque:
        personagem.ataque = False

    for boss in bosses:
        if boss.rect.x - personagem.rect.x <= width:
            # Caso o boss esteja proximo mostra sua barra de vida
            boss_lbl(boss)

    for x in pygame.sprite.spritecollide(personagem, drops, False):
        # Recolhe drops
        personagem.coins += x.value
        x.kill()

    health_bar(personagem)
    level(personagem)
    dados(personagem)
    pygame.display.flip()
