# Основная логика бота
import telebot
import buttons
import database
import json

# Создаем объект бота
bot = telebot.TeleBot('8266782515:AAFd4XxAT2TFP1i4iYxoIQZsKJCVSimTXyU')



# === Функция для получения курса по коду ===
def get_rate(code):
    with open("json.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        if item["Ccy"] == code:
            return item["Rate"]
    return None


# === Сопоставление слов с кодами валют ===
CURRENCY_MAP = {
    "доллар": "USD",
    "usd": "USD",
    "евро": "EUR",
    "eur": "EUR",
    "рубль": "RUB",
    "рубля": "RUB",
    "rub": "RUB",
}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # Проверяем, зарегистрировался ли юзер
    if database.check_user(user_id):
        bot.send_message(user_id, 'Добро пожаловать!',reply_markup=buttons.location_button())
    else:
        bot.send_message(user_id, 'Здравствуйте! Давайте начнем регистрацию!\n'
                                  'Введите свое имя',
                         reply_markup=telebot.types.ReplyKeyboardRemove())

 # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)

@bot.message_handler(commands=['help'])
def help_command(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "📌 Справка по командам:\n\n"
                     "/start – начать работу и регистрацию\n"
                     "/help – показать это сообщение\n\n"
                     "🛠 Основные возможности:\n"
                     "• Регистрация с вводом имени, номера и локации\n"
                     "• Приветствие по имени\n"
                     "• Конвертер валют (тенге → евро, доллар, рубль)\n\n"
                     "👉 Чтобы начать конвертацию, нажмите кнопку «Конвертер валют» после регистрации")



# Этап получения имени
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Отлично! Теперь отправьте свой номер!',
                     reply_markup=buttons.num_button())
    # Переход на этап получения номера
    bot.register_next_step_handler(message, get_num, user_name)

# Этап получения номера
def get_num(message, user_name):
    user_id = message.from_user.id
    # Проверяем правильность отправки номера
    if message.contact:
        user_num = message.contact.phone_number
        # Регистрируем юзера
        database.register(user_id, user_name, user_num)
        bot.send_message(user_id, 'Регистрация прошла успешно!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Отправьте номер по кнопке!')
        # Возвращение на этап получени номера
        bot.register_next_step_handler(message, get_num, user_name)

# Этап получени локации
def get_location(message, user_name):
    user_id = message.from_user.id
    # Проверяем правильность отправления локации
    if message.location:
        latitude = message.location.latitude # широта
        longitude = message.location.longitude # долгота
        bot.send_message(user_id, f"Вы отправили локацию!\nШирота: {latitude}\nДолгота: {longitude}")



def currency_step(message):
    user_id = message.from_user.id
    txt = message.text.lower()
    code  = CURRENCY_MAP.get(txt)
    if code:
        rate = get_rate(code)
        if rate:
            bot.send_message(user_id, f"1 {txt} = {rate} сум", reply_markup=buttons.choose_buttons())
        else:
            bot.send_message(user_id, "Курс не найден", reply_markup=buttons.choose_buttons())
    else:
        bot.send_message(user_id, "Такой валюты нет", reply_markup=buttons.choose_buttons())



# Запуск бота
bot.polling(non_stop=True)