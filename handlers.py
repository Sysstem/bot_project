from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

import time

import keyboards

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer('Привет', reply_markup=keyboards.menu)

@router.callback_query(F.data == "getCurrentTime")
async def answerTime(msg):
    await msg.send_message('Сейчас ' + time.asctime())  #time.asctime() текущее время

    """ bot.send_message(message.chat.id, 'Сейчас ' + time.asctime()) #time.asctime() текущее время
	bot.send_message(message.chat.id, 'Время ' + str(structTime.tm_hour) + ':' + str(structTime.tm_min))
	bot.send_message(message.chat.id, 'Дата ' + time.strftime("%d.%m.%Y")) #%H:%M:%S  время, %d.%m.%Y дата
 """

