import requests
import dotenv
import os

dotenv.load_dotenv()

api_key = os.getenv('OPEN_SUBTITLES_API_KEY')
base_url = 'https://api.opensubtitles.com/api/v1/'
token = os.getenv('OPEN_SUBTITLES_TOKEN')
headers = {
    'Accept': '*/*',
    'Api-Key': f'{api_key}',
    'User-Agent': 'ProjetoTEIA v1',
    'Authorization': f'Bearer {token}'
}

file_ids = open('ids.txt', 'r').readlines()
sub_ids = []
sub_nomes = []
i = 1

for id in file_ids:
    legendas = requests.get(
        url = f'{base_url}subtitles',
        headers = headers,
        params = {
            'imdb_id': id[2:],
            'languages': 'pt-br',
            'order_by': 'rating',
            'order_direction': 'desc'
        }
    )

    status = legendas.status_code
    legendas = legendas.json()['data']

    if status == 200 and len(legendas) > 0:
        primeiro = legendas[0]['attributes']
        file = primeiro['files'][0]
        print(f'{i:03d}/{len(file_ids)} | {primeiro["files"][0]["file_name"]} - {primeiro["files"][0]["file_id"]} - Rating: {primeiro["ratings"]}')
        if primeiro['ratings'] < 7:
            print('Nota baixa, ignorando legenda')
            sub_ids.append('-')
            sub_nomes.append('-')
        else:
            sub_ids.append(str(file['file_id']))
            sub_nomes.append(file['file_name'])
    else:
        print('Sem legendas')
        sub_ids.append('-')
        sub_nomes.append('-')
    i += 1

open('sub_ids.txt', 'w').write('\n'.join(sub_ids))
open('sub_nomes.txt', 'w').write('\n'.join(sub_nomes))
