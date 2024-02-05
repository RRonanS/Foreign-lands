# Automatiza a leitura dos blocos presentes na pasta alvo
import os

# Itera sobre os arquivos na pasta
def get_lista(dir):
    """Retorna um dicionario com o nome das imagens encontradas e seus ids buscados na pasta dir"""

    # Lista todos os arquivos na pasta
    files = os.listdir(dir)
    # Dicionário para armazenar o mapeamento id -> nome do arquivo
    id_png = {}

    for file in files:
        # Divide o nome do arquivo e a extensão
        name, ext = os.path.splitext(file)

        # Verifica se a extensão é .png
        if ext == '.png' or ext == '.jpg':
            # Divide o nome para obter o id e o nome do bloco
            parts = name.split('_')
            try:
                id = int(parts[-1])
                block_name = '_'.join(parts[:-1])

                # Adiciona ao dicionário
                id_png[id] = block_name
            except ValueError:
                print(f'[Erro], a imagem {name} não está no formato nome_id')

    return id_png
