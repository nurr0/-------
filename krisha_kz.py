import csv
from datetime import datetime
from decimal import Decimal
import json
from time import sleep
from bs4 import BeautifulSoup
import requests



def parse_krisha(url, max_page):
    res_file = f'data/{datetime.now()}.csv'
    with open(res_file, "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            'id',
            'Ссылка',
            'Комнаты',
            'Кв. метры'
            'Адрес',
            'Цена',
            'Цена за кв.м')
            )    
    
    page = requests.get(url)

    for i in range(1, max_page+1):
        current_url = url+str(i)
        page = requests.get(current_url)
        if page.status_code != 200:
            print(f'Сервер ответил ошибкой, код - {page.status_code}')
            continue    
        soup = BeautifulSoup(page.text, 'html.parser')
        all_flats = soup.findAll('div', class_='a-card__header')

        for flat in all_flats:
            link_hot = flat.find('a', class_='a-card__title tm-click-checked-hot-adv')
            link_common = flat.find('a', class_='a-card__title')
            link = link_hot.get('href') if link_hot else link_common.get('href')
            description = link_hot.text if link_hot else link_common.text
            price = flat.find('div', class_='a-card__price').text.strip() 
            price_int = ''.join([x for x in price if x.isdigit()])
            adress_hot = flat.find('div', class_='a-card__subtitle tm-click-checked-hot-adv')
            adress_common = flat.find('div', class_='a-card__subtitle')
            adress = adress_hot.text.strip() if adress_hot else adress_common.text.strip()
            id = flat.find('a', class_='a-action a-action-note').get('data-a-id')
            description = description.split(', ')
            rooms = description[0]
            m_2 = Decimal(description[1].rstrip(' м²'))
            price_for_m_2 = Decimal(int(price_int) / m_2).quantize(Decimal('0.00'))

            with open(res_file, "a", encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow((
                    id,
                    f'krisha.kz{link}',
                    rooms,
                    m_2,
                    adress,
                    price,
                    price_for_m_2)
                )
        print(f'Обработана {i} страница из {max_page}')
        sleep(5)

url = 'https://krisha.kz/prodazha/kvartiry/astana/?page='
max_page = 1000

parse_krisha(url, max_page)