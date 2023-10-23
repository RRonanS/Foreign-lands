import json


class Tradutor:
    """Classe responsável pela tradução das palavras do jogo"""
    def __init__(self):
        from codigos.variaveis import idioma
        self.conversao = {}
        if idioma != 'portugues':
            self.load(idioma)

    def load(self, idioma):
        """Carrega o idioma na memória"""
        if idioma == 'portugues':
            self.conversao = {}
            return 0
        try:
            with open('arquivos/idiomas/'+idioma+'.json', 'r', encoding='utf-8') as i:
                arq = json.load(i)
                self.conversao = arq['palavras']
        except Exception as e:
            print('[Erro] Problema ao carregar o idioma', idioma)

    def traduzir(self, linha):
        """Traduz uma frase e a retorna"""
        if len(self.conversao) == 0:
            return linha

        if linha in self.conversao:
            return self.conversao[linha]

        palavras = linha.split()
        for i in range(len(palavras)):
            has_virgula = ',' in palavras[i]
            has_ponto = '.' in palavras[i]
            palavra_sem_pontuacao = palavras[i].rstrip(',.')
            if palavra_sem_pontuacao in self.conversao:
                palavras[i] = self.conversao[palavra_sem_pontuacao]
            if has_ponto:
                palavras[i] = palavras[i]+'.'
            elif has_virgula:
                palavras[i] = palavras[i]+','

        linha_traduzida = " ".join(palavras)
        return linha_traduzida

    def reload(self):
        """Recarrega com base no idioma atual"""
        from codigos.variaveis import idioma
        self.load(idioma)
