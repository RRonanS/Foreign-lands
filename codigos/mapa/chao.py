# Este arquivo possui os construtores de objetos para o chão do jogo
from collections import defaultdict
import pygame.sprite
from json import load
from codigos.variaveis import screen_size, block_size, char_size, fps
import codigos.mapa.decorativo as decorativo

width, height = screen_size

dir = 'arquivos/imagens/blocos/'
dir_img = 'arquivos/imagens'

# Conversão de id de bloco para nome da png
try:
    with open(dir_img+'/tabela.json', 'r', encoding='UTF-8') as arq:
        id_png = load(arq)['id_png']
        id_png = {int(key): value for key, value in id_png.items()}
except Exception as E:
    # Carrega o padrão
    print(f'[Erro] ao carregar o arquivo {dir_img}/tabela.png:', E)
    id_png = {
        1: 'terra1', 2: 'terra2', 3: 'terra3', 4: 'terra4', 5: 'terra5',
        6: 'volcano1', 7: 'terra', 8: 'grama', 9: 'grama-passagem',
        10: 'grama-intersec', 11: 'cogumelo1', 12: 'cogumelo2', 13: 'cogumelo3',
        14: 'brick/brick1', 15: 'brick/brick2', 16: 'brick/brick3', 17: 'brick/brick4',
        18: 'brick/brick5', 19: 'brick/brick6', 20: 'brick2/stone1', 21: 'brick2/stone2',
        22: 'lavaf1', 23: 'lavaf2', 24: 'lavaf3', 25: 'lavaf4'
    }
imgs = {
    key: pygame.transform.scale(pygame.image.load(dir+f'{id_png[key]}.png'), block_size)
    for key in id_png
}

class Bloco(pygame.sprite.Sprite):
    """Classe para representar um bloco na tela"""
    def __init__(self, pos, id):
        """Cria um bloco dada sua posição topleft e o id do bloco"""
        pygame.sprite.Sprite.__init__(self)
        self.tipo = 'bloco'
        self.block_id = id
        try:
            img = imgs[id]
        except:
            raise ValueError('ID de bloco inválido <'+str(id)+'>')
        self.image = img
        self.fliped = False
        # Define se entidades podem andar sobre esse bloco
        self.walkable = True
        # Se True, diminui a velocidade das entidades no bloco para x%
        self.slower = (False, 0)
        self.damage = (False, 0)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.mask = pygame.mask.from_surface(self.image)

    def flip(self):
        """Rotaciona o bloco em 90 graus"""
        img = pygame.image.load(dir+f'{id_png[self.block_id]}.png')
        img = pygame.transform.scale(img, block_size)
        img = pygame.transform.rotate(img, 90)
        self.image = img
        self.fliped = True

    def set_walkable(self, value):
        """Muda a flag se o bloco é andavel"""
        self.walkable = value

    def set_slower(self, value, amount):
        """Muda a flag de desaceleracao do bloco"""
        self.slower = (value, amount)

    def set_damager(self, value, amount):
        """Muda a flag do bloco causar dano"""
        self.damage = value, amount

    def reload(self):
        """Recarrega a imagem do bloco"""
        try:
            self.image = imgs[self.block_id]
        except:
            raise ValueError('ID de bloco inválido <'+str(id)+'>')


def arredondar(cords):
    """Arredonda as coordenadas passadas para representarem o topleft de
    algum bloco"""
    x, y = cords
    b_x = -(x % block_size[0])
    if abs((x % block_size[0])-block_size[0]) < abs(b_x):
        b_x = abs((x % block_size[0])-block_size[0])
    x += b_x
    b_y = -(y % block_size[1])
    if abs((y % block_size[1])-block_size[1]) < abs(b_y):
        b_y = abs((y % block_size[1])-block_size[1])
    y += b_y
    return x, y


class Chao:
    def __init__(self, fonte):
        """Classe para gerar e armazenar o chao do jogo,
        Obs, o senso é invertido, ficando y, x. Com exceção do self.bloqueios"""
        self.grupo = pygame.sprite.Group()
        self.bloqueios = {}
        self.lock = False
        self.acesso = True
        self.background = 0
        self.posicoes = {}
        self.copia = False
        self.fonte = '0 0'
        self.efeitos = defaultdict(list)
        finais = fonte['final']
        self.finais = finais
        excludex = []
        excludey = []
        # Detecção de Blocos de fronteira com o vazio
        if '+x' in finais:
            excludex.append((width//block_size[0])-1)
        if '-x' in finais:
            excludex.append(0)
        if '+y' in finais:
            excludey.append(0)
        if '-y' in finais:
            excludey.append((height//block_size[1])-1)
        source = fonte['blocos']
        # Leitura dos dados e armazenamento
        for linha in source:
            x = int(linha)
            if x not in excludex:
                for coluna in source[linha]:
                    y = int(coluna)
                    if y not in excludey:
                        b_id = source[linha][coluna]['id']
                        if 'mudar_id' in fonte['copia']:
                            # Muda id do bloco destino
                            if fonte['copia']['mudar_id']:
                                b_id = fonte['copia']['novo_id']

                        bloco = Bloco((x*block_size[0], y*block_size[1]), b_id)
                        if source[linha][coluna]['flip']:
                            bloco.flip()
                        if 'walkable' in source[linha][coluna]:
                            bloco.walkable = source[linha][coluna]['walkable']
                        if 'damage' in source[linha][coluna]:
                            val = int(source[linha][coluna]['damage'])
                            if val > 0:
                                bloco.damage = True, val
                        if 'slower' in source[linha][coluna]:
                            val = int(source[linha][coluna]['slower'])
                            if val > 0:
                                bloco.slower = True, val
                        if bloco.walkable:
                            self.posicoes[(y, x)] = True
                            if bloco.slower[0]:
                                self.efeitos[(y, x)].append(('S', bloco.slower[1] / fps))
                            if bloco.damage[0]:
                                self.efeitos[(y, x)].append(('D', bloco.damage[1] / fps))
                        self.grupo.add(bloco)
        if 'decoracoes' in fonte:
            decor = fonte['decoracoes']
            for dec in decor:
                class_ = getattr(decorativo, decor[dec]['classe'])
                inst = class_(decor[dec]['index'], decor[dec]['blocos'])
                a = decor[dec]['pos'].split()
                x, y = int(a[0]), int(a[1])
                inst.rect.topleft = x*block_size[0], y*block_size[1]
                if 'bloqueia' in decor[dec]:
                    if decor[dec]['bloqueia']:
                        inst.bloqueia = True
                        self.bloqueios[(x*block_size[0], y*block_size[1])] = decor[dec]['blocos']
                self.grupo.add(inst)

    def tem_bloco(self, cords):
        """Dadas as coordenadas, converte para posição de bloco e retorna
        True se houver um bloco nesta posição, False senão"""
        x, y = arredondar(cords)
        if ((y//block_size[1]), (x//block_size[0])) in self.posicoes:
            return True
        return False

    def tem_efeito(self, cords):
        """Verifica se nessas coordenadas há algum efeito a ser aplicado na entidade nela presente,
        retorna uma lista dos efeitos presentes ou None"""
        x, y = arredondar(cords)
        if self.tem_bloco(cords):
            if ((y // block_size[1]), (x // block_size[0])) in self.efeitos:
                return self.efeitos[((y // block_size[1]), (x // block_size[0]))]
        return None

    def aplicar_efeitos(self, entidade):
        """Aplica efeitos a uma entidade, caso haja efeito no bloco em questão"""
        pos = entidade.rect.centerx, entidade.rect.centery
        efeitos = self.tem_efeito(pos)
        if efeitos is not None:
            for efeito in efeitos:
                if efeito[0] == 'D':
                    entidade.vida -= efeito[1]
                if efeito[0] == 'S':
                    # Diminuir velocidade, depois retornar a original
                    pass

    def tem_bloqueio(self, rect):
        """Verifica se alguma decoração bloqueia tal retangulo,
        retorna True se houver, False senão"""
        x, y = arredondar(rect.center)
        tolerancia = char_size[0]//2
        for key in self.bloqueios:
            if key[0]+tolerancia <= x < key[0] + (self.bloqueios[key]*block_size[0]) - tolerancia:
                if key[1]+tolerancia < y < key[1] + (self.bloqueios[key]*block_size[1]) - tolerancia:
                    return True
        return False
