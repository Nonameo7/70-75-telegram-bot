# Кнопки
from telebot import types

# Кнопка отправки номера
def num_button():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    but1 = types.KeyboardButton('Отправить свой номер📞',
                                request_contact=True)

    # Добавляем кнопки в пространство
    kb.add(but1)
    return kb
def location_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but2 = types.KeyboardButton('Отправьте свою локацию',
                                request_location=True)
    kb.add(but2)
    return kb
