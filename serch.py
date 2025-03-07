from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


async def get_basketball_matches():
    # Настройка Selenium WebDriver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Запуск без отображения окна браузера
    # options.add_argument("--disable-gpu")  # Отключаем GPU для работы в headless
    # options.add_argument("--no-sandbox")  # Отключаем sandbox (если это нужно)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://winline.ru/live")

        # Ожидаем, пока сайт полностью загрузится (например, элемент для баскетбольных матчей)
        wait = WebDriverWait(driver, 20)
        basketball_li = wait.until(EC.presence_of_element_located((By.XPATH, "//li[@title='Баскетбол']")))

        driver.execute_script("document.body.style.zoom='50%'")  # Масштабируем страницу

        # Нажимаем на li с title="Баскетбол"
        basketball_li.click()

        # Ожидаем загрузки матчей
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card.card--live.ng-star-inserted")))
        time.sleep(2)

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

        # Ожидаем загрузки элементов после прокрутки
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card.card--live.ng-star-inserted")))

        # Получаем HTML-код div с классом block-sport__champ-list block-sport__champ-list--longperiod
        champ_list_div = driver.find_element(By.CLASS_NAME,
                                             "block-sport__champ-list.block-sport__champ-list--longperiod")
        html_content = champ_list_div.get_attribute("outerHTML")

        # Сохраняем HTML в файл
        with open("champ_list.html", "w", encoding="utf-8") as file:
            file.write(html_content)

    finally:
        driver.quit()
