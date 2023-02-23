import json
from codigos.variaveis import load
import codigos.entidades.monstros as monstros
import codigos.entidades.bosses as bmod
import codigos.entidades.npcs as npcmod

dir = 'dados/'


def escrever(personagem, inimigos, npcs, cenario):
    """Recebe os objetos do jogo e armazena em formato json"""
    data = {
        "personagem": {
            "nivel": personagem.nivel,
            "skills": [personagem.vida_max, personagem.dano, personagem.vel, personagem.sorte],
            "vida": personagem.vida,
            "pontos": personagem.pontos,
            "coins": personagem.coins,
            "exp": personagem.exp,
            "pos": [personagem.rect.bottomleft[0], personagem.rect.bottomleft[1]],
            "cenario": [cenario[0], cenario[1]],
            "acesso": [x for x in personagem.acesso],
            "desbloqueio": [[x[0], x[1]] for x in personagem.desbloqueio]
        },
        "inimigos": {},
        "npcs": {}
    }
    cont = 0
    for x in inimigos.sprites():
        cont += 1
        data['inimigos'][str(cont)] = {
            "pos": [x.rect.centerx, x.rect.centery],
            "vida": x.vida,
            "tipo": type(x).__name__
        }
    cont = 0
    for x in npcs.sprites():
        cont += 1
        data['npcs'][str(cont)] = {
            "pos": [x.rect.bottomleft[0], x.rect.bottomleft[1]],
            "tipo": type(x).__name__
        }

    with open(f'{dir}player_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)


def ler(personagem, inimigos, npcs, bosses):
    """Lê os dados armazenados e carrega nos objetos, retorna False se nao leu"""
    try:
        with open(f'{dir}player_data.json', 'r') as json_file:
            d = json.load(json_file)
    except:
        with open(f'{dir}player_data.json', 'w'):
            pass
        return False, (0, 0)
    if len(d) > 0 and load:
        p = d['personagem']
        personagem.nivel, personagem.vida_max = p['nivel'], p['skills'][0]
        personagem.dano, personagem.vel = p['skills'][1], p['skills'][2]
        personagem.sorte, personagem.vida = p['skills'][3], p['vida']
        personagem.pontos, personagem.coins = p['pontos'], p['coins']
        personagem.exp = p['exp']
        personagem.acesso = [(i[0], i[1]) for i in p['acesso']]
        personagem.desbloqueio = [(i[0], i[1]) for i in p['desbloqueio']]
        personagem.rect.bottomleft = p['pos'][0], p['pos'][1]
        cenario = p['cenario'][0], p['cenario'][1]
        personagem.upar()

        i = d['inimigos']
        for key in i:
            if 'Boss' in i[key]['tipo']:
                class_ = getattr(bmod, i[key]['tipo'])
            else:
                class_ = getattr(monstros, i[key]['tipo'])
            item = class_()
            item.rect.centerx, item.rect.centery = i[key]['pos'][0], i[key]['pos'][1]
            item.vida = i[key]['vida']
            inimigos.add(item)
            if 'Boss' in i[key]['tipo']:
                bosses.add(item)

        n = d['npcs']
        for key in n:
            class_ = getattr(npcmod, n[key]['tipo'])
            item = class_((n[key]['pos'][0], n[key]['pos'][1]))
            npcs.add(item)

        return True, cenario
    else:
        return False, (0, 0)
