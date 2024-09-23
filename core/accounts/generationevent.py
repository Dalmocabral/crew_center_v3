from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def scrape_data(url, tipo_evento):
    # Mapeamento entre os tipos de eventos e os valores de 'data-type' na página da web
    tipo_evento_map = {
        'departures': 'departures',
        'arrivals': 'arrivals'
    }

    # Verificar se o tipo de evento fornecido é válido
    if tipo_evento not in tipo_evento_map:
        raise ValueError("Tipo de evento inválido.")

    # Configurar o navegador controlado pelo Selenium
    options = Options()
    options.add_argument('--headless')  # Para executar em segundo plano, sem abrir uma janela de navegador
    driver = webdriver.Chrome(options=options)

    # Obter o conteúdo da página usando o navegador controlado pelo Selenium
    driver.get(url)
    html_content = driver.page_source

    # Fechar o navegador controlado pelo Selenium
    driver.quit()

    # Analisar o conteúdo HTML com BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Encontrar a tabela específica com base no tipo de evento
    data_type = tipo_evento_map[tipo_evento]
    table = soup.find('table', {'data-type': data_type})

    # Extrair os dados da tabela
    data = extract_table_data(table)

    return data

from datetime import datetime, timedelta

def extract_table_data(table):
    data = []

    if not table:
        return data

    # Remover o texto 'Partidas (Mais)' do cabeçalho
    headers = [header.text.strip() for header in table.find_all('th') if 'Partidas (Mais)' not in header.text.strip()]

    # Extrair os dados das linhas da tabela
    rows = table.find_all('tr')
    for row in rows[1:]:  # Ignorar o primeiro row que é o cabeçalho
        cols = row.find_all('td')
        if len(cols) >= 6:  # Verificar se há dados suficientes na linha
            voo = cols[0].text.strip()
            tipo = cols[1].text.strip()
            para = cols[2].text.strip()
            partida = cols[3].text.strip()
            chegada = cols[5].text.strip()

            # Verificar se o tipo não está vazio antes de adicionar o registro aos dados
            if tipo:
                # Verificar se a chegada não está vazia antes de tentar dividir
                if chegada:
                    chegada_split = chegada.split()
                    if chegada_split:
                        chegada_datetime = datetime.strptime(chegada_split[0], '%H:%M')

                        # Calcular a duração do voo
                        partida_datetime = datetime.strptime(partida.split()[0], '%H:%M')
                        duracao_voo = chegada_datetime - partida_datetime

                        # Adicionar a duração do voo ao formato HH:MM
                        duracao_formatada = str(duracao_voo).split('.')[0]

                        row_data = {
                            'voo': voo,
                            'tipo': tipo,
                            'para': para,
                            'partida': partida,
                            'chegada': chegada,
                            'duracao': duracao_formatada
                        }
                        data.append(row_data)

    return data