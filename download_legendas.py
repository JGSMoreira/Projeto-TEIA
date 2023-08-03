import requests
import dotenv
import os

dotenv.load_dotenv()

api_key = os.getenv('OPEN_SUBTITLES_API_KEY')
base_url = 'https://api.opensubtitles.com/api/v1/'
token = os.getenv('OPEN_SUBTITLES_TOKEN')
headers = {
    'Accept': 'application/json',
    # 'Content-Type': 'application/json',
    'Api-Key': f'{api_key}',
    'Authorization': f'Bearer {token}',
    'User-Agent': 'ProjetoTEIA v1',
}

sub_ids = open('sub_ids.txt', 'r').readlines()
sub_nomes = open('sub_nomes.txt', 'r').readlines()
ultimo_id = open('ultimo_id.txt', 'r').read()

cota_restante = 200
subs_baixadas = 0
# ultimo_id = 0
index_inicial = 0

if ultimo_id != '':
    index_inicial = sub_ids.index(f'{ultimo_id}\n') + 1

for i in range(index_inicial, len(sub_ids)):
    sub_id = sub_ids[i]
    sub_nome = sub_nomes[i].split('\n')[0]

    if cota_restante == 0:
        print('Atingiu a cota diária, aguarde 24h')
        break

    if sub_id != '-\n' and sub_id != '-':
        print(f'{i+1:03d}/{len(sub_ids)} | {sub_nome} - {sub_id}')

        sub = requests.post(
            url = f'{base_url}download',
            headers = headers,
            json = {
                'file_id': sub_id,
            }
        )

        status = sub.status_code

        if status == 200:
            # print(sub.json())
            sub = sub.json()
            subs_baixadas += 1
            cota_restante = sub['remaining']
            ultimo_id = sub_id
            print('Baixando legenda...')
            legenda = requests.get(sub['link'], headers=headers).content
            print(f'Salvando legenda {subs_baixadas:03d}')
            open(f'legendas/{sub_nome}.srt', 'wb').write(legenda)
        else:
            print(f'Erro ao baixar legenda do filme com id {sub_id}')
            print(sub.content)
        
        print(f'Cota restante: {cota_restante}')

print(f'{subs_baixadas:03d} legenda(s) baixada(s) com sucesso')
print(f'Último id baixado: {ultimo_id}')
open('ultimo_id.txt', 'w').write(ultimo_id)





