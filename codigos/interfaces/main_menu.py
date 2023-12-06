# Adaptado em cim do código do seguinte repositório;
# https://github.com/baraltech/Menu-System-PyGame/tree/main
import json
import os
from importlib import reload
from random import randint
import pygame
import sys
import editor_cenario
from .button import Button
from codigos.variaveis import screen_size, fps
from ..entidades.personagem import Personagem
from codigos.outros.tradutor import Tradutor

pygame.init()

cur_dir = 'arquivos/'
BG = pygame.image.load(cur_dir + 'interfaces/Background.png')


def return_true(x):
    return True


def return_false(x):
    return False


def get_font(size):
    """Retorna o tamanho da fonte"""
    return pygame.font.Font(cur_dir + "interfaces/font.ttf", size)


def main_menu():
    """Roda o menu inicial do jogo"""
    W, H = screen_size

    tradutor = Tradutor()

    def tl(x):
        return tradutor.traduzir(x)

    SCREEN = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Menu")
    relogio = pygame.time.Clock()

    sprites = pygame.sprite.Group()
    personagem = Personagem((W * 0.35, 0.90 * H))
    p_dir = 0, 1
    sprites.add(personagem)
    while 1:
        relogio.tick(fps)
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(int(0.0001 * (W * H))).render(tl("Foreign lands"), True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(W // 2, 0.13 * H))

        PLAY_BUTTON = Button(
            image=pygame.transform.scale(pygame.image.load(cur_dir + "interfaces/Play Rect.png"), (0.28 * W, 0.15 * H)),
            pos=(W // 2, 0.34 * H), text_input=tl("jogar"), font=get_font(int(0.00008 * (W * H))),
            base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(
            image=pygame.transform.scale(pygame.image.load(cur_dir + "interfaces/Play Rect.png"), (0.28 * W, 0.15 * H)),
            pos=(W // 2, 0.5 * H), text_input=tl("opcoes"), font=get_font(int(0.00008 * (W * H))),
            base_color="#d7fcd4", hovering_color="White")
        EDITOR_BUTTON = Button(
            image=pygame.transform.scale(pygame.image.load(cur_dir + "interfaces/Play Rect.png"), (0.28 * W, 0.15 * H)),
            pos=(W // 2, 0.66 * H), text_input=tl("cenários"), font=get_font(int(0.00008 * (W * H))),
            base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(
            image=pygame.transform.scale(pygame.image.load(cur_dir + "interfaces/Play Rect.png"), (0.28 * W, 0.15 * H)),
            pos=(W // 2, 0.82 * H), text_input=tl("sair"), font=get_font(int(0.00008 * (W * H))),
            base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, EDITOR_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            """Recebe os eventos de click"""
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Essa sessão precisa ser otimizada, o jogo está sendo carregado duas vezes
                    import game
                    reload(game)
                    game.run()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    tradutor.load(options())
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if EDITOR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    editor_cenario.run()

        # Animacoes
        sprites.draw(SCREEN)
        sprites.update()
        if randint(1, 400) == 10:
            personagem.attack()
        elif randint(1, 400) == 10:
            personagem.pular()
        else:
            # Move o personagem para direita e esquerda
            if personagem.rect.centerx > W * 0.8:
                p_dir = 0, -1
            if personagem.rect.centerx < W * 0.2:
                p_dir = 0, 1
            personagem.mover(p_dir, return_true, return_false)
        pygame.display.update()


def options():
    """Exibe o menu de opções"""
    W, H = screen_size
    data = get_base_config()
    if data['sons']['musica']:
        musica = True, 'Ligado'
    else:
        musica = False, 'Desligado'

    if data['sons']['efeitos']:
        efeitos = True, 'Ligado'
    else:
        efeitos = False, 'Desligado'

    if data['load_save']:
        carregar = True, 'Ligado'
    else:
        carregar = False, 'Desligado'

    idioma = data['idioma']
    fps = data['fps']
    idi_tab = False

    IDIOMAS = get_idiomas_tab()
    idioma_buttons = []
    idioma_buttons_x = W * 0.8
    idioma_buttons_y = 0.50 * H

    fps_30_cor = fps_60_cor = 'Black'
    if fps == 30:
        fps_30_cor = 'Red'
    elif fps == 60:
        fps_60_cor = 'Red'

    for x in IDIOMAS:
        button = Button(image=None, pos=(idioma_buttons_x, idioma_buttons_y),
                        text_input=x, font=get_font(int(0.00004*W*H)),
                        base_color="Black", hovering_color="Green")
        idioma_buttons.append(button)
        idioma_buttons_y += 0.10 * H

    tradutor = Tradutor()

    def tl(x):
        return tradutor.traduzir(x)

    SCREEN = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Menu")

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("gray")

        OPTIONS_TEXT = get_font(int(0.00008*W*H)).render(tl("Opções de jogo"), True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(W//2, 0.10*H))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        MUSICA = get_font(int(0.00004*W*H)).render(tl("Musica")+":", True, "Black")
        MUSICA_RECT = OPTIONS_TEXT.get_rect(center=(W//2, 0.20*H))
        SCREEN.blit(MUSICA, MUSICA_RECT)
        MUSICA_ON = Button(image=None, pos=(W*0.6, 0.20*H),
                              text_input=tl(musica[1]), font=get_font(int(0.00004*W*H)), base_color="Black", hovering_color="Green")
        MUSICA_ON.changeColor(OPTIONS_MOUSE_POS)
        MUSICA_ON.update(SCREEN)

        EFEITOS = get_font(int(0.00004*W*H)).render(tl("Efeitos")+":", True, "Black")
        EFEITOS_RECT = OPTIONS_TEXT.get_rect(center=(W//2, 0.30*H))
        SCREEN.blit(EFEITOS, EFEITOS_RECT)
        EFEITOS_ON = Button(image=None, pos=(W*0.6, 0.30*H),
                              text_input=tl(efeitos[1]), font=get_font(int(0.00004*W*H)), base_color="Black", hovering_color="Green")
        EFEITOS_ON.changeColor(OPTIONS_MOUSE_POS)
        EFEITOS_ON.update(SCREEN)

        CARREGAR = get_font(int(0.00004*W*H)).render(tl("Carregar"), True, "Black")
        CARREGAR_RECT = OPTIONS_TEXT.get_rect(center=(W//2, 0.40*H))
        SCREEN.blit(CARREGAR, CARREGAR_RECT)
        CARREGAR_ON = Button(image=None, pos=(W*0.6, 0.40*H),
                              text_input=tl(carregar[1]), font=get_font(int(0.00004*W*H)), base_color="Black", hovering_color="Green")
        CARREGAR_ON.changeColor(OPTIONS_MOUSE_POS)
        CARREGAR_ON.update(SCREEN)

        IDIOMA = get_font(int(0.00004*W*H)).render(tl("Idioma")+":", True, "Black")
        IDIOMA_RECT = OPTIONS_TEXT.get_rect(center=(W//2, 0.50*H))
        SCREEN.blit(IDIOMA, IDIOMA_RECT)
        IDIOMA_ON = Button(image=None, pos=(W*0.6, 0.50*H),
                              text_input=idioma, font=get_font(int(0.00004*W*H)), base_color="Black", hovering_color="Green")
        IDIOMA_ON.changeColor(OPTIONS_MOUSE_POS)
        IDIOMA_ON.update(SCREEN)

        if idi_tab:
            pygame.draw.rect(SCREEN, (0, 0, 125), (W * 0.7, 0.45*H, W * 0.2, 0.1*H*len(idioma_buttons)))
            for button in idioma_buttons:
                button.changeColor(OPTIONS_MOUSE_POS)
                button.update(SCREEN)

        FPS = get_font(int(0.00004*W*H)).render("Fps:", True, "Black")
        FPS_RECT = OPTIONS_TEXT.get_rect(center=(W//2, 0.60*H))
        SCREEN.blit(FPS, FPS_RECT)
        FPS_30 = Button(image=None, pos=(W*0.55, 0.60*H),
                              text_input='30', font=get_font(int(0.00004*W*H)), base_color=fps_30_cor, hovering_color="Green")
        FPS_30.changeColor(OPTIONS_MOUSE_POS)
        FPS_30.update(SCREEN)
        FPS_60 = Button(image=None, pos=(W*0.6, 0.60*H),
                              text_input='60', font=get_font(int(0.00004*W*H)), base_color=fps_60_cor, hovering_color="Green")
        FPS_60.changeColor(OPTIONS_MOUSE_POS)
        FPS_60.update(SCREEN)

        OBS_TEXT = get_font(int(0.00002*W*H)).render(tl("* "+"Troca de fps requer reinicio"), True, "Red")
        OBS_RECT = OPTIONS_TEXT.get_rect(center=(W*0.6, 0.70*H))
        SCREEN.blit(OBS_TEXT, OBS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(W//2, 0.80*H),
                              text_input="BACK", font=get_font(int(0.00004*W*H)), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write_config(musica, efeitos, carregar, idioma, fps)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    write_config(musica, efeitos, carregar, idioma, fps)
                    return idioma
                if IDIOMA_ON.checkForInput(OPTIONS_MOUSE_POS):
                    idi_tab = not idi_tab
                if FPS_30.checkForInput(OPTIONS_MOUSE_POS):
                    fps, fps_30_cor = 30, 'Red'
                    fps_60_cor = 'Black'
                if FPS_60.checkForInput(OPTIONS_MOUSE_POS):
                    fps, fps_60_cor = 60, 'Red'
                    fps_30_cor = 'Black'
                if MUSICA_ON.checkForInput(OPTIONS_MOUSE_POS):
                    if musica[0]:
                        musica = False, 'Desligado'
                    else:
                        musica = True, 'Ligado'
                if EFEITOS_ON.checkForInput(OPTIONS_MOUSE_POS):
                    if efeitos[0]:
                        efeitos = False, 'Desligado'
                    else:
                        efeitos = True, 'Ligado'
                if CARREGAR_ON.checkForInput(OPTIONS_MOUSE_POS):
                    if carregar[0]:
                        carregar = False, 'Desligado'
                    else:
                        carregar = True, 'Ligado'
                for botao in idioma_buttons:
                    if botao.checkForInput(OPTIONS_MOUSE_POS):
                        idioma = botao.text_input
                        tradutor.load(idioma)

        pygame.display.update()


def get_idiomas_tab():
    """Retorna a lista de idiomas disponíveis"""
    lista = ['portugues']
    diretorio = "arquivos/idiomas"
    if os.path.exists(diretorio) and os.path.isdir(diretorio):
        for arquivo in os.listdir(diretorio):
            if os.path.isfile(os.path.join(diretorio, arquivo)):
                lista.append(arquivo.replace('.json', ''))
    return lista

def write_config(musica, efeitos, carregar, idioma, fps):
    """Escreve as configurações no json"""
    data = {}
    try:
        with open('dados/configuracao.json', 'r') as arq:
            data = json.load(arq)
    except:
        pass
    if not data['sons']:
        data['sons'] = {}
    data['sons']['musica'] = musica[0]
    data['sons']['efeitos'] = efeitos[0]
    data['load_save'] = carregar[0]
    data['idioma'] = idioma
    data['fps'] = fps
    with open('dados/configuracao.json', 'w') as arq:
        json.dump(data, arq, indent=2)


def get_base_config():
    """Retorna as configurações atuais"""
    try:
        with open('dados/configuracao.json', 'r') as arq:
            data = json.load(arq)
    except:
        data = {
          "idioma": "portugues",
          "load_save": True,
          "sons": {
            "musica": True,
            "efeitos": True,
            "volume": 1
          },
          "console": True,
          "fps": 30
        }
    return data
