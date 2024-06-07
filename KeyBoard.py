from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



main_f = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = 'Добавить валюту'),
            KeyboardButton(text='Удалить валюту'),
            KeyboardButton(text="Изменить курс валюты"),

            KeyboardButton(text = 'Выйти из режима редактирования валюты')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard= True,
    input_field_placeholder='Выберите действие из меню'
)


