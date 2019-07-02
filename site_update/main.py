import requests, json
from ucalc import ucalc_update
from lxml import html, etree


def get_token(token_pach: str) -> str:
    # POST https://metal52.ru/wp-json/jwt-auth/v1/token?username=metal52&password=*****
    """
    Читает текстоый файл с ключом от REST API
    :param token_pach: str = путь к файлу .txt
    :return: str = возвращает строку с токеном.
    """
    with open(token_pach, 'r', encoding='utf-8') as file:
        token = file.read()

    return token


TOKEN = get_token('token.txt')


def lxml_tree() -> list:
    """
    Служит для формирования сапска строк из таблицы цветного лома.
    :param html: исходный код текущего состояния страницы.
    :return: list | Список из строк значеним которых является блок tr.
    """
    with open('color_metal_changer.html', 'r', encoding='utf-8') as file:
        html_str = file.read()  # Валидный исходный код для страницы.
    value = []   # Список из строковых значений для передачи в color_metal_changer
    tree = etree.HTML(html_str)
    for block in tree.xpath("//tr"):
        value.append(html.tostring(block, encoding='unicode'))

    return value



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
        'Authorization': TOKEN,
        'Content-Type': 'application/json; charset=utf-8'}
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
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 ('
                      'KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Authorization': TOKEN,
    }

    data = json.dumps(value)

    try:
        post = session.post(url, data=data, headers=header)
        return str(post.status_code)

    except Exception as error:
        return str(error)


def get_price() -> dict:
    page = requests.get('https://metal52.ru/prinimaem/cvetnoj-lom/').text
    tree = etree.HTML(page)

    metal_names = []
    metal_price = []

    for block in tree.xpath("//tr")[1:]:
        # Проходимся по всем строка таблицы и заберам имена металлов.
        try:
            line = block[0].xpath("a")[0]
            metal_names.append(line.xpath('b')[0].text)
            metal_price.append(block[1].xpath('b')[0].text)
        except IndexError:
            metal_price.append('договорная')

    data = {}
    for x, y in zip(metal_names, metal_price):
        data.update({x: y})

    return data


def color_metal_changer(value: dict, data: dict, ) -> str:
    """
    Индесы металов:
    0  = Медь
    1  = Колонка медная
    2  = Латунь
    3  = Алюминий
    4  = Алюминиевые банки
    5  = Титан
    6  = Нихром
    7  = Свинец
    8  = Свинец(кабель)
    9  = Цинк
    10 = Лом нержавеющий стали (никельсодержащий)
    11 = Лом кабеля медного и алюминиевого , как очищенный так и в оплетке
    12 = Электродвигатели
    13 = Магний
    14 = Трансформаторы
    15 = Аккумуляторы
    16 = Прокат медный, бронзовый, латунный, алюминиевый, нержавеющий
    17 = Никель
    18 = Медная стружка
    19 = Латунная стружка
    20 = Алюминиевая стружка
    21 = Быстрорез Р6М5
    22 = ВК, ТК
    23 = Олово
    24 = Вольфрам, молибден, ванадий

    Данная функция служит для генерация нового html кода страницы с цветным ломом.
    Задача функции заменить старые цены на новые.

    :param value: dict | Словарь из текущих цен на цветной лом в формате {'Медь':'330'}
    :param data: dict  | Словарь с ключами которые нужно заменить, каждый ключ это индекс ключа value
    :param soup: class | Объект bs4 для парсинга стараницы, в изоляции кушает меньше памяти.
    :return: html: str | Возвращает исправленный html код который нужно передать в get_request
    """

    table_str = lxml_tree()[1:]       # list из строк таблицы.
    metal_name = list(value.keys())   # Ключи = Имена металлов.
    index_name = data.keys()          # Ключи = Индексы имён.
    update_data = {}                  # Название лома : новая цена.

    with open('color_metal_changer.html', 'r', encoding='utf-8') as file:
        template = file.read()        # Валидный исходный код для страницы.

    for i in index_name:              # Формирование словаря с новыми ценами.
        update_data.update({metal_name[i]: data.get(i)})

    for html_str in table_str:        # проходимся по всем строка таблицы.
        current_line = html_str       # html код текущей строки таблицы.
        for m_name in update_data:    # проходим по всем ключам/именам металлов которые нужно заменить.

            if str(m_name) in str(current_line):
                """
                Прежде всего нужно заменить стару цену на новую, а потом всё строку нового кода вставить
                вместо старого. Такой подход гарантирует что в случае появление одинаковых цен в таблице
                код будет изменяться только нужная. P.S первая реализация просто делал замену цены,
                по этому возникали ситуации кода несколько разных типов лома стояли одинаково =) 
                """
                current_price = str(current_line).replace(value.get(m_name), update_data.get(m_name))

                template = template.replace(str(current_line), current_price)

    body = {'content': template}

    # TODO: Исправить ссылку на цветной лом.
    test_url = 'https://metal52.ru/wp-json/wp/v2/pages/1004'  # https://metal52.ru/wp-json/wp/v2/pages/131
    go_post = post_request(body, test_url)

    return go_post


def med_changer(value: int) -> str:
    """
    Обновляет цену и сео заголову на Медь
    :param value: int = новая цена на медь.
    :return: str = статус успеха операции | возвращается из post_request
    """

    pattern = '<strong><span style="color: #000000;">от 340</span> </strong>'
    good_data = f'<strong><span style="color: #000000;">от {value}</span> </strong>'

    with open('med.html', 'r') as file:
        old_data = file.read()

    new_data = {'content': old_data.replace(pattern, good_data),
                "yoast_meta": {
                    "yoast_wpseo_title": f"Цена на медь сегодня {value}₽ за кг Демонтируем и Вывозим"
                }}
    # TODO: Исравить ссылку на медь.
    demo_url = 'https://metal52.ru/wp-json/wp/v2/pages/1004'  # https://metal52.ru/wp-json/wp/v2/pages/192

    send = post_request(new_data, demo_url)

    return send


def accumulator_changer(value: int) -> str:
    """
    Обновляет цену и сео заголову на Акб
    :param value: int = новая цена на аккомуляторы.
    :return: str = статус успеха операции | возвращается из post_request
    """

    pattern = '<span style="color: #000000;"> <strong>38</strong> </span>рублей.'
    good_data = f'<span style="color: #000000;"> <strong>{value}</strong> </span>рублей.'

    with open('akkumuljatory.html', 'r', encoding='utf-8') as file:
        old_data = file.read()

    new_data = {'content': old_data.replace(pattern, good_data),
                "yoast_meta": {
                    "yoast_wpseo_title": f"Сдать аккумулятор б/у цена за КГ от {value}₽ + демонтаж и вывоз"
                }}
    # TODO: Исправить ссылку на АКБ
    demo_url = 'https://metal52.ru/wp-json/wp/v2/pages/1004'  # https://metal52.ru/wp-json/wp/v2/pages/137

    send = post_request(new_data, demo_url)

    return send


index_name = {0: '350', 1: '211'}
price = get_price()
test = color_metal_changer(price, index_name)
print(test)
# ucalc_update.ucalc_changer(39, 'linux')

# post https://metal52.ru/wp-json/wp/v2/pages/1004

