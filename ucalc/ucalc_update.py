from selenium import webdriver
from time import sleep

def ucalc_changer(new_price: int, path: str, config='linux'):
    """
    Служит для обновления цены на акколмуяторы внутри калькулятора реализованного на сервесе ucalc.
    :param new_price: новая цена за кг акб.
    :param path путь до файла с почтой и паролем.
    :param config: конифгурация среды в которой запусукается скрипт.
    :return: возваращет в идеальном случае True в случае ошибки возвращает её трэйсбэк.
    """

    def authorization(file_path: str) -> list:
        """
        Отдаёт логин и пароль взятые из файла (от ucalc)
        :param file_pach: путь к файлу с почтой и паролем.
        :return: list [mail@mail.ru, 'password']
        """
        data = []
        with open(file_path, 'r') as file:
            values = file.readlines()
            data.append(values[0].replace('\n', ''))
            data.append(values[1])
        return data

    def linux_config():
        options = webdriver.ChromeOptions()
        options.add_argument('headless')  # Без GUI
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path="/home/moonz/selenium/chromedriver", chrome_options=options)
        return driver

    def windows_config():
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(executable_path="/home/moonz/chromedriver", chrome_options=options)
        return driver

    def ucalc_login(autch):
        browser.implicitly_wait(10)
        browser.get('https://ucalc.pro/#login')
        sleep(2)
        browser.find_element_by_id('login_email').send_keys(autch[0])
        browser.find_element_by_id('login_password').send_keys(autch[1])
        browser.find_element_by_xpath('//button[@class="btn_prior"]').click()
        sleep(2)
        browser.get('https://ucalc.pro/create/17716/103271')
        sleep(3)
        browser.execute_script(f'SAVER.getResultBy("id", 1).formula="E-N%×{new_price}"; ')
        browser.execute_script('RECALC.go();')
        browser.execute_script('SAVER.publish("publish");')

    login = authorization(path)
    browser = None
    msg = 'ucalc был обновлён (цена на акб)'

    try:
        if config == 'windows':
            browser = windows_config()
            ucalc_login(login)
            return msg

        else:
            browser = linux_config()
            ucalc_login(login)
            return msg

    except Exception as error:
        print(f'Ошибка в локальном скупе сленеиум: {error}')
        return f'Произошла ошибка при обновлении цены на АКБ внутри калькулятора | {error}'

    finally:
        browser.close()
        sleep(1)
        browser.quit()


if __name__ == '__main__':
    test = ucalc_changer(39, '/home/moonz/gitGub/metal52/ucalc/login.txt')