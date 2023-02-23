import pygame
from pygame.locals import *
from sys import exit
from codigos.entidades.personagem import Personagem
from codigos.variaveis import screen_size, musica, imortal, block_size, colide, fps, \
    colide_tolerancia as tolerancia, tamanho_barra_itens
from codigos.mapa.cenarios import gerar_cenarios
from codigos.entidades.bosses import boss_group
from codigos.interfaces.menu import level_up, mercado
from codigos.outros.auxiliares import level as le, dados as da, \
    boss_lbl as bl, health_bar as hb, info, update_grupos, update_to_draw, update_pos, grupo_menu
from codigos.mapa.backgrounds import backgrounds
from codigos.entidades.gerador import get_mercadores, get_npcs, get_inimigos
from codigos.outros.armazenamento import ler, escrever
from threading import Thread

pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

width, height = screen_size
size = screen_size

cenarios = {}
t = Thread(target=gerar_cenarios, args=[cenarios])
t.start()

if musica:
    pygame.mixer.music.load('arquivos/sons/musicas/The_Old_Tower_Inn.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)

inimigos = pygame.sprite.Group()
npcs = pygame.sprite.Group()
drops = pygame.sprite.Group()
lista_sprites = pygame.sprite.Group()
bosses = pygame.sprite.Group()
sprites_update = pygame.sprite.Group()
sprites_draw = pygame.sprite.Group()
sprites_menu = pygame.sprite.Group()

personagem = Personagem((width + block_size[0], height // 2))
personagem.rect.bottomleft = block_size[0], height // 2
lista_sprites.add(personagem)
dir = (-1, personagem.vel)
# -1 não move, 0 x, 1 y,2 x e y, index 1->velocidade x, index 2 velocidade y

# Leitura do armazenamento
leitura, cenario = ler(personagem, inimigos, npcs, bosses)
for sprite in inimigos.sprites():
    lista_sprites.add(sprite)
for npc in npcs.sprites():
    lista_sprites.add(npc)

# Geração das entidades do jogo
if not leitura:
    get_inimigos(inimigos)
    boss_group(lista_sprites, inimigos, bosses)
    for sprite in inimigos.sprites():
        lista_sprites.add(sprite)

    for x in get_mercadores():
        mercador = x
        npcs.add(x)
        lista_sprites.add(x)

    for y in get_npcs():
        npc = y
        npcs.add(y)
        lista_sprites.add(y)

tela = pygame.display.set_mode(size)
pygame.display.set_caption('RPG Pygame')
relogio = pygame.time.Clock()


# Funcoes que desenham informacoes na tela


def level(target, ajuste=(-14, -8)): le(target, tela, ajuste)


def dados(target): da(target, personagem, tela)


def boss_lbl(target): bl(target, tela)


def health_bar(target): hb(target, tela)


update_grupos(personagem, lista_sprites, sprites_update, sprites_draw)

if imortal:
    personagem.vida, personagem.vida_max = 2 ** 32, 2 ** 32

t.join()
chao_sprite = cenarios[cenario].grupo

for b in bosses.sprites():
    if b.lock is not None:
        cenarios[b.lock].lock = True

# Exibição dos itens utilizaveis do personagem
sprites_menu = grupo_menu(personagem, tamanho_barra_itens)

while 1:
    # Laço principal do jogo
    relogio.tick(fps)
    tela.blit(backgrounds[cenarios[cenario].background], (0, 0))
    t2 = Thread(target=chao_sprite.draw, args=[tela])
    t2.start()
    for event in pygame.event.get():
        # Recebe os eventos da tela
        if event.type == QUIT:
            escrever(personagem, inimigos, npcs, cenario)
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                personagem.attack()
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
            if pygame.key.get_pressed()[K_e]:
                # Interage com Npc
                for sprite in npcs.sprites():
                    if type(sprite).__name__ == 'Mercador':
                        if pygame.sprite.collide_mask(personagem, sprite):
                            # Abre o menu de mercado deste mercador
                            mercado(personagem, sprite)
                            sprites_menu = grupo_menu(personagem, tamanho_barra_itens)
                        break
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
                    if event.key == K_s or event.key == K_w:
                        dir = 0, dir[1]
                    elif event.key == K_d or event.key == K_a:
                        dir = 1, dir[2]
                    else:
                        stop = True
            if stop:
                dir = (-1, 0)
                personagem.idle()
        elif event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            for sprite in sprites_menu:
                if sprite.rect.collidepoint(x, y):
                    print('clicou')
                    sprite.usar(personagem)

    for x in pygame.sprite.spritecollide(personagem, sprites_draw, False):
        # Verifica se alguma entidade bloqueia movimento do personagem
        if x != personagem:
            if pygame.sprite.collide_mask(personagem, x):
                # Aplica condicionais para ver se ha de fato bloqueio
                dx = personagem.rect.centerx - x.rect.centerx
                dy = personagem.rect.centery - x.rect.centery

                cond1 = dx - personagem.vel <= 0 and dir[0] == 0 and dir[1] >= 0
                cond2 = personagem.vel - dx <= 0 and dir[0] == 0 and dir[1] <= 0
                cond3 = dy - personagem.vel <= 0 and dir[0] == 1 and dir[1] >= 0
                cond4 = personagem.vel - dy <= 0 and dir[0] == 1 and dir[1] <= 0
                cond5 = abs(dx) >= tolerancia and abs(dy) >= tolerancia
                if (cond1 or cond2 or cond3 or cond4) and colide and (not cond5):
                    dir = -1, dir[1]

    t2.join()

    if dir[0] != -1:
        # Movimentação do personagem
        mudanca = personagem.mover(dir, cenarios[cenario].tem_bloco, cenarios[cenario].tem_bloqueio)
        if (mudanca is not None) and ((not cenarios[cenario].lock) or cenario in personagem.desbloqueio):
            # Tenta mudar de cenário
            target = None
            if mudanca[0] == 0:
                if (cenario[0] + mudanca[1], cenario[1]) in cenarios:
                    if cenarios[(cenario[0] + mudanca[1], cenario[1])].acesso or (cenario[0] + mudanca[1], cenario[1]) \
                            in personagem.desbloqueio:
                        target = 'centerx', width * (-1 * mudanca[1])
                        cenario = (cenario[0] + mudanca[1], cenario[1])
                        if mudanca[1] > 0:
                            personagem.rect.bottomleft = 0, personagem.rect.bottomleft[1]
                        else:
                            personagem.rect.topright = width, personagem.rect.topright[1]
            elif mudanca[0] == 1:
                if (cenario[0], cenario[1] + mudanca[1]) in cenarios:
                    if cenarios[(cenario[0], cenario[1] + mudanca[1])].acesso or (cenario[0], cenario[1] + mudanca[1]) \
                            in personagem.desbloqueio:
                        target = 'centery', height * (-1 * mudanca[1])
                        cenario = (cenario[0], cenario[1] + mudanca[1])
                        if mudanca[1] > 0:
                            personagem.rect.bottomleft = personagem.rect.bottomleft[0], 96
                        else:
                            personagem.rect.bottomleft = personagem.rect.bottomleft[0], height - 1
            chao_sprite = cenarios[cenario].grupo
            # Atualização das posições das entidades
            t4 = Thread(target=update_pos, args=[target, inimigos, drops, npcs])
            t4.start()
            # Atualização dos grupos update e draw
            t3 = Thread(target=update_grupos, args=[personagem, lista_sprites, sprites_update, sprites_draw, t4])
            t3.start()

    sprites_update.update()
    sprites_draw.draw(tela)
    sprites_menu.draw(tela)
    for sprite in sprites_draw.sprites():
        if sprite.tipo not in ['balao', 'decorativo']:
            health_bar(sprite)

    t4 = Thread(target=update_to_draw, args=[personagem.rect, sprites_update, sprites_draw])
    t4.start()

    # Processos dos inimigos
    for inimigo in [x for x in sprites_update.sprites() if (x.tipo == 'monster' or x.tipo == 'boss')]:
        # Itera sobre os inimigos que estão no range de update
        if pygame.sprite.collide_mask(inimigo, personagem.sprite_ataque()) is not None:
            if personagem.ataque:
                # Personagem ataca inimigo em seu alcance
                inimigo.vida -= personagem.dano
        if pygame.sprite.collide_mask(inimigo.ataque_sprite(), personagem) is not None:
            # Inimigo colide com o personagem
            if personagem.vida >= 0:
                # Inicia um movimento de ataque
                inimigo.atacar()
            inimigo.dir = 0, 0
            if inimigo.ataque:
                # Movimento de ataque bem sucedido
                personagem.vida -= inimigo.dano
                inimigo.ataque = False
            elif inimigo.ataque:
                # Movimento de ataque errou
                inimigo.ataque = False

        # Verifica se o personagem está no campo de visão do inimigo
        seguir = False
        if abs(personagem.rect.centerx - inimigo.rect.centerx) + abs \
                    (personagem.rect.centery - inimigo.rect.centery) <= inimigo.visao * width \
                and personagem.vida >= 0:
            seguir = True

        # Age a partir da verificação acima
        if seguir:
            # Seu dir representa a distancia que andará em cada direção
            inimigo.dir = inimigo.rect.centerx - personagem.rect.centerx, inimigo.rect.centery - personagem.rect.centery
            inimigo.busy = True
        else:
            inimigo.busy = False
            inimigo.rand_walk()

        # Movimentação do inimigo
        inimigo.mover(cenarios[cenario].tem_bloco, cenarios[cenario].tem_bloqueio)

        # Morte do inimigo
        if inimigo.dead:
            if inimigo.is_boss:
                # Desbloqueia a saida do cenario que o boss referencia
                personagem.desbloqueio.append(inimigo.lock)
                for x in inimigo.unlocks:
                    personagem.acesso.append(x)
            personagem.exp += inimigo.exp
            inimigo.kill()
            drop = inimigo.drop()
            lista_sprites.add(drop)
            sprites_draw.add(drop)
            sprites_update.add(drop)
            drops.add(drop)
            personagem.upar()

    if personagem.ataque:
        # Cancela o ataque do personagem
        personagem.ataque = False

    for boss in bosses:
        if boss.rect.x - personagem.rect.x <= width:
            # Caso o boss esteja proximo mostra sua barra de vida
            boss_lbl(boss)

    for x in pygame.sprite.spritecollide(personagem, drops, False):
        # Recolhe drops
        personagem.coins += x.value
        x.kill()

    for npc in npcs.sprites():
        if type(npc).__name__ != 'Balao':
            npc.proximidade(personagem)
            # health_bar(npc)
            level(npc, (0, 0))

    level(personagem)
    dados(personagem)
    info(cenario, personagem, tela, relogio.get_fps())
    pygame.display.flip()
