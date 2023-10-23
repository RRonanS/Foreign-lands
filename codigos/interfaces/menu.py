# Esse arquivo contem as telas referentes aos menus de jogo
import PySimpleGUI as sg
from codigos.variaveis import acrescimos


def level_up(char, tl):
    """Roda o menu de skills do player"""
    layout = [[sg.Text(tl('pontos disponíveis') + ':', key='title', font=('Courier New', 12, 'bold')),
               sg.Text('000', key='points', font=('Courier New', 12, 'bold'))],
              [sg.Text(tl('vida')), sg.Text('000/000', key='val_health'),
               sg.Button('+', key='plus_health')],
              [sg.Text(tl('dano')), sg.Text('000', key='val_damage'),
               sg.Button('+', key='plus_damage')],
              [sg.Text(tl('velocidade')), sg.Text('00', key='val_speed'),
               sg.Button('+', key='plus_speed')],
              [sg.Text(tl('sorte')), sg.Text('0.0%', key='val_luck'),
               sg.Button('+', key='plus_luck')]
              ]
    tela = sg.Window(tl('personagem'), layout, size=(250, 250),
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


def mercado(char, merc, tl):
    import codigos.itens.itens as itens_mod
    itens = [
        [sg.Text(tl(x.nome)), sg.Text(x.valor),
         sg.Image(x.img_sg, enable_events=True, key=f'comprar {x.classe} {x.valor}')]
        for x in merc.mercadorias
    ]
    lbl = [sg.Frame('', [[sg.Text(tl('nome')), sg.Text(tl('preço')), sg.Text(tl('comprar'))]])]
    itens.insert(0, lbl)
    itensframe = sg.Frame('', itens)
    layout = [
        [sg.Text(tl('seu dinheiro') + ':'), sg.Text(f'{char.coins}',
                                                    text_color='yellow', key='dinheiro')],
        [sg.Text(tl('mercadorias de') + f' {merc.nome}:')],
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
                tela.Element('feedback').update(tl('compra efetuada com sucesso'))
                tela.Element('feedback').update(text_color='green')
                tela.Element('feedback').update(visible=True)
            else:
                tela.Element('feedback').update(tl('dinheiro insuficiente'))
                tela.Element('feedback').update(text_color='red')
                tela.Element('feedback').update(visible=True)
    return None
