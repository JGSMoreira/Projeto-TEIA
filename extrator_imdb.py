from bs4 import BeautifulSoup as bs
import requests
import time
import dotenv
import os

dotenv.load_dotenv()

base_url = 'https://www.imdb.com/find/'
headers= {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0'
}

file_filmes = open('filmes.txt', 'r').readlines()
id_filmes = []

def limparId(href):
    return href.split('/')[2]
i = 1
for filme in file_filmes:
    results = requests.get(
        url = base_url, 
        headers = headers,
        params = {'q': filme}
    )

    soup = bs(results.content, 'html.parser')
    lista_filmes = soup.find('ul', class_='ipc-metadata-list')

    if lista_filmes is None:
        print('Nenhum filme encontrado')
        exit()

    filme = lista_filmes.find('li')
    titulo = filme.find('a')
    ano = filme.find('span')
    if (titulo is not None) and (ano is not None):
        id_filmes.append(limparId(titulo['href']))
        print(f'{i:03d}/{len(file_filmes)} | {titulo.text} - {ano.text} - {limparId(titulo["href"])}')
    
    time.sleep(.5)
    i += 1

file_ids = open('ids.txt', 'w').write('\n'.join(id_filmes))