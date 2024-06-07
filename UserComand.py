from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from Postgres.sqlal import session, Currency, Admin
from KeyBoards.KeyBoard import main_f
import requests

#Импорт кнопок


router = Router()

@router.message(Command('start'))
async def cmd_start(message: Message):
    user = message.from_user
    username = user.username if user.username else "Не указано"
    await message.answer(f'Добро пожаловать, {username}')

@router.message(Command('manage_currency'))
async def manage(message: Message):
    user_id = message.from_user.id
    params = {'user': user_id}
    try:
        response = requests.get('http://127.0.0.1:5000/check', params=params)
        if response.status_code == 200:
            message_text = response.json().get('message', 'error')
            await message.answer(f"{message_text}", reply_markup=main_f)
        else:
            await message.answer("У вас нет разрешения к функциям администратора")
    except Exception as e:
        await message.answer(f"{e} Не грустите")

# вывод валют
@router.message(Command('get_currencies'))
async def get_currencies(message: types.Message):
    try:
        response = requests.get('http://127.0.0.1:5002/currencies')
        data = response.json()
        message_text = data.get('message')
        for currency in message_text:
            await message.answer(f"Список валют с курсом к рублю:\n {currency['name']}: {currency['rate']}")
    except Exception as e:
        await message.answer("Произошла ошибка")


class ConvertCurrency(StatesGroup):
    amount_con = State()
    curr_con = State()

# Команда конвертация
@router.message(Command('convert'))
async def convert_currency(message: Message, state: FSMContext):
    await state.set_state(ConvertCurrency.curr_con)
    await message.answer("Введите валюту для конвертации:")

@router.message(ConvertCurrency.curr_con)
async def amount_currency(message: Message, state: FSMContext):
    await state.update_data(curr_con=message.text.upper())
    await state.set_state(ConvertCurrency.amount_con)
    await message.answer("Введите количество валюты:")

@router.message(ConvertCurrency.amount_con)
async def amount_currency_get(message: Message, state: FSMContext):
    amount_con = message.text
    await state.update_data(amount_con=message.text)
    data = await state.get_data()
    cur = data["curr_con"]

    await message.answer(f"Вы ввели {amount_con} {cur}, конвертация...")

    params = {'currency_name': cur, 'amount': amount_con}
    try:
        response = requests.get('http://127.0.0.1:5002/convert', params=params)
        data = response.json()
        message_text = data.get('message')
        await message.answer(f"{message_text}")
    except Exception as e:
        await message.answer("Произошла ошибка")

    await state.clear()

