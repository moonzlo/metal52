"""
Основной функционал для обработки REST API wp

"""
import requests, json
from bs4 import BeautifulSoup as bs


def get_request(url: str) -> str:  # return html
    """
    Данная функция служит для полуения html кода страниц.
    :param url:
    :return: html code or status code error
    """
    session = requests.Session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:
        html = session.get(url, headers=header)
        if html.status_code == 200:
            return html.text

        else:
            return f'error status_code = {html.status_code}'

    except Exception as error:
        return str(error)


def post_request(value: dict, url: str) -> str:
    """
    Функция служит для отправик POST запроса на REST API сайта.
    :param value: dict = состоит из сео параметров и исходного кода страницы.
    :param url: str = ссылка на ту страницу данные которой требуется обновить.
    :return: str = статус операции (для потверждения успеха).
    """
    session = requests.Session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    data = json.dumps(value)
    try:
        post = session.post(url, data=data, headers=header)
        return str(post.status_code)

    except Exception as error:
        return str(error)


def get_price(url: str) -> dict:
    """
    Служит для получения актуальнго прайса цена на цветные металлы.
    :param url: ссылка на страницу https://metal52.ru/prinimaem/cvetnoj-lom/
    :return: dict = словарь из название типов металла и его цены | {'Медь':320}
    """
    soup = bs(get_request(url), 'html.parser')

    a = soup.find('table', class_='tftable')
    b = a.find_all('b')
    metals = ['Медь', 'Колонка медная', 'Латунь', 'Алюминий', 'Алюминиевые банки', 'Титан', 'Нихром', 'Свинец',
              'Свинец(кабель)', 'Цинк', 'Нержа', 'Электродвигатели', 'Магний', 'Аккумуляторы', 'Медная стружка',
              'Латунная стружка', 'Алюминиевая стружка', 'Быстрорез Р6М5', 'ВК, ТК', ]

    values = []
    for i in b:
        ab = i.text
        if ab.isdigit():
            values.append(i.text)

    data = {}
    for x, y in zip(metals, values):
        data.update({x: y})

    return data


def color_metal_changer(value: dict) -> str:
    pass

def med_changer(value: str) -> str:
    pass

test = get_price('https://metal52.ru/prinimaem/cvetnoj-lom/')
print(test)