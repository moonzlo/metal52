from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def ucalc_changer(new_price: int, config) -> bool:

    def linux_config():
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')  # Без GUI
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument(r"user-data-dir=/home/moonz/profile")
        driver = webdriver.Chrome(executable_path="/home/moonz/selenium/chromedriver", chrome_options=options)
        return driver

    def windows_config():
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=/home/moonz/profile")
        driver = webdriver.Chrome(executable_path="/home/moonz/chromedriver", chrome_options=options)
        return driver

    def ucalc_login():
        browser.implicitly_wait(10)
        browser.get('https://ucalc.pro/#login')
        sleep(2)
        browser.find_element_by_id('login_email').send_keys('mihail.moonz@gmail.com')
        browser.find_element_by_id('login_password').send_keys('SnowKiller216')
        browser.find_element_by_xpath('//button[@class="btn_prior"]').click()
        sleep(2)
        browser.get('https://ucalc.pro/create/17716/103271')
        sleep(3)
        browser.execute_script(f'SAVER.getResultBy("id", 1).formula="E-N%×{new_price}"; ')
        browser.execute_script('RECALC.go();')
        browser.execute_script('SAVER.publish("publish");')

    browser = None

    try:
        if config == 'linux':
            browser = linux_config()
            ucalc_login()

        else:
            browser = windows_config()


    except Exception as error:
        print(f'Ошибка в локальном скупе сленеиум: {error}')

    finally:
        browser.close()
        sleep(1)
        browser.quit()

    return True
