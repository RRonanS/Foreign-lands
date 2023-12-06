# Sistema para edição de cenários
import json
import jsbeautifier
import pygame
import PySimpleGUI as sg
from pygame.locals import *
from threading import Thread
from codigos.entidades.bosses import boss_group
from codigos.entidades.gerador import get_inimigos
from codigos.variaveis import screen_size, fps, block_size
from codigos.outros.auxiliares import info
from codigos.ambiente.textuais import fonte0, preto
from collections import defaultdict
from codigos.interfaces.button import Button

side_bar = False
if side_bar:
    barra_size = 200, 0
else:
    barra_size = 0, 0

pygame.init()
tela = pygame.display.set_mode((screen_size[0] + barra_size[0], screen_size[1] + barra_size[1]))
pygame.display.set_caption('Editor cenário')
relogio = pygame.time.Clock()
relogio.tick(fps)

options = jsbeautifier.default_options()
options.indent_size = 2
options.max_preserve_newlines = True

arq_entrada = 'dados/cenario_dev.json'
arq_destino = 'dados/cenario_dev.json'

from codigos.mapa.cenarios import gerar_cenarios

cenarios = {}
gerar_cenarios(cenarios, arq_entrada)
monstros_sprites = pygame.sprite.Group()
cenario = [0, 0]  # Cenario atual
auto_save_delay = auto_save_atual = 600 * fps  # Delay para salvar automaticamente em segundos

W, H = screen_size
B_W, B_H = H // block_size[1], W // block_size[1]
bloco_selecionado = None
running = True
do_up_bloco = do_up_cenario = False
do_up_run = False


def get_font(size):
    """Retorna o tamanho da fonte"""
    return pygame.font.Font("arquivos/interfaces/font.ttf", size)


def draw_selected_rect(bloco, screen):
    """Desenha um retangulo verde ao redor do bloco selecionado"""
    if bloco is not None:
        # Obter as posições do bloco
        x, y = bloco.rect.topleft[0], bloco.rect.topleft[1]
        largura = bloco.rect.width
        altura = bloco.rect.height

        # Desenhar uma borda verde ao redor do bloco
        pygame.draw.rect(screen, (0, 255, 0), (x, y, largura, altura), 3)


