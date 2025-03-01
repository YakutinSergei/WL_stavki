import asyncio
import random

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from environs import Env

from serch import get_basketball_matches

env = Env()
env.read_env()

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logging.getLogger().setLevel(logging.WARNING)  # Устанавливает минимальный уровень логирования для терминала


TOKEN = env('BOT_TOKEN')  # Токен бота
CHAT_ID = env('CHAT_ID')  # ID группы для сообщений
# 🔹 Создаем бота и диспетчер
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())


# 🔹 Основной цикл мониторинга
async def monitoring():
    from pars import analysis
    while True:
        try:
            sleep_time = random.uniform(50, 70)  # Генерируем случайное число
            await get_basketball_matches()
            await analysis()
            await asyncio.sleep(sleep_time)
        except Exception as e:
            logging.error(f"Ошибка в monitoring: {e}")


# 🔹 Главная асинхронная функция
async def main():

    logging.info("Запуск бота...")
    await bot.send_message(text='Бот запущен', chat_id=CHAT_ID)
    asyncio.create_task(monitoring())
    await dp.start_polling(bot)



# 🔹 Запуск бота
if __name__ == "__main__":
    asyncio.run(main())