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


def soup_obj(html: str) -> "class 'bs4.BeautifulSoup'":
    soup = bs(html, 'html.parser')
    return soup


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


def get_price(soup: "class 'bs4.BeautifulSoup'") -> dict:
    """
    Служит для получения актуальнго прайса цена на цветные металлы.
    :param soup: объект супа для работы с парсенгом, использует html
    :return: dict = словарь из название типов металла и его цены | {'Медь':320}
    """
    a = soup.find_all('tr')

    names = []
    price = []

    for i in a[1:]:
        value = i.find('a')
        names.append(value.text)
        prices = str(i.find_all('td')[1].text).split()
        if len(prices) > 1:
            price.append(prices[0])
        else:
            price.append('None')

    data = {}
    for x, y in zip(names, price):
        data.update({x: y})

    return data


def color_metal_changer(html: str, value: dict, data: dict, soup: "class 'bs4.BeautifulSoup'") -> str:
    """
    Данная функция служит для генерация нового html кода страницы с цветным ломом.
    Задача функции заменить старые цены на новые.
    :param html: str   | Валидный код текущего состояния страницы с цветным ломом.
    :param value: dict | Словарь из текущих цен на цветной лом в формате {'Медь':'330'}
    :param data: dict  | Словарь с ключами которые нужно заменить, каждый ключ это индекс ключа value
    :param soup: class | Объект bs4 для парсинга стараницы, в изоляции кушает меньше памяти.
    :return: html: str | Возвращает исправленный html код который нужно передать в get_request
    """

    table_str = soup.find_all('tr')
    metal_name = list(value.keys())  # Ключи = Имена металлов.
    index_name = data.keys()  # Ключи = Индексы имён.
    update_data = {}

    for i in index_name:
        # current_price = value.get(metal_name[i])
        update_data.update({metal_name[i]: data.get(i)})

    for html_str in table_str:  # проходимся по всем строка таблицы.
        current_line = html_str  # html код текущей строки таблицы.
        for m_name in update_data:  # проходим по всем ключам/именам металлов которые нужно заменить.

            if str(m_name) in str(current_line):
                """
                Прежде всего нужно заменить стару цену на новую, а потом всё строку нового кода вставить
                вместо старого. Такой подход гарантирует что в случае появление одинаковых цен в таблице
                код будет изменяться только нужная. P.S первая реализация просто делал замену цены,
                по этому возникали ситуации кода несколько разных типов лома стояли одинаково =) 
                """
                current_price = str(current_line).replace(value.get(m_name), update_data.get(m_name))
                html = str(html).replace(str(current_line), current_price)

    return html


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


index_name = {0: '330', 1: '220'}
html1 = get_request('https://metal52.ru/prinimaem/cvetnoj-lom/')

sup = soup_obj(html1)
price = get_price(sup)
test = color_metal_changer(html, price, index_name, sup)
print(color_metal_changer.__doc__)

# post https://metal52.ru/wp-json/wp/v2/pages/1004
