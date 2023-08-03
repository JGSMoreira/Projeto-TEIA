from bs4 import BeautifulSoup as bs
import dotenv
import requests
import os

dotenv.load_dotenv()

base_url = f'https://letterboxd.com/{os.getenv("LETTERBOXD_USER")}/films'
headers = {
    'User-Agent': 'Mozilla/5.0',
}

filmes = []
i = 1

while True:
    pagina = requests.get(
        url = f'{base_url}/page/{i}',
        headers = headers
    )
    print(f'Página {i} - Status: {pagina.status_code}')

    soup = bs(pagina.content, 'html.parser')

    poster_list = soup.find('ul', class_='poster-list')
    poster_list_img = poster_list.find_all('div', class_='film-poster')

    if len(poster_list_img) == 0:
        break

    for poster in poster_list_img:
        # print(poster.find('img')['alt'])
        filmes.append(poster.find('img')['alt'])
    i += 1

open('filmes.txt', 'w').write('\n'.join(filmes))