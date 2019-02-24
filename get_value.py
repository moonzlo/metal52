import requests, json
from bs4 import BeautifulSoup

def get_cvetmet():
    """Парсит ткущие цены на цветмет, формирует словарь Медь:340"""
    b = requests.Session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    html = b.get('https://metal52.ru/prinimaem/cvetnoj-lom/', headers=header).text
    soup = BeautifulSoup(html, 'html.parser')

    a = soup.find('table', class_='tftable')
    b = a.find_all('b')
    metalls = ['Медь', 'Колонка медная', 'Латунь', 'Алюминий', 'Алюминиевые банки', 'Титан', 'Нихром', 'Свинец',
               'Свинец(кабель)', 'Цинк', 'Нержа', 'Электродвигатели', 'Магний', 'Аккумуляторы', 'Медная стружка',
               'Латунная стружка', 'Алюминиевая стружка', 'Быстрорез Р6М5', 'ВК, ТК',]

    values = []
    for i in b:
        ab = i.text

        if ab.isdigit() == True:

            values.append(i.text)

    data = {}
    for x,y in zip(metalls, values):
        data.update({x:y})

    return data

def akb_update(new_price, price, tokken):
    """Данная функция служит для обновления цены на  страице АКБ"""

    b = requests.Session()
    header = {
        'Content-Type': 'application/JSON',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Authorization': tokken}


    with open('/home/moonz/PycharmProjects/metall52/akb.txt', 'r') as file:
        data = file.read()

    data1 = data.replace(f'{price}', f'{new_price}')


    body1 = {'content': data1}
    body2 = {"yoast_meta": {
        "yoast_wpseo_title": f"Сдать аккумулятор б/у цена за КГ от {new_price}₽ + демонтаж и вывоз",

    }}

    post = b.post('https://metal52.ru/wp-json/wp/v2/pages/137', data=json.dumps(body1), headers=header)
    post1 = b.post('https://metal52.ru/wp-json/wp/v2/pages/137', data=json.dumps(body2), headers=header)


def med_update(new_price, price, tokken):
    """Данная функция служит для изменения цен на странице Медь"""
    b = requests.Session()
    header = {
        'Content-Type': 'application/JSON',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Authorization': tokken}

    with open('/home/moonz/PycharmProjects/metall52/med.txt', 'r') as file:
        data = file.read()

    data1 = data.replace(f'{price}', f'{new_price}')


    body1 = {'content': data1}
    body2 = {"yoast_meta": {
        "yoast_wpseo_title": f"Цена на медь сегодня {new_price}₽ за кг Демонтируем и Вывозим",

    }}

    post = b.post('https://metal52.ru/wp-json/wp/v2/pages/192', data=json.dumps(body1), headers=header)
    post1 = b.post('https://metal52.ru/wp-json/wp/v2/pages/192', data=json.dumps(body2), headers=header)

def cvetmet_editor(old_price, new_price, tokken):
    """Данная функция служит для внесения изменений на страницу с таблицей цветмета"""

    with open('/home/moonz/PycharmProjects/metall52/cvetmet.txt', 'r') as file:
        data = file.read()

    # Меням старые значения на новые.
    for x,y in zip(old_price, new_price):
        if x != None:
            data = data.replace(f'{x}', f'{y}')


    body1 = {'content': data}
    b = requests.Session()
    header = {
        'Content-Type': 'application/JSON',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Authorization': tokken}
    post = b.post('https://metal52.ru/wp-json/wp/v2/pages/131', data=json.dumps(body1), headers=header)
