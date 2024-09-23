import requests
import json



def getAllLiveries():
    url = 'https://api.infiniteflight.com/public/v2/aircraft?apikey=nvo8c790hfa9q3duho2jhgd2jf8tgwqw'
    response = requests.get(url)
    data = json.loads(response.text)

    # Verifica se 'result' está presente e é uma lista
    if 'result' in data and isinstance(data['result'], list):
        # Extrai 'aircraftName' de cada dicionário na lista e converte para um conjunto para remover duplicatas
        unique_liveries_set = set((livery['name'], livery['name']) for livery in data['result'])

        # Converte o conjunto de volta para uma lista
        unique_liveries_list = list(unique_liveries_set)

        # Ordena a lista alfabeticamente
        sorted_liveries_list = sorted(unique_liveries_list, key=lambda x: x[0])

        return sorted_liveries_list
    # Se não houver 'result' ou 'result' não for uma lista, retorna uma lista vazia
    return []



def get_user_status(name):

    paramentro = {"discourseNames": [name]}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    url = 'https://api.infiniteflight.com/public/v2/user/stats?apikey=nvo8c790hfa9q3duho2jhgd2jf8tgwqw'
    payload = requests.post(url, data=json.dumps(paramentro), headers=headers)
    x = json.loads(payload.text)
    return x['result']


def getUserFlights(userId):
    url = requests.get(f'https://api.infiniteflight.com/public/v2/users/{userId}/flights?apikey=nvo8c790hfa9q3duho2jhgd2jf8tgwqw')
    response = json.loads(url.text)
    return response['result']


def get_country_flags():
    url = 'https://api-paises.pages.dev/paises.json'
    response = requests.get(url)
    if response.status_code == 200:
        country_data = response.json()
        # Cria um dicionário que mapeia o código alfa-2 para a URL da imagem da bandeira
        flags = {item['pais']: item['img'] for item in country_data.values()}
        return flags
    return {}

def get_api_metar(icao):
    url = requests.get(f'https://api-redemet.decea.mil.br/mensagens/metar/{icao}?api_key=6yuRqn7NopffZcJ31aVCjEfPX1QGE4wJiM0NoD3P')
    response = json.loads(url.text)
    metar = response['data']['data'][0]['mens']
    return metar.rstrip('=')


def bandeirasPaises():
    return [
        {
            "pais": "BR",
            "bandeira": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/22px-Flag_of_Brazil.svg.png"
        },
        {
            "pais": "US",
            "bandeira": "https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg"
        },
        {
            "pais": "JP",
            "bandeira": "https://upload.wikimedia.org/wikipedia/en/9/9e/Flag_of_Japan.svg"
        },
        {
            "pais": "DE",
            "bandeira": "https://upload.wikimedia.org/wikipedia/en/b/ba/Flag_of_Germany.svg"
        },
        {
            "pais": "FR",
            "bandeira": "https://upload.wikimedia.org/wikipedia/en/c/c3/Flag_of_France.svg"
        },
        {
            "pais": "CN",
            "bandeira": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Flag_of_China.svg/22px-Flag_of_China.svg.png"
        },
        {
            "pais": "IN",
            "bandeira": "https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg"
        },
        {
            "pais": "RU",
            "bandeira": "https://upload.wikimedia.org/wikipedia/en/f/f3/Flag_of_Russia.svg"
        },
        {
            "pais": "GB",
            "bandeira": "https://upload.wikimedia.org/wikipedia/en/a/ae/Flag_of_the_United_Kingdom.svg"
        },
        {
            "pais": "IT",
            "bandeira": "https://upload.wikimedia.org/wikipedia/en/0/03/Flag_of_Italy.svg"
        },
        {
            "pais": "CA",
            "bandeira": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Flag_of_Canada_%28Pantone%29.svg/22px-Flag_of_Canada_%28Pantone%29.svg.png"
        },
        {
            "pais": "AU",
            "bandeira": "https://upload.wikimedia.org/wikipedia/en/b/b9/Flag_of_Australia.svg"
        },
        {
            "pais": "ES",
            "bandeira": "https://upload.wikimedia.org/wikipedia/en/9/9a/Flag_of_Spain.svg"
        },
        {
            "pais": "MX",
            "bandeira": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Flag_of_Mexico.svg/22px-Flag_of_Mexico.svg.png"
        },
        {
            "pais": "ZA",
            "bandeira": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Flag_of_South_Africa.svg/22px-Flag_of_South_Africa.svg.png"
        },
        {
            "pais": "AR",
            "bandeira": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Flag_of_Argentina.svg/22px-Flag_of_Argentina.svg.png"
        },
        {
            "pais": "KR",
            "bandeira": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Flag_of_South_Korea.svg/22px-Flag_of_South_Korea.svg.png"
        },
        {
            "pais": "TR",
            "bandeira": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Flag_of_Turkey.svg/22px-Flag_of_Turkey.svg.png"
        },
        {
            "pais": "NL",
            "bandeira": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Flag_of_the_Netherlands.svg/22px-Flag_of_the_Netherlands.svg.png"
        },
        {
            "pais": "SE",
            "bandeira": "https://upload.wikimedia.org/wikipedia/en/4/4c/Flag_of_Sweden.svg"
        }
    ]
