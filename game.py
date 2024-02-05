import pygame
from pygame.locals import *
from codigos.ambiente.gerenciador_musicas import GerenciadorMusica
from codigos.ambiente.sons import mercador_saudar
from codigos.entidades.personagem import Personagem
from codigos.variaveis import screen_size, imortal, block_size, colide, \
    colide_tolerancia as tolerancia, tamanho_barra_itens, console, efeitos, load_config
from codigos.mapa.cenarios import gerar_cenarios
from codigos.entidades.bosses import boss_group
from codigos.interfaces.menu import level_up, mercado
from codigos.outros.auxiliares import level as le, dados as da, \
    boss_lbl as bl, health_bar as hb, info, update_grupos, update_to_draw, \
    update_pos, grupo_menu, dead, alerta_level_up, deletar_save, mudar_cenario
from codigos.mapa.backgrounds import backgrounds
from codigos.entidades.gerador import get_mercadores, get_npcs, get_inimigos
from codigos.outros.armazenamento import ler, escrever
from threading import Thread
from codigos.command_line import CommandLine
from codigos.outros.tradutor import Tradutor

pygame.init()
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
pygame.mixer.pre_init(44100, 16, 2, 4096)

width, height = screen_size
size = screen_size

# Inicializando cenarios
cenarios = {}
t = Thread(target=gerar_cenarios, args=[cenarios])
t.start()

gerenciador_musica = GerenciadorMusica()

# Grupos de sprites
inimigos = pygame.sprite.Group()
npcs = pygame.sprite.Group()
drops = pygame.sprite.Group()
lista_sprites = pygame.sprite.Group()
bosses = pygame.sprite.Group()
sprites_update = pygame.sprite.Group()
sprites_draw = pygame.sprite.Group()
sprites_menu = pygame.sprite.Group()
sprites_buffer = pygame.sprite.Group()
spell_sprites = pygame.sprite.Group()
alertas = pygame.sprite.Group()

personagem = Personagem()
lista_sprites.add(personagem)
dir = (-1, personagem.vel)
# Dir representa o vetor que move o personagem
# Index 0                            Index 1
# -1 não move, 0->x, 1->y, 2->x e y, Velocidade do movimento