def run():
    """Executa o programa de edição"""
    global bloco_selecionado, running, do_up_bloco, do_up_cenario, do_up_run, auto_save_atual, monstros_sprites

    exiting = False
    button_x, button_y = W * 0.4, H // 2
    exiting_menu = [
        Button(image=None, pos=(button_x, button_y),
               text_input='Salvar', font=get_font(int(0.00003 * W * H)),
               base_color="Blue", hovering_color="Green"),
        Button(image=None, pos=(button_x + 0.1 * W, button_y),
               text_input='Não salvar', font=get_font(int(0.00002 * W * H)),
               base_color="Red", hovering_color="Green"),
        Button(image=None, pos=(button_x + 0.2 * W, button_y),
               text_input='Cancelar', font=get_font(int(0.00003 * W * H)),
               base_color="Gray", hovering_color="Green")
    ]

    click_buttons = []
    if side_bar:
        button_x = W + barra_size[0] * 0.25
        button_y = 0.1 * W
        for img, classe in entity_imgs():
            click_buttons.append(Button(image=img, pos=(button_x, button_y),
                                        text_input=classe, font=get_font(int(0.00003 * W * H)),
                                        base_color="Blue", hovering_color="Green"))
            if button_x + barra_size[0] // 2 > barra_size[0] + W:
                button_y += img.get_height() * 1.2
                button_x = W + barra_size[0] * 0.3
            else:
                button_x += barra_size[0] // 2

    menu = Thread(target=menu_select)
    menu.start()

    get_inimigos(monstros_sprites)
    boss_group(monstros_sprites, pygame.sprite.Group, pygame.sprite.Group)
    # l_cmd = Thread(target=linha_comando_add)
    # l_cmd.start()

    t_salvar = None

    chao_sprite = cenarios[tuple(cenario)].grupo

    while running:
        MOUSE_POS = pygame.mouse.get_pos()
        if not exiting:
            auto_save_atual -= 1

        if auto_save_atual <= 0:
            # Salva automaticamente
            auto_save_atual = auto_save_delay
            if t_salvar is None:
                t_salvar = Thread(target=salvar_json, args=[cenarios])
                t_salvar.start()
            else:
                t_salvar.join()
                t_salvar = Thread(target=salvar_json, args=[cenarios])
                t_salvar.start()

        if do_up_run:
            # Atualiza o cenário atual com base na barra lateral
            chao_sprite = cenarios[tuple(cenario)].grupo
            do_up_run = False

        tela.fill(preto)
        chao_sprite.draw(tela)
        monstros_sprites.draw(tela)

        for event in pygame.event.get():
            if event.type == QUIT:
                exiting = True
            if event.type == MOUSEBUTTONDOWN:
                if exiting_menu[0].checkForInput(MOUSE_POS) and exiting:
                    # Salvar
                    try:
                        if t_salvar is not None:
                            t_salvar.join()
                        salvar_json(cenarios)
                        print('Cenários salvos com sucesso no arquivo', arq_destino)
                        # salvar_monstros()
                        # print('Monstros salvos com sucesso no arquivo', 'dados/monstros_dev.json')
                    except Exception as e:
                        print('Erro ao salvar:', e)
                    running = False
                elif exiting_menu[1].checkForInput(MOUSE_POS) and exiting:
                    # Sair sem salvar
                    running = False
                    exiting = False
                elif exiting_menu[2].checkForInput(MOUSE_POS) and exiting:
                    # Cancelar
                    exiting = False
                if pygame.mouse.get_pressed()[0]:
                    # Seleção de bloco
                    x, y = MOUSE_POS
                    temp = bloco_selecionado
                    bloco_selecionado = find_block(chao_sprite,
                                                   (x // block_size[0], y // block_size[1]))
                    if temp == bloco_selecionado:
                        bloco_selecionado = None
                    do_up_bloco = True
            if event.type == KEYDOWN:
                # Teclas de mudança de cenário
                if pygame.key.get_pressed()[K_ESCAPE]:
                    exiting = True
                if pygame.key.get_pressed()[K_d]:
                    cenario[0] += 1
                    if tuple(cenario) in cenarios:
                        chao_sprite = cenarios[tuple(cenario)].grupo
                        do_up_cenario = True
                        for x in monstros_sprites.sprites():
                            x.rect.centerx -= W
                    else:
                        cenario[0] -= 1
                if pygame.key.get_pressed()[K_a]:
                    cenario[0] -= 1
                    if tuple(cenario) in cenarios:
                        chao_sprite = cenarios[tuple(cenario)].grupo
                        do_up_cenario = True
                        for x in monstros_sprites.sprites():
                            x.rect.centerx += W
                    else:
                        cenario[0] += 1
                if pygame.key.get_pressed()[K_w]:
                    cenario[1] -= 1
                    if tuple(cenario) in cenarios:
                        chao_sprite = cenarios[tuple(cenario)].grupo
                        do_up_cenario = True
                        for x in monstros_sprites.sprites():
                            x.rect.centery += H
                    else:
                        cenario[1] += 1
                if pygame.key.get_pressed()[K_LCTRL] and pygame.key.get_pressed()[K_s]:
                    if t_salvar is None:
                        t_salvar = Thread(target=salvar_json, args=[cenarios])
                        t_salvar.start()
                    else:
                        t_salvar.join()
                        t_salvar = Thread(target=salvar_json, args=[cenarios])
                        t_salvar.start()
                elif pygame.key.get_pressed()[K_s]:
                    cenario[1] += 1
                    if tuple(cenario) in cenarios:
                        chao_sprite = cenarios[tuple(cenario)].grupo
                        do_up_cenario = True
                        for x in monstros_sprites.sprites():
                            x.rect.centery -= H
                    else:
                        cenario[1] -= 1

        if exiting:
            # Exibe as opções de saida na tela
            pygame.draw.rect(tela, (125, 125, 125),
                             ((W * 0.7) / 2, (H - 0.1 * H) / 2,
                              W * 0.1 * len(exiting_menu), 0.1 * H))
            for button in exiting_menu:
                button.changeColor(MOUSE_POS)
                button.update(tela)

        if running:
            # Imprime informações na tela
            if side_bar:
                for btn in click_buttons:
                    btn.changeColor(MOUSE_POS)
                    btn.update(tela)

            info(cenario, None, tela, fps, True)
            print_pos(tela, chao_sprite)
            draw_selected_rect(bloco_selecionado, tela)
        pygame.display.flip()

    if t_salvar is not None:
        t_salvar.join()
    menu.join()
    # l_cmd.join(timeout=1000)
    # pygame.quit()  # Remover na release
    return 0


def print_pos(tela, grupo):
    """Imprime as posicoes dos blocos"""
    for i in range(B_H):
        for j in range(B_W):
            txt = fonte0.render(f'{i} {j}', True, preto)
            tela.blit(txt, (i * block_size[0],
                            j * block_size[1]))


def find_block(grupo, loc):
    """Descobre o bloco de tal localização no grupo"""
    for x in grupo.sprites():
        a, b = x.rect.topleft
        if a // block_size[0] == loc[0] and b // block_size[1] == loc[1]:
            return x
    return None


def menu_select():
    """Menu de edição de bloco"""
    global do_up_cenario, do_up_bloco, bloco_selecionado, cenario, do_up_run

    BG = 'black'  # Background
    TC = 'red'  # Cor do texto
    IS = 6, 6  # Input size

    layout = sg.Frame('',
                      [
                          [
                              sg.Text('Menu do bloco', background_color=BG, text_color=TC)
                          ],
                          [
                              sg.Frame('Posição', [
                                  [sg.Text('Selecionada:'),
                                   sg.Input('  ', key='posicao', enable_events=True, size=IS)],
                                  [sg.Text('Id bloco'),
                                   sg.Input('   ', key='bloco', size=IS),
                                   sg.Text(' ' * 15, key='bloco_nome')]
                              ], element_justification='left')
                          ],
                          [
                              sg.Frame('Flags', [
                                  [
                                      sg.Text('Flip'),
                                      sg.Checkbox('', key='flip')
                                  ],
                                  [
                                      sg.Text('Andável'),
                                      sg.Checkbox('', key='andavel')
                                  ],
                                  [
                                      sg.Text('Lentidao %'),
                                      sg.Input(' ' * 3, key='lentidao', size=IS)
                                  ],
                                  [
                                      sg.Text('Dano/segundo'),
                                      sg.Input(' ' * 3, key='dano', size=IS)
                                  ]
                              ], element_justification='left')
                          ],
                          [
                              sg.Text('Menu do cenário', background_color=BG, text_color=TC)
                          ],
                          [
                              sg.Frame('', [
                                  [
                                      sg.Text('Atual'),
                                      sg.Input(' ' * 3, key='cenario', size=IS, enable_events=True)
                                  ],
                                  [
                                      sg.Text('Lock'),
                                      sg.Checkbox('', key='lock')
                                  ],
                                  [
                                      sg.Text('Acesso'),
                                      sg.Checkbox('', key='acesso')
                                  ],
                                  [
                                      sg.Text('Background'),
                                      sg.Input('  ', key='background', size=IS)
                                  ],
                                  [
                                      sg.Text('Copiar'),
                                      sg.Checkbox('', key='copia')
                                  ],
                                  [
                                      sg.Text('Fonte'),
                                      sg.Input('   ', key='copia_fonte', size=IS)
                                  ]
                              ])
                          ],
                          [
                              sg.Button('Salvar', key='salvar', enable_events=True)
                          ]
                      ],
                      element_justification='ce', background_color=BG, border_width=0)
    tela = sg.Window('Menu', layout=[[layout]], background_color=BG, finalize=True)

    def update_bloco():
        if bloco_selecionado is not None:
            pos = bloco_selecionado.rect.topleft[0] // block_size[0], bloco_selecionado.rect.topleft[1] // block_size[1]
            posicao = f'{pos[0]} {pos[1]}'
            tela.Element('flip').update(value=bloco_selecionado.fliped)
            tela.Element('andavel').update(value=bloco_selecionado.walkable)
            tela.Element('dano').update(bloco_selecionado.damage[1])
            tela.Element('lentidao').update(bloco_selecionado.slower[1])
            tela.Element('bloco').update(bloco_selecionado.block_id)
        else:
            posicao = ''
            tela.Element('flip').update(value=False)
            tela.Element('andavel').update(value=False)
            tela.Element('dano').update('0.0')
            tela.Element('lentidao').update('0')
            tela.Element('bloco').update('0')
        tela.Element('posicao').update(posicao)

    def update_cenario():
        tela.Element('cenario').update(f'{cenario[0]} {cenario[1]}')
        tela.Element('lock').update(value=cenarios[tuple(cenario)].lock)
        tela.Element('acesso').update(value=cenarios[tuple(cenario)].acesso)
        tela.Element('background').update(f'{cenarios[tuple(cenario)].background}')
        tela.Element('copia').update(value=cenarios[tuple(cenario)].copia)
        tela.Element('copia_fonte').update(f'{cenarios[tuple(cenario)].fonte}')

    def salvar(values):
        """Dado o estado da tela, tenta salvar em memória local"""
        erros = []
        cen = tuple(int(x) for x in values['cenario'].split())
        if cen in cenarios:
            # Salvando config do cenario
            cenarios[cen].lock = bool(values['lock'])
            cenarios[cen].acesso = bool(values['acesso'])
            cenarios[cen].copia = bool(values['copia'])
            fonte = tuple(map(int, values['copia_fonte'].split()))
            if len(fonte) == 2:
                cenarios[cen].fonte = values['copia_fonte']
            else:
                erros.append('Fonte inválida')
            try:
                pos = tuple(map(int, values['posicao'].split()))
            except:
                pos = 0
                erros.append('Posição inválida ou nula não modificada')
            if len(pos) == 2:
                # Altera os campos da posicao
                obj = find_block(cenarios[tuple(cenario)].grupo, (pos[0], pos[1]))
                if obj is not None:
                    obj.fliped = values['flip']
                    obj.walkable = values['andavel']
                    if values['bloco'].isnumeric():
                        old_id = obj.block_id
                        obj.block_id = int(values['bloco'])
                        try:
                            obj.reload()
                        except ValueError:
                            obj.block_id = old_id
                            erros.append('ID de bloco inválido')
                    else:
                        erros.append('Tipo de bloco inválido')
                    if values['dano'].replace(".", "").isnumeric():
                        dano = float(values['dano'])
                        if dano > 0:
                            obj.damage = True, dano
                    else:
                        erros.append('Dano deve ser numérico')

                    if values['lentidao'].isnumeric():
                        lentidao = int(values['lentidao'])
                        if lentidao > 0:
                            obj.slower = True, lentidao
                    else:
                        erros.append('Lentidão deve ser numéro inteiro')
                else:
                    erros.append('Objeto da posição não encontrado')
            else:
                erros.append('Posição inválida')
        else:
            erros.append('cenario inexistente')
        return erros

    update_bloco()
    update_cenario()

    while running:
        event, values = tela.read(timeout=100, timeout_key='timeout')
        if event != 'timeout':
            if event == 'WIN_CLOSED':
                tela.close()
                break
            if event == 'posicao':
                try:
                    tupla = tuple(map(int, values['posicao'].split()))
                    if len(tupla) == 2:
                        if tupla in cenarios:
                            bloco_selecionado = find_block(cenarios[tuple(cenario)].grupo,
                                                           (tupla[0], tupla[1]))
                            do_up_bloco = True
                except ValueError:
                    pass
            elif event == 'cenario':
                try:
                    tupla = tuple(map(int, values['cenario'].split()))
                    if len(tupla) == 2:
                        if tupla in cenarios:
                            cenario = [tupla[0], tupla[1]]
                            do_up_cenario = True
                            do_up_bloco = True
                            do_up_run = True
                            bloco_selecionado = None
                except ValueError:
                    pass
            elif event == 'salvar':
                salvou = salvar(values)
                for erro in salvou:
                    print(erro)

        if do_up_cenario:
            update_cenario()
            do_up_cenario = False

        if do_up_bloco:
            update_bloco()
            do_up_bloco = False

    tela.close()


def salvar_json(dic):
    """Salva o estado da aplicação num json destino"""
    print('[Sistema] Salvando...')
    data = {}
    for key, item in dic.items():
        new_key = f'{key[0]} {key[1]}'
        blocos = defaultdict(dict)
        decoracoes = defaultdict(dict)
        for bloco in [x for x in item.grupo.sprites() if type(x).__name__ == 'Bloco']:
            x, y = bloco.rect.topleft[0] // block_size[0], bloco.rect.topleft[1] // block_size[1]
            blocos[x][y] = {
                'id': bloco.block_id,
                'flip': bloco.fliped,
                'walkable': bloco.walkable,
            }
            if bloco.damage[0]:
                blocos[x][y]['damage'] = bloco.damage[1]
            if bloco.slower[0]:
                blocos[x][y]['slower'] = bloco.slower[1]
        decor_index = 0
        for decor in [x for x in item.grupo.sprites() if x.tipo == 'decorativo']:
            decor_index += 1
            decoracoes[decor_index] = {
                'classe': type(decor).__name__,
                'index': decor.index,
                'pos': f'{decor.rect.topleft[0] // block_size[0]} {decor.rect.topleft[1] // block_size[1]}',
                'blocos': decor.blocos,
                'bloqueia': decor.bloqueia
            }

        data[new_key] = {
            'acesso': item.acesso,
            'lock': item.lock,
            'background': item.background,
            'final': [x for x in item.finais],
            'copia': {
                'valor': item.copia,
                'fonte': item.fonte
            },
            'blocos': blocos,
            'decoracoes': decoracoes
        }
    with open(arq_destino, 'w') as arq:
        arq.write((jsbeautifier.beautify(json.dumps(data), options)))
    print('[Sistema] Estado do cenário salvo')


def salvar_monstros():
    """Salva os monstros no json"""
    inimigos = {}
    cont = 1
    for sprite in monstros_sprites.sprites():
        pos = sprite.rect.topleft[0], sprite.rect.topleft[1]
        inimigos[str(cont)] = {
            "pos": [pos[0], pos[1]],
            "tipo": type(sprite).__name__,
            "quantidade": 1,
        }
        if type(sprite).__name__.startswith('Boss'):
            inimigos[str(cont)]['boss'] = True
        cont += 1
    data = {
        "inimigos": inimigos
    }

    with open('dados/monstros_dev.json', 'w') as arq:
        arq.write((jsbeautifier.beautify(json.dumps(data), options)))


def entity_imgs():
    """Retorna as imagens dos monstros iteravel"""
    from codigos.entidades.gerenciador_imagens import imagens
    monstros = ['Executor', 'Olho', 'Goblin', 'Esqueleto', 'Golem', 'Lobo', 'BringerDeath', 'Cogumelo']
    # bosses = [f'Boss{i}' for i in range(1, 4)]
    imgs = imagens['monstros']
    for monstro in monstros:
        yield imgs[monstro.lower()]['idle'][0], monstro


comando = []


def get_user_input():
    global comando
    comando = input("").split()


def linha_comando_add():
    """Linha de comando para adição de inimigos no json de inimigos"""
    import codigos.entidades.monstros as monstros
    import codigos.entidades.bosses as bosses
    global comando, monstros_sprites, running
    # global lista_monstros
    print('[Dica] Digite criar {classe} {qtd} para criar uma entidade num bloco selecionado')
    print('> ', end='')
    while running:
        t_cmd = Thread(target=get_user_input)
        t_cmd.start()
        t_cmd.join(timeout=1)
        if len(comando) >= 2:
            if comando[0] == 'criar':
                classe = getattr(monstros, comando[1], None)
                if classe is None:
                    classe = getattr(bosses, comando[1], None)
                if classe is not None:
                    obj = classe()
                    if bloco_selecionado is not None:
                        obj.rect.centerx = bloco_selecionado.rect.centerx
                        obj.rect.centery = bloco_selecionado.rect.centery
                        monstros_sprites.add(obj)
                    else:
                        print('[Falha] Precisa ter um bloco selecionado')
                else:
                    print('[Falha] Classe não encontrada')
                print('> ', end='')
                comando = []


run()
