# Системные библиотеки
import threading
import logging
import os
import asyncio
from Hendlers import UserComand, UserMessenge
from Postgres import sqlal
from aiogram import Router


# Библиотеки aiogram
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand(command='start', description='Старт работы'),
            BotCommand(command='get_currencies', description='Список валют'),
            BotCommand(command='convert', description='Конвертирование валюты'),
            BotCommand(command='manage_currency', description='Управление валютой')

    ],
        scope=BotCommandScopeDefault()
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    token_bot = os.getenv('TOKEN_BOT')

    bot = Bot(token=token_bot)
    dp = Dispatcher()

    dp.include_routers(
        UserComand.router, UserMessenge.router
    )
    await set_default_commands(bot)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

