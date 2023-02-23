# Esse arquivo contem as telas referentes aos menus de jogo
import PySimpleGUI as sg
from codigos.variaveis import acrescimos, devs, versao, update


def run():
    """Roda o menu de abertura do jogo"""
    info = sg.Frame('', [[sg.Text('Developed by:')],
                         [sg.Text(x) for x in devs],
                         [sg.Text(f'Last update: {update}')],
                         [sg.Text(f'Version: {versao}')],
                         [sg.Button('Back', key='back')]], key='infomenu',
                    visible=False, element_justification='center')
    mainl = [[sg.Text('Just a Rpg', key='title',
                      font=('Courier New', 22, 'bold'), background_color='black')],
             [sg.Button('Play', key='play', button_color='black',
                        size=(11, 1), font='Consolas 12')],
             [sg.Button('Info', key='info', button_color='black', size=(11, 1),
                        font='Consolas 12')]
             ]
    main = sg.Frame('', mainl, key='mainmenu', element_justification='center',
                    background_color='black', border_width=0)
    layout = [[main, info]]
    tela = sg.Window('Just a Rpg', layout, size=(250, 250),
                     background_color='black', element_justification='ce')

    while True:
        evento, valores = tela.read()
        if evento is None:
            return False
        if evento == 'play':
            try:
                tela.close()
                import game
                return True
            except Exception as e:
                sg.popup('Ocorreu o seguinte erro ao tentar abrir o jogo\n', e)
                return True
        if evento == 'info':
            tela.Element('infomenu').update(visible=True)
            tela.Element('mainmenu').update(visible=False)
        elif evento == 'back':
            tela.Element('infomenu').update(visible=False)
            tela.Element('mainmenu').update(visible=True)


def level_up(char):
    """Roda o menu de skills do player"""
    layout = [[sg.Text('Avaliable points:', key='title', font=('Courier New', 12, 'bold')),
               sg.Text('000', key='points', font=('Courier New', 12, 'bold'))],
              [sg.Text('Health'), sg.Text('000/000', key='val_health'),
               sg.Button('+', key='plus_health')],
              [sg.Text('Damage'), sg.Text('000', key='val_damage'),
               sg.Button('+', key='plus_damage')],
              [sg.Text('Speed'), sg.Text('00', key='val_speed'),
               sg.Button('+', key='plus_speed')],
              [sg.Text('Luck'), sg.Text('0.0%', key='val_luck'),
               sg.Button('+', key='plus_luck')]
              ]
    tela = sg.Window('Level-up', layout, size=(250, 250),
                     background_color='', element_justification='left')
    tela.read(timeout=1)
    while True:
        tela.Element('points').update(f'{char.pontos}')
        tela.Element('val_health').update(f'{char.vida}/{char.vida_max}')
        tela.Element('val_damage').update(f'{char.dano}')
        tela.Element('val_speed').update(f'{char.vel}')
        tela.Element('val_luck').update(f'{char.sorte}%')
        evento, valores = tela.read()
        if evento is None:
            return None
        elif 'plus' in evento:
            if char.pontos > 0:
                tipo = evento.replace('plus_', '')
                if tipo == 'health':
                    if char.vida == char.vida_max:
                        char.vida += acrescimos['vida']
                    char.vida_max += acrescimos['vida']
                elif tipo == 'damage':
                    char.dano += acrescimos['dano']
                elif tipo == 'speed':
                    char.vel += acrescimos['velocidade']
                elif tipo == 'luck':
                    char.sorte += acrescimos['sorte']
                char.pontos -= 1


def mercado(char, merc):
    import codigos.itens.itens as itens_mod
    itens = [
        [sg.Text(x.nome), sg.Text(x.valor),
         sg.Image(x.img_sg, enable_events=True, key=f'comprar {x.classe} {x.valor}')]
        for x in merc.mercadorias
    ]
    lbl = [sg.Frame('', [[sg.Text('Nome'), sg.Text('Preço'), sg.Text('Comprar')]])]
    itens.insert(0, lbl)
    itensframe = sg.Frame('', itens)
    layout = [
        [sg.Text(f'Seu dinheiro:'), sg.Text(f'{char.coins}',
                                            text_color='yellow', key='dinheiro')],
        [sg.Text(f'Mercadorias de {merc.nome}:')],
        [itensframe],
        [sg.Text('Mensagem de feedback', key='feedback', visible=False)]
    ]
    tela = sg.Window('', layout, element_justification='ce')
    while True:
        e, v = tela.read()
        if e is None:
            tela.close()
            break
        elif 'comprar' in e:
            e = e.split()
            c, va = e[1], int(e[2])
            if char.coins >= va:
                classe = getattr(itens_mod, c)
                char.add_item(classe())
                char.coins -= va
                tela.Element('dinheiro').update(str(char.coins))
                tela.Element('feedback').update('Compra efetuada com sucesso')
                tela.Element('feedback').update(text_color='green')
                tela.Element('feedback').update(visible=True)
            else:
                tela.Element('feedback').update('Dinheiro insuficiente')
                tela.Element('feedback').update(text_color='red')
                tela.Element('feedback').update(visible=True)

    return None
