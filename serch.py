import tempfile

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

async def get_basketball_matches():
    # Настройка Selenium WebDriver
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Запуск без отображения окна браузера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # Указываем уникальную директорию для данных пользователя
    user_data_dir = tempfile.mkdtemp()  # Создаём временную директорию
    options.add_argument(f"user-data-dir={user_data_dir}")

    try:
        #driver.set_window_size(3840, 2160)  # Уменьшает размер окна в 2 раза

        driver.get("https://winline.ru/live")
        time.sleep(3)  # Даем время сайту загрузиться
        driver.execute_script("document.body.style.zoom='50%'")

        # Нажимаем на li с title="Баскетбол"
        basketball_li = driver.find_element(By.XPATH, "//li[@title='Баскетбол']")
        basketball_li.click()
        time.sleep(5)  # Ждем загрузки матчей

        # Прокручиваем страницу вниз для подгрузки данных
        last_count = 0
        while True:
            match_elements = driver.find_elements(By.CLASS_NAME, "card card--live ng-star-inserted")
            match_count = len(match_elements)

            if match_count == last_count:
                break  # Останавливаемся, если новые матчи не загружаются

            last_count = match_count

            # Используем JavaScript для плавной прокрутки
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(2)

        # Получаем HTML-код div с классом block-sport__champ-list block-sport__champ-list--longperiod
        champ_list_div = driver.find_element(By.CLASS_NAME,
                                             "block-sport__champ-list.block-sport__champ-list--longperiod")
        html_content = champ_list_div.get_attribute("outerHTML")

        # Сохраняем HTML в файл
        with open("champ_list.html", "w", encoding="utf-8") as file:
            file.write(html_content)


    finally:
        driver.quit()