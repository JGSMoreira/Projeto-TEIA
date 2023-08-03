import os

caminho = './legendas'

arquivos_de_legenda = os.listdir(caminho)

palavras_chave = ['sala', 'quarto', 'cozinha', 'banheiro', 'cômodo']

def dict_legenda(numLinha, inicio, fim, texto): 
    return {
        'numero': numLinha.replace('\n', ''),
        'inicio': inicio.replace('\n', ''),
        'fim': fim.replace('\n', ''),
        'texto': texto.replace('\n', ' ').strip(),
    }

for arquivo in arquivos_de_legenda:
    srt_file = open(caminho + '/' + arquivo, 'r', encoding="utf8").readlines()
    print('Buscando palavras-chave no arquivo ' + arquivo)

    lista_dicts = []

    numero_linha = 0
    inicio = ''
    fim = ''
    texto = ''
    primeira = True

    for linha in srt_file:
        if primeira:
            numero_linha = linha
            primeira = False
        elif str(linha).find('-->') != -1:
            inicio = str(linha).split(' --> ')[0]
            fim = str(linha).split(' --> ')[1]
        elif str(linha).find('\n') != -1:
            texto += str(linha).replace('\n', ' ')

        if linha == '\n':
            lista_dicts.append(dict_legenda(numero_linha, inicio, fim, texto))
            numero_linha = 0
            inicio = ''
            fim = ''
            texto = ''
            primeira = True

    quant_resultados = 0
    resultados = []
    for legenda in lista_dicts:
        for palavra in palavras_chave:
            if legenda['texto'].find(palavra) != -1:
                quant_resultados += 1
                resultados.append(legenda)

    if len(resultados) > 0:
        print('Salvando cenas...')
        open(f'momentos/{arquivo}.txt', 'w', encoding="utf8").write(str(resultados))

    print('Quantidade de resultados: ' + str(quant_resultados))

