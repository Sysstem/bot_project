import telebot
from telebot import types
import time
bot = telebot.TeleBot("6811141380:AAGt_a-gfCrn6j4rmBBzgTImPfeg8dtt1fM")

"""@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "How are you doing?")

 @bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.send_message(message.chat.id, 'Your message is ' + message.text)
 """

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Текущее время")
    btn2 = types.KeyboardButton("Ввести время...")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}!".format(message.from_user), reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Текущее время"):
        bot.send_message(message.chat.id, 'Текущее вермя ' + time.strftime("%H:%M:%S"))
    elif(message.text == "Ввести время..."):
        msg = bot.send_message(message.chat.id, 'Введите дату: (день.месяц.год часы:минуты)')
        bot.register_next_step_handler(msg, setTime)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")

@bot.message_handler(commands=['time'])
def sendTime(message):
	structTime = time.localtime(time.time()) # Время типа struct_time(tm_year=2023 и т д)
	bot.send_message(message.chat.id, 'Сейчас ' + time.asctime()) #time.asctime() текущее время
	bot.send_message(message.chat.id, 'Время ' + str(structTime.tm_hour) + ':' + str(structTime.tm_min))
	bot.send_message(message.chat.id, 'Дата ' + time.strftime("%d.%m.%Y")) #%H:%M:%S  время, %d.%m.%Y дата
	
@bot.message_handler(commands=['parseTime'])
def parseTime(message):
    msg = bot.send_message(message.chat.id, 'Введите дату: (день.месяц.год часы:минуты)')
    bot.register_next_step_handler(msg, setTime)


def setTime(message):
    gotTime = time.strptime(message.text, "%d.%m.%Y %H:%M")
    bot.send_message(message.chat.id, 'Введенная дата:' + str(gotTime))


bot.infinity_polling()




""" 
@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "👋 Поздороваться"):
        bot.send_message(message.chat.id, text="Привеет")
    elif(message.text == "❓ Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как меня зовут?")
        btn2 = types.KeyboardButton("Что я могу?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
    
    elif(message.text == "Как меня зовут?"):
        bot.send_message(message.chat.id, "У меня нет имени..")
    
    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text="Поздороваться с читателями")
    
    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Поздороваться")
        button2 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")
 """