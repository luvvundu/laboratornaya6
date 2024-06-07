from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router

import requests

from Postgres.sqlal import session, Currency, Admin

#Импорт кнопок

from KeyBoards.KeyBoard import main_f


router = Router()


class Curstate(StatesGroup):
    cur_name = State()
    cur_rate = State()

@router.message(F.text.lower() == "добавить валюту")
async def manage(message: Message, state: FSMContext):
    user_id = message.from_user.id
    admin = session.query(Admin).filter(Admin.chat_id == str(user_id)).first()
    if admin:
        await state.set_state(Curstate.cur_name)
        await message.answer('Введите название валюты')
    else:
        await message.answer('Непонятно')

@router.message(Curstate.cur_name)
async def process_currency_name(message: Message, state: FSMContext):
    currency_name = message.text.upper()

    # Проверяем, существует ли такая валюта уже в базе данных
    existing_currency = session.query(Currency).filter(Currency.currency_name == currency_name).first()
    if existing_currency:
        await message.answer('Эта валюта уже есть')

        await state.clear()
    else:
        # Сохраняем название валюты в состоянии
        await state.update_data(currency_name=message.text)
        await state.set_state(Curstate.cur_rate)
        await message.answer('Введите курс к рублю')


@router.message(Curstate.cur_rate)
async def process_currency_rate(message: Message, state: FSMContext):
    await state.update_data(cur_rate=message.text)
    # Получаем сохраненные данные о валюте из состояния
    data = await state.get_data()
    currency_name = data['currency_name'].upper()
    exchange_rate = message.text

    url = 'http://127.0.0.1:5001/load'
    data = {'currency_name': currency_name, 'rate': exchange_rate}
    try:
        response = requests.post(url, json=data)

        response_json = response.json()
        message_text = response_json.get('message')
        await message.answer(f"{message_text}")

        return response.text

        await state.clear()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    # Завершаем обработку команды
    await state.clear()

class CurstateDel(StatesGroup):
    cur_name_delete = State()

@router.message(F.text.lower() == "удалить валюту")
async def delete_currency(message: Message, state: FSMContext):
    user_id = message.from_user.id
    admin = session.query(Admin).filter(Admin.chat_id == str(user_id)).first()
    if admin:
        await state.set_state(CurstateDel.cur_name_delete)
        await message.answer('Введите название валюты, которую вы хотите удалить')
    else:
        await message.answer('Непонятно')

@router.message(CurstateDel.cur_name_delete)
async def confirm_delete_currency(message: Message, state: FSMContext):
    currency_name = message.text.upper()
    await state.update_data(cur_name_delete=currency_name)

    url = 'http://127.0.0.1:5001/delete'
    data = {'currency_name': currency_name}
    try:
        response = requests.post(url, json=data)
        response_json = response.json()
        message_text = response_json.get('message')
        await message.answer(f"{message_text}")

        await state.clear()
        return response.text

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        await state.clear()  # Вызываем здесь, чтобы гарантировать очистку состояния при ошибке
        return None


class Curstate_new(StatesGroup):
    cur_nameNew = State()
    cur_rate_new = State()

@router.message(F.text.lower() == "изменить курс валюты")
async def change_currency_rate(message: Message, state: FSMContext):
    user_id = message.from_user.id
    admin = session.query(Admin).filter(Admin.chat_id == str(user_id)).first()
    if admin:
        await state.set_state(Curstate_new.cur_nameNew)
        await message.answer('Введите название валюты, для которой вы хотите изменить курс')
    else:
        await message.answer('Непонятно')


@router.message(Curstate_new.cur_nameNew)
async def request_new_rate(message: Message, state: FSMContext):
    currency_name_new = message.text.upper()
    # Проверяем, существует ли такая валюта в базе данных
    existing_currency = session.query(Currency).filter(Currency.currency_name == currency_name_new).first()
    if existing_currency:
        # Сохраняем название валюты в состоянии и запрашиваем новый курс
        await state.update_data(cur_nameNew=currency_name_new)
        await state.set_state(Curstate_new.cur_rate_new)
        await message.answer('Введите новый курс к рублю для валюты')
    else:
        await message.answer('Данной валюты нет в базе данных.')
        await state.clear()


@router.message(Curstate_new.cur_rate_new)
async def update_currency_rate(message: Message, state: FSMContext):
    new_rate = message.text
    await state.update_data(cur_rate_new=new_rate)
    currency_name = (await state.get_data())['cur_nameNew']
    # Обновляем курс валюты в базе данных
    url = 'http://127.0.0.1:5001/update_currency'
    data = {'currency_name': currency_name, 'new_rate': new_rate}
    try:
        response = requests.post(url, json=data)

        response_json = response.json()
        message_text = response_json.get('message')
        await message.answer(f"{message_text}")

        await state.clear()
        return response.text

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        await state.clear()  # Вызываем здесь, чтобы гарантировать очистку состояния при ошибке
        return None

@router.message()
async def admin_panel(message: Message):
    msg = message.text.lower()
    if msg == 'выйти из режима редактирования валюты':
        msg = message.text.lower()
        print("Получено сообщение:", msg)
        print("Удаление кастомной клавиатуры...")
        await message.answer("Выход из режима", reply_markup=None)
        print("Кастомная клавиатура удалена")
    else:
        await message.answer('Сообщение не распознано')