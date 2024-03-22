import telebot
import random
import string
from telebot import types

bot_token = "Token_bot"
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для генерации случайных паролей. Просто напиши /generate и я сгенерирую пароль для тебя.")

@bot.message_handler(commands=['generate'])
def generate_password(message):
    markup_digits = types.InlineKeyboardMarkup()
    markup_digits.row(types.InlineKeyboardButton('Да', callback_data='use_digits_yes'),
                      types.InlineKeyboardButton('Нет', callback_data='use_digits_no'))
    msg_digits = bot.send_message(message.chat.id, "Использовать цифры?", reply_markup=markup_digits)
    bot.register_next_step_handler(msg_digits, process_use_digits)

def process_use_digits(message):
    use_digits = message.text.lower() == 'да'
    markup_symbols = types.InlineKeyboardMarkup()
    markup_symbols.row(types.InlineKeyboardButton('Да', callback_data='use_symbols_yes'),
                       types.InlineKeyboardButton('Нет', callback_data='use_symbols_no'))
    msg_symbols = bot.send_message(message.chat.id, "Использовать символы?", reply_markup=markup_symbols)
    bot.register_next_step_handler(msg_symbols, lambda m: process_use_symbols(m, use_digits))

def process_use_symbols(message, use_digits):
    use_symbols = message.text.lower() == 'да'
    markup_length = types.InlineKeyboardMarkup()
    markup_length.row(types.InlineKeyboardButton('6', callback_data='length_6'),
                      types.InlineKeyboardButton('8', callback_data='length_8'),
                      types.InlineKeyboardButton('10', callback_data='length_10'),
                      types.InlineKeyboardButton('12', callback_data='length_12'),
                      types.InlineKeyboardButton('Другое', callback_data='custom_length'))
    msg_length = bot.send_message(message.chat.id, "Выберите количество символов в пароле:", reply_markup=markup_length)
    bot.register_next_step_handler(msg_length, lambda m: process_password_length(m, use_digits, use_symbols))

def process_password_length(message, use_digits, use_symbols):
    try:
        length = int(message.text)
        if length < 6:
            raise ValueError("Слишком короткий пароль. Выберите значение не менее 6.")
        password = generate_random_password(length, use_digits, use_symbols)
        bot.send_message(message.chat.id, f"Ваш случайный пароль: {password}")
        bot.delete_message(message.chat.id, message.message_id)  # Удаление предыдущего сообщения
    except ValueError as e:
        if message.text.lower() == 'другое':
            msg_custom_length = bot.send_message(message.chat.id, "Введите желаемое количество символов:")
            bot.register_next_step_handler(msg_custom_length, lambda m: process_password_length(m, use_digits, use_symbols))
        else:
            bot.send_message(message.chat.id, str(e))

def generate_random_password(length=12, use_digits=True, use_symbols=True):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data.startswith('use_digits'):
        use_digits = call.data.endswith('yes')
        markup_symbols = types.InlineKeyboardMarkup()
        markup_symbols.row(types.InlineKeyboardButton('Да', callback_data='use_symbols_yes'),
                           types.InlineKeyboardButton('Нет', callback_data='use_symbols_no'))
        bot.edit_message_text("Использовать символы?", call.message.chat.id, call.message.message_id, reply_markup=markup_symbols)
        bot.answer_callback_query(call.id)
    elif call.data.startswith('use_symbols'):
        use_symbols = call.data.endswith('yes')
        markup_length = types.InlineKeyboardMarkup()
        markup_length.row(types.InlineKeyboardButton('6', callback_data='length_6'),
                          types.InlineKeyboardButton('8', callback_data='length_8'),
                          types.InlineKeyboardButton('10', callback_data='length_10'),
                          types.InlineKeyboardButton('12', callback_data='length_12'),
                          types.InlineKeyboardButton('Другое', callback_data='custom_length'))
        bot.edit_message_text("Выберите количество символов в пароле:", call.message.chat.id, call.message.message_id, reply_markup=markup_length)
        bot.answer_callback_query(call.id)
    elif call.data.startswith('length'):
        length = int(call.data.split('_')[-1])
        use_digits = True  # По умолчанию
        use_symbols = True  # По умолчанию
        # Предыдущий текст сообщения не нужен, поэтому можно его удалить
        bot.delete_message(call.message.chat.id, call.message.message_id)
        try:
            password = generate_random_password(length, use_digits, use_symbols)
            bot.send_message(call.message.chat.id, f"Ваш случайный пароль: <pre>{password}</pre>", parse_mode="HTML")
        except ValueError as e:
            bot.send_message(call.message.chat.id, str(e))
        bot.answer_callback_query(call.id)

bot.polling()