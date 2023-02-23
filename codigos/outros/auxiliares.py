# Este arquivo contém funções auxiliares usadas pelo programa
import pygame.transform
from codigos.variaveis import screen_size, info as info_s, update_range as ur, draw_range as dr
from codigos.ambiente.textuais import fonte1, fonte2, vermelho, verde, preto, amarelo

width, height = screen_size
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


def level(target, tela, ajuste=(-14, -8)):
    '''Mostra o nível do jogador na tela'''
    nivel = target.nivel
    pos = target.rect.centerx+ajuste[0], target.rect.centery+ajuste[1]
    formatado = fonte1.render(str(nivel), True, vermelho)
    tela.blit(formatado, pos)


def dados(target, personagem, tela):
    '''Mostra dados do jogador na tela'''
    atual, restante = int(target.exp), int(target.niveis[target.nivel])
    formatado = fonte2.render(f'{atual}/{restante} XP', True, verde)
    if personagem.coins == 0 or personagem.coins>1:
        adj = 's'
    else: adj = ''
    budget = fonte2.render(f'{personagem.coins} coin{adj}', True, amarelo)
    tela.blit(formatado, (width-formatado.get_width(), 0))
    tela.blit(budget, (width-budget.get_width(), formatado.get_height()))


def boss_lbl(target, tela):
    pos = width//2, 0
    prop = target.vida/target.vida_max
    pygame.draw.line(tela, vermelho, pos, (pos[0], pos[1]+15), 300)
    if prop > 0:
        pygame.draw.line(tela, verde, pos, (pos[0], pos[1]+15), int(300*prop))


def health_bar(target, tela):
    '''Mostra na tela a barra de vida da entidade target'''
    size = 12
    pos = target.rect.center
    prop = target.vida/target.vida_max
    pygame.draw.line(tela, vermelho, pos, (pos[0]+size, pos[1]))
    if prop > 0:
        pygame.draw.line(tela, verde, pos, (pos[0]+int(size*prop), pos[1]))


def info(num, personagem, tela, fps):
    """Mostra o numero do cenario na tela"""
    if info_s:
        val = fonte1.render(f'X: {num[0]}, Y: {num[1]}', True, preto)
        val2 = fonte1.render(f'W: {personagem.rect.centerx}, H: {personagem.rect.centery}', True, preto)
        val3 = fonte1.render('Fps: '+str(int(fps)), True, preto)
        tela.blit(val, (0, 0))
        tela.blit(val2, (0, val.get_height()))
        tela.blit(val3, (0, val.get_height()*2))


def update_grupos(pers, todas, updt, draw, t_wait=None):
    """Calcula quais entidaddes receberam update e/ou draw,
    aguarda a thread t_wait finalizar para iniciar"""
    if t_wait is not None:
        t_wait.join()
    x, y = pers.rect.centerx, pers.rect.centery
    updt.empty()
    draw.empty()
    for sprite in todas.sprites():
        # E as falas dos npcs ?
        if sprite != pers:
            dx, dy = abs(x-sprite.rect.centerx), abs(y-sprite.rect.centery)
            if dx <= ur[0] and dy <= ur[1]:
                updt.add(sprite)
            if dx <= dr[0] and dy <= dr[1]:
                draw.add(sprite)

    updt.add(pers)
    draw.add(pers)
    print(updt, draw)
    return updt, draw


def update_to_draw(rect, updt, draw):
    """Atualiza as listas de sprites ja geradas"""
    for inimigo in updt.sprites():
        dx, dy = abs(rect.centerx - inimigo.rect.centerx), abs(rect.centery - inimigo.rect.centery)
        if dx <= dr[0] and dy <= dr[1]:
            if inimigo not in draw.sprites():
                draw.add(inimigo)
        if not(dx <= ur[0] and dy <= ur[1]):
            updt.remove(inimigo)


def update_pos(target, inimigos, drops, npcs):
    if target is not None:
        t, v = target
        for i in inimigos.sprites():
            setattr(getattr(i, 'rect'), t, getattr(getattr(i, 'rect'), t) + v)
        for i in drops.sprites():
            setattr(getattr(i, 'rect'), t, getattr(getattr(i, 'rect'), t) + v)
        for i in npcs.sprites():
            setattr(getattr(i, 'rect'), t, getattr(getattr(i, 'rect'), t) + v)
            if i.falando:
                i.fala.kill()


def grupo_menu(personagem, tam):
    grupo = pygame.sprite.Group()
    r = (1-tam)/2
    acresc = 64
    mn, mx = width*r, width*(r+tam)
    i = mn
    for x in personagem.inventario:
        if x.tipo == 'pocao':
            x.rect.bottomleft = i, height-1
            grupo.add(x)
            i += acresc
    return grupo