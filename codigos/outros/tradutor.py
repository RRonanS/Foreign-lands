import json

from codigos.variaveis import idioma


class Tradutor:
    """Classe responsável pela tradução das palavras do jogo"""
    def __init__(self):
        self.conversao = {}
        if idioma != 'portugues':
            self.load(idioma)

    def load(self, idioma):
        """Carrega o idioma na memória"""
        try:
            with open('arquivos/idiomas/'+idioma+'.json', 'r') as i:
                arq = json.load(i)
                self.conversao = arq['palavras']
                print(self.conversao)
        except Exception as e:
            print('[Erro] Problema ao carregar o idioma', idioma)

    def traduzir(self, linha):
        """Traduz uma frase e a retorna"""
        if len(self.conversao) == 0:
            return linha
        for palavra in linha.split():
            if palavra in self.conversao:
                linha = linha.replace(palavra, self.conversao[palavra])
        return linha
