import sys
from codigos.variaveis import screen_size, idioma
from random import randint
from threading import Thread

itens = sys.modules['codigos.itens.itens']
monstros = sys.modules['codigos.entidades.monstros']
entidades = sys.modules['codigos.entidades']


comando = []


def get_user_input():
    global comando
    comando = input("").split()


class CommandLine:
    """Classe para linha de comando do jogo"""

    def __init__(self, cenarios, sprites, sprites_buffer, tl):
        self.cenarios = cenarios
        self.sprites = sprites
        self.updates = sprites_buffer
        self.running = True
        self.tl = tl

    def run(self):
        """Executa a linha de comando, recebendo os comandos"""
        print(self.tl('Digite ajuda para ver todos os comandos'))
        print('> ', end='')
        while self.running:
            t_input = Thread(target=get_user_input)
            t_input.start()
            t_input.join(timeout=1)
            if len(comando) > 0:
                ordem = comando[0]
                params = comando[1::]
                comando.clear()
                try:
                    func = getattr(self, ordem)
                    func(params)
                except Exception as e:
                    print('['+self.tl('Erro')+']', e)
                print('> ', end='')

    def ajuda(self, params):
        """Imprime o guia de comandos disponível na pasta Guias"""
        try:
            with open(f'Guias/{idioma}_Linha de comando.txt', 'r') as arq:
                l = arq.readlines()
                for x in l:
                    print(x.replace('\n', ''))
        except:
            print(self.tl('Não foi possível encontrar o guia para o idioma')+': '+idioma)

    def print_e(self, params):
        """Imprime todas entidades ou aquelas relacionadas a uma classe"""
        cont = 0
        for x in self.sprites.sprites():
            if len(params) > 0:
                if type(x).__name__.lower() == params[0].lower():
                    print(str(cont) + ': ', x)
                    cont += 1
            else:
                print(str(cont) + ': ', x)
                cont += 1

    def info_e(self, params):
        """Imprime toda informacao relacionada a tal entidade, parametro 0 = Numero da entdiade,
        parametro 1 = Classe (opcional)"""

        def atts(entidade):
            lis = dir(entidade)
            for att in lis:
                if not att.startswith('_'):
                    print(att, getattr(entidade, att))

        params[0] = int(params[0])
        cont = 0
        for x in self.sprites.sprites():
            if cont == params[0]:
                if len(params) > 1:
                    if type(x).__name__.lower() == params[1].lower():
                        atts(x)
                        return 1
                else:
                    atts(x)
                    return 1
            else:
                if len(params) > 1:
                    if type(x).__name__.lower() == params[1].lower():
                        cont += 1
                else:
                    cont += 1
        raise ValueError(self.tl("Nenhuma entidade encontrada com tal filtro"))

    def matar(self, params):
        """Mata a entidade dado seu numero e classe, -1 como numero para matar todas da classe"""
        cont = 0
        for x in self.sprites.sprites():
            if int(params[0]) == -1:
                if type(x).__name__.lower() == params[1].lower():
                    setattr(x, 'dead', True)
                    self.updates.add(x)
                    print(self.tl('Entidade'), x, self.tl('foi morta'))
            else:
                if type(x).__name__.lower() == params[1].lower():
                    if cont == int(params[0]):
                        setattr(x, 'dead', True)
                        self.updates.add(x)
                        print(self.tl('Entidade'), x, self.tl('foi morta'))
                        break
                    else:
                        cont += 1

    def xp(self, params):
        """Adiciona xp ao personagem"""
        if len(params) == 0:
            raise ValueError(self.tl('Informe a quantidade de xp a ser adicionada'))
        if not params[0].isnumeric():
            raise ValueError(self.tl('O parametro passado deve ser um numero'))
        val = int(params[0])
        personagem = self.sprites.sprites()[0]
        setattr(personagem, 'exp', getattr(personagem, 'exp') + val)
        personagem.upar()
        print(self.tl('Adicionado'), val, self.tl('de experiencia ao personagem'))

    def coins(self, params):
        """Adiciona dinheiro ao personagem"""
        if len(params) == 0:
            raise ValueError(self.tl('Informe a quantidade de dinheiro a ser adicionada'))
        if not params[0].isnumeric():
            raise ValueError(self.tl('O parametro passado deve ser um numero'))
        val = int(params[0])
        personagem = self.sprites.sprites()[0]
        setattr(personagem, 'coins', getattr(personagem, 'coins') + val)
        print(self.tl('Adicionado'), val, self.tl('moedas ao personagem'))

    def set_atr(self, params):
        """Seta algum atributo da entidade dado seu numero (Obs: problema com floats)"""
        if len(params) < 3:
            raise ValueError(self.tl('Numero de parametros errado'))
        entidade = int(params[0])
        atr = params[1]
        val = params[2]
        try:
            x = self.sprites.sprites()[entidade]
        except:
            raise ValueError(self.tl('Entidade inexistente'))
        if val.isnumeric():
            val = int(val)
        elif val.lower() == 'true':
            val = True
        elif val.lower() == 'false':
            val = False
        has = getattr(x, atr, None)
        if has is None:
            raise ValueError(self.tl('Atributo inexistente'))
        setattr(x, atr, val)
        print(atr, self.tl('de'), x, self.tl('setado para'), val)

    def set_atrc(self, params):
        """Seta algum atributo do personagem"""
        if len(params) < 2:
            raise ValueError(self.tl('Numero de parametros errado'))
        params.insert(0, 0)
        self.set_atr(params)

    def add_item(self, params):
        """Adiciona um item ao inventario do personagem"""
        if len(params) < 2:
            raise ValueError(self.tl('Numero de parametros errado'))
        item = params[0]
        if not params[1].isnumeric():
            raise ValueError(self.tl('O segundo argumento deve ser um numero'))
        qtd = int(params[1])
        personagem = self.sprites.sprites()[0]
        i = getattr(itens, item, None)
        if i is None:
            raise ValueError(self.tl('Item inexistente'))
        i = i()
        i.quantidade = qtd
        personagem.add_item(i)
        print(self.tl('Item adicionado ao inventario'))

    def spawn_cords(self, params):
        """Spawna uma entidade em determinada coordenada"""
        classe = getattr(entidades.monstros, params[0], None)
        if classe is None:
            classe = getattr(entidades.bosses, params[0], None)
        if classe is None:
            classe = getattr(entidades.npcs, params[0], None)
        if classe is None:
            classe = getattr(entidades.personagem, params[0], None)
        if classe is None:
            raise ValueError(self.tl('Entidade inexistente'))
        if not params[1].isnumeric() or not params[2].isnumeric():
            raise ValueError(self.tl('Coordenadas deve ser inteiro'))
        cords = int(params[1]), int(params[2])
        obj = classe()
        obj.rect.centerx, obj.rect.centery = cords[0], cords[1]
        self.updates.add(obj)
        print(self.tl('Entidade'), obj, self.tl('gerada em'), cords[0], cords[1])

    def spawn(self, params):
        """Spawna uma entidade em posicao proxima"""
        classe = params[0]
        self.spawn_cords([classe, str(randint(0, screen_size[0])), str(randint(0, screen_size[1]))])

    def reviver(self, params):
        """Revive o personagem"""
        perso = self.sprites.sprites()[0]
        perso.reviver()
        print(self.tl('Personagem ressucitado'))

    def end(self):
        """Finaliza a linha de comando"""
        self.running = False