def inicializar():
    """Lê os dados do armazenamento para inicializar o jogo"""
    global cenario, sprites_menu

    tradutor.reload()
    personagem.__init__((width + block_size[0], height // 2))
    personagem.rect.bottomleft = block_size[0], height // 2

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
            npcs.add(x)
            lista_sprites.add(x)

        for y in get_npcs():
            npcs.add(y)
            lista_sprites.add(y)

    update_grupos(personagem, lista_sprites, sprites_update, sprites_draw)
    sprites_menu = grupo_menu(personagem, tamanho_barra_itens)

    for b in bosses.sprites():
        if b.lock is not None:
            cenarios[b.lock].lock = True

    if imortal:
        personagem.vida, personagem.vida_max = 2 ** 32, 2 ** 32


tela = pygame.display.set_mode(size)
pygame.display.set_caption('Foreign Lands')
relogio = pygame.time.Clock()


# Funcoes que desenham informacoes na tela


def level(target, ajuste=(-14, -8)): le(target, tela, ajuste)


def dados(target): da(target, personagem, tela, tl)


def boss_lbl(target): bl(target, tela)


def health_bar(target): hb(target, tela)


t.join()
cenario = 0, 0
cenarios_seguros = [(0, 0)]  # Bloqueia a atualização de monstros

tradutor = Tradutor()
def tl(frase):
    """Traduz determinada frase do portugues para o idioma das configuracoes"""
    return tradutor.traduzir(frase)


def run():
    """Executa o jogo"""
    global cenario, chao_sprite, dir, t_musicas
    load_config()
    from codigos.variaveis import fps

    inicializar()

    chao_sprite = cenarios[cenario].grupo

    linha_comandos = thread_comandos = None
    is_run = True
    nivel_base = personagem.nivel

    t_musicas = Thread(target=gerenciador_musica.run, args=[cenario])
    t_musicas.start()

    sfx_t = Thread(target=gerenciador_musica.effect_thread, args=[])
    sfx_t.start()

    if console:
        linha_comandos = CommandLine(cenarios, lista_sprites, sprites_buffer, tl)
        thread_comandos = Thread(target=linha_comandos.run)
        thread_comandos.start()

    while is_run:
        # Laço principal do jogo
        relogio.tick(fps)
        tela.blit(backgrounds[cenarios[cenario].background], (0, 0))
        t2 = Thread(target=chao_sprite.draw, args=[tela])
        t2.start()
        sprites_menu = grupo_menu(personagem, tamanho_barra_itens)
        MOUSE_POS = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # Recebe os eventos da tela
            if event.type == QUIT:
                is_run = False
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
                    level_up(personagem, tl)
                if pygame.key.get_pressed()[K_r]:
                    # Tenta reviver o personagem
                    personagem.reviver_custo()
                if pygame.key.get_pressed()[K_e]:
                    # Interage com Npc
                    for sprite in npcs.sprites():
                        if type(sprite).__name__ == 'Mercador':
                            if pygame.sprite.collide_mask(personagem, sprite):
                                # Abre o menu de mercado deste mercador
                                mercado(personagem, sprite, tl)
                                if efeitos:
                                    mercador_saudar.play()
                                break
                if pygame.key.get_pressed()[K_ESCAPE]:
                    is_run = False
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
                clicou = False
                for sprite in sprites_menu:
                    if sprite.rect.collidepoint(x, y):
                        sprite.usar(personagem)
                        clicou = True
                if not clicou:
                    if event.button == 1:
                        personagem.attack()
        for sprite in sprites_menu:
            # Mostra tooltip(informações) de um item quando o mouse estiver acima dele
            if sprite.rect.collidepoint(MOUSE_POS[0], MOUSE_POS[1]):
                tooltip = sprite.get_tooltip()
                if tooltip is not None:
                    tela.blit(tooltip, (sprite.rect.topleft[0],
                                        sprite.rect.topleft[1] - tooltip.get_height())
                              )

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

        # Verificar colisao com portais e executar mudança

        if dir[0] != -1:
            # Movimentação do personagem
            mudanca = personagem.mover(dir, cenarios[cenario].tem_bloco, cenarios[cenario].tem_bloqueio)

            targets, cenario = mudar_cenario(mudanca, cenario, cenarios, personagem)
            # Dada a validação do movimento, muda de cenário e atualiza as posições
            if targets is not None:
                chao_sprite = cenarios[cenario].grupo
                # Atualização das posições das entidades
                t4 = Thread(target=update_pos, args=[targets, inimigos, drops, npcs])
                t4.start()
                # Atualização dos grupos update e draw
                t3 = Thread(target=update_grupos, args=[personagem, lista_sprites, sprites_update, sprites_draw, t4])
                t3.start()
                # Chamada do gerenciador de musica
                t_musicas.join()
                t_musicas = Thread(target=gerenciador_musica.run, args=[cenario])
                t_musicas.start()

        sprites_update.update()
        sprites_draw.draw(tela)
        sprites_menu.draw(tela)
        spell_sprites.update()
        spell_sprites.draw(tela)
        for sprite in sprites_draw.sprites():
            if sprite.tipo not in ['balao', 'decorativo', 'pocao', 'projetil']:
                health_bar(sprite)
            if sprite.tipo == 'projetil':
                # Verifica colisão do projetil com o jogador
                if pygame.sprite.collide_mask(sprite, personagem):
                    sprite.colidiu(personagem)

        t5 = Thread(target=update_to_draw, args=[personagem.rect, sprites_update, sprites_draw])
        t5.start()

        # Joga as sprites do buffer de comandos para as listas de uso
        for x in sprites_buffer:
            sprites_update.add(x)
            sprites_buffer.remove(x)

        for inimigo in [x for x in sprites_update.sprites() if (x.tipo == 'monster' or x.tipo == 'boss')]:
            # Itera sobre os inimigos que estão no range de update
            if pygame.sprite.collide_mask(inimigo, personagem.sprite_ataque()) is not None:
                if personagem.ataque:
                    # Personagem ataca inimigo em seu alcance
                    inimigo.vida -= personagem.dano
            if pygame.sprite.collide_mask(inimigo.ataque_sprite(), personagem) is not None:
                # Inimigo colide com o personagem
                if personagem.vida >= 0:
                    # Inicia um movimento de ataquea
                    inimigo.atacar()
                inimigo.dir = 0, 0
                if inimigo.ataque:
                    # Movimento de ataque bem sucedido
                    if not pygame.mixer.Channel(0).get_busy():
                        inimigo.play_sound('hit')

                    if inimigo.ataque_critico:
                        personagem.vida -= inimigo.dano_critico
                        personagem.curando = False
                    else:
                        personagem.vida -= inimigo.dano
                        personagem.curando = False

                    if personagem.vida <= 0:
                        gerenciador_musica.play_death()
                    inimigo.ataque = False
                elif inimigo.ataque:
                    # Movimento de ataque errou
                    inimigo.ataque = False

            inimigo.ataque = False

            # Processos de geracao de spells
            if inimigo.has_spell:
                if inimigo.spelling:
                    if pygame.sprite.collide_rect_ratio(inimigo.spell_range)(inimigo, personagem):
                        spell_sprites.add(inimigo.get_spell())
                    inimigo.spelling = False

            # Verifica se o personagem está no campo de visão do inimigo
            seguir = False
            if abs(personagem.rect.centerx - inimigo.rect.centerx) + abs \
                        (personagem.rect.centery - inimigo.rect.centery) <= inimigo.visao * width \
                    and personagem.vida >= 0:
                seguir = True

            # Age a partir da verificação acima
            if seguir:
                # Seu dir representa a distancia que andará em cada direção
                if not pygame.mixer.Channel(0).get_busy():
                    inimigo.play_sound('find')
                inimigo.dir = inimigo.rect.centerx - personagem.rect.centerx, inimigo.rect.centery - personagem.rect.centery
                inimigo.busy = True
            else:
                inimigo.busy = False
                inimigo.rand_walk()

            # Movimentação do inimigo
            if cenario not in cenarios_seguros:
                inimigo.mover(cenarios[cenario].tem_bloco, cenarios[cenario].tem_bloqueio, sprites_update.sprites())
                cenarios[cenario].aplicar_efeitos(inimigo)

            # Morte do inimigo
            if inimigo.dead:
                inimigo.play_sound('death')
                if inimigo.is_boss:
                    # Desbloqueia a saida do cenario que o boss referencia
                    personagem.desbloqueio.append(inimigo.lock)
                    for x in inimigo.unlocks:
                        personagem.acesso.append(x)
                personagem.exp += inimigo.exp * (1 + personagem.inteligencia/100)
                inimigo.kill()
                for drop in inimigo.drop(sorte=personagem.sorte):
                    lista_sprites.add(drop)
                    sprites_draw.add(drop)
                    sprites_update.add(drop)
                    drops.add(drop)
                personagem.upar()

        if personagem.ataque:
            # Cancela o ataque do personagem
            personagem.ataque = False

        for boss in bosses:
            if abs(boss.rect.x - personagem.rect.x) <= width and abs(boss.rect.y - personagem.rect.y) <= height:
                # Caso o boss esteja proximo mostra sua barra de vida
                boss_lbl(boss)

        for x in pygame.sprite.spritecollide(personagem, drops, False):
            # Recolhe drops
            if type(x).__name__ == 'Coin':
                personagem.coins += x.value
            else:
                personagem.add_item(x)
            x.kill()

        for npc in npcs.sprites():
            if type(npc).__name__ != 'Balao':
                npc.proximidade(personagem)
                # health_bar(npc)
                level(npc, (0, 0))

        for spell in spell_sprites.sprites():
            spell.rect = personagem.rect
            if spell.end:
                personagem.vida -= spell.dmg
                personagem.curando = False
                spell.kill()

        cenarios[cenario].aplicar_efeitos(personagem)
        t5.join()

        if personagem.is_dead():
            dead(personagem, tela, tl)
        level(personagem)
        dados(personagem)
        info(cenario, personagem, tela, relogio.get_fps())
        nivel_base = alerta_level_up(alertas, nivel_base, personagem.nivel, tl)
        alertas.draw(tela)
        pygame.display.flip()

    # Encerrando o modulo
    gerenciador_musica.stop()
    if not personagem.is_dead():
        escrever(personagem, inimigos, npcs, cenario)
    else:
        deletar_save('player_data.json')

    t_musicas.join()
    sfx_t.join()

    if console:
        linha_comandos.end()
        thread_comandos.join(timeout=1)
    # pygame.quit()  # Remover na versão release
