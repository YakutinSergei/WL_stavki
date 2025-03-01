from bs4 import BeautifulSoup

from main import bot, CHAT_ID


async def analysis():
    # Читаем HTML-файл
    with open("champ_list.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Находим все карточки матчей
    matches = soup.find_all("div", class_="card card--live ng-star-inserted")

    for match in matches:
        # Названия команд
        teams = [team.text.strip().split('\n')[0] for team in match.find_all("div", class_="card__competitors")]

        # Текущий период
        period = match.find("span", class_="header-left__time ng-star-inserted")  # Нужно уточнить точный класс
        period_text = period.text.strip() if period else "Нет данных"

        # Текущий счет
        score = match.find("div", class_="ww-scores__total ng-star-inserted")  # Нужно уточнить класс
        score_text = score.text.strip() if score else "Нет данных"

        # Коэффициент на тотал

        total = match.find('div', class_='card__coeffs')

        # Находим все элементы с классом ww-feature-event-market-dsk внутри этого блока
        market_dsk_elements = total.find_all('ww-feature-event-market-dsk')

        # Берем третий элемент (индекс 2) и находим все span внутри него
        third_market_dsk = market_dsk_elements[2]

        # Находим все span внутри третьего элемента
        spans = third_market_dsk.find_all('span', class_='ng-star-inserted')

        kof = []
        # Извлекаем и выводим текст из каждого span
        for span in spans:
            kof.append(span.get_text(strip=True))


        rez = rezult(period_text,
                     score_text,
                     kof)
        print(teams[0])
        if rez:
            text = f'Команды: {teams[0]}\n'\
                   f'Счет: {score_text}\n'\
                   f'Коэффициент: ТМ{kof[0]}\n'\
                   f'Тотал: {kof[1]}\n'\
                   f'Рахница: {rez}\n'

            print(f'Команды: {teams[0]}\n'
                  f'Счет: {score_text}\n'
                  f'Коэффициент: ТМ{kof[0]}\n'
                  f'Тотал: {kof[1]}\n'
                  f'Рахница: {rez}\n')
            await bot.send_message(text=text, chat_id=CHAT_ID)


def rezult(period_text,
           score_text,
           kof):
    if not "Пер.2" in period_text:
        print("Текст не содержит '2ч пер'")
        return False

    if score_text.split(' ')[0].isdigit():
        score_1 = int(score_text.split(' ')[0])
    else:
        return False

    score_2 = int(score_text.split(' ')[-1])

    score_total = float(kof[1])

    signal = score_total - (score_1 + score_2) * 2

    if signal > 14:
        return signal

    return False
