import get_value


def get_tokken(file_name):
    """Принимаем путь файла, отдаёт ключ для авторизации на сайте
    :rtype: str
    """
    with open(file_name, 'r') as file:
        value = file.readline()

    return value


def get_value_prcie(file_name):
    """Принимает путь до файла с данными (новыми ценами), словарь Металл:цена
    :rtype: dict
    """
    with open(file_name, 'r') as file:
        data = file.readlines()

    value = {}
    for i in data:
        stroka = i.split()
        value.update({stroka[0]: stroka[1]})

    return value

def main(price_value):

    # Получаем словарь с текущеми ценами на цветной лом (в том числе и АКБ)
    init_value = get_value.get_cvetmet()


    if 'Медь' in price_value:
        new_price = price_value.get('Медь')
        old_price = init_value.get('Медь')
        # Обновляем цены на медь + сео заголовок.
        get_value.med_update(new_price, old_price, TOKKEN)

    if 'Акб' in price_value:
        new_price1 = price_value.get('Акб')
        old_price1 = init_value.get('Аккумуляторы')
        # Обновляем цены на акб + сео заголовок.
        get_value.akb_update(new_price1, old_price1, TOKKEN)


    # Функция создание двух списков, новые цены и старые
    new = []
    old = []
    for i in price_value:

        if i == 'Акб':
            old.append(init_value.get('Аккумуляторы'))
            new.append(price_value.get(i))
        else:
            new.append(price_value.get(i))
            old.append(init_value.get(i))

    get_value.cvetmet_editor(old, new, TOKKEN)


# Токкен для доступа к REST API сайта
TOKKEN = get_tokken('/home/moonz/PycharmProjects/metall52/tokken.txt')
