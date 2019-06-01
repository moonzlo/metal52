import requests, json
from bs4 import BeautifulSoup as bs


def get_token(token_pach: str) -> str:
    """
    Читает текстоый файл с ключом от REST API
    :param token_pach: str = путь к файлу .txt
    :return: str = возвращает строку с токеном.
    """
    with open(token_pach, 'r') as file:
        token = file.read()

    return token


TOKEN = get_token('token.txt')


def get_request(url: str) -> str:  # return html
    """
    Данная функция служит для полуения html кода страниц.
    :param url:
    :return: html code or status code error
    """
    session = requests.Session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Authorization': TOKEN}
    try:
        html = session.get(url, headers=header)
        if html.status_code == 200:
            return html.text

        else:
            return f'error, status_code = ({html.status_code})'

    except Exception as error:
        return str(error)


def post_request(value: dict, url: str) -> str:  # return status_code
    """
    Функция служит для отправик POST запроса на REST API сайта.
    :param value: dict = состоит из сео параметров и исходного кода страницы.
    :param url: str = ссылка на ту страницу данные которой требуется обновить.
    :return: str = статус операции (для потверждения успеха).
    """
    session = requests.Session()
    header = {
        'Content-Type': 'application/JSON',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 ('
                      'KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Authorization': TOKEN}

    data = json.dumps(value)

    try:
        post = session.post(url, data=data, headers=header)
        return str(post.status_code)

    except Exception as error:
        return str(error)


def get_price() -> dict:
    """
    Служит для получения актуальнго прайса цена на цветные металлы.
    :param url: ссылка на страницу https://metal52.ru/prinimaem/cvetnoj-lom/
    :return: dict = словарь из название типов металла и его цены | {'Медь':320}
    """
    url = 'https://metal52.ru/prinimaem/cvetnoj-lom/'
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


def color_metal_changer(value: dict, data: list) -> str:
    """
    Ожидается :param data = list = список со списком названий которые нужно изменить | [[Медь:320][Латунь:120]]
    Обновляет цены на странице с цветным ломам
    :param value: dict = словарь с наименованием металлов и цен.
    :return: str = статус успеха операции | возвращается из post_request
    """
    for metal in data:
        price_data = metal[0].split(':')  # 0 = Название металла | 1 = Новая цена
        if value.get(price_data[0]) != price_data[1]:
            value.update({price_data[0]: price_data[1]})

    # url = 'https://metal52.ru/prinimaem/cvetnoj-lom/'
    # status = post_request(value, url)
    return value


def med_changer(value: int) -> str:
    """
    Обновляет цену и сео заголову на Медь
    :param value: int = новая цена на медь.
    :return: str = статус успеха операции | возвращается из post_request
    """


def accumulator_changer(value: int) -> str:
    """
    Обновляет цену и сео заголову на Акб
    :param value: int = новая цена на аккомуляторы.
    :return: str = статус успеха операции | возвращается из post_request
    """


test_data = [['Медь:342'], ['Алюминий:56']]
test = color_metal_changer(get_price(), test_data)
print(test)

# post https://metal52.ru/wp-json/wp/v2/pages/1004