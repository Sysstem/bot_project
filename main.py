import asyncio
import logging
import time
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
import keyboards

router = Router()
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()


date_choise = State() # Состояние, когда пользователь вводит дату

@router.message(Command("start"))
async def echo_msg(message: types.Message):
	await message.answer(f'Привет, {message.from_user.full_name}', reply_markup=keyboards.menu)

@router.callback_query(F.data == "getCurrentTime")
async def writeTime(query: types.CallbackQuery):
	structTime = time.localtime(time.time()) # Время типа struct_time(tm_year=2023 и т д)
	answerTime = 'Время ' + str(structTime.tm_hour) + ':' + str(structTime.tm_min) + ', Дата ' + time.strftime("%d.%m.%Y") #%H:%M:%S  время, %d.%m.%Y дата
	await bot.send_message(query.message.chat.id, answerTime)


@router.callback_query(F.data == "inputTime")
async def inputTime(query: types.CallbackQuery, state: FSMContext):
	await bot.send_message(query.message.chat.id, 'Введите дату: (день.месяц.год часы:минуты)')
	await state.set_state(date_choise)


async def sendNotification(chatid):
	await bot.send_message(chatid, 'Внимание!')

@router.message(date_choise, F.text.regexp(r'\d{1,2}.\d{1,2}.\d{4}\s+\d{1,2}:\d{2}'))
async def timeGot(message: types.Message, state: FSMContext):
	try:
		gotTime = time.strptime(message.text, "%d.%m.%Y %H:%M") # получаем данные типа struct_time(tm_year=2023 и т д)
		await bot.send_message(message.chat.id, f'Введенная дата в struct_time:\n{str(gotTime)}')
		scheduler.add_job(
			sendNotification,
			"date",
			run_date=datetime(gotTime.tm_year, gotTime.tm_mon, gotTime.tm_mday, gotTime.tm_hour, gotTime.tm_min),
			args=(message.chat.id, )
		)
	except ValueError:
		# Если дата выходит за рамки (типа 40.13.2000 33:33)
		await bot.send_message(message.chat.id, 'Введена некорректная дата!')
	finally:
		await state.clear()
		await bot.send_message(message.chat.id, 'Что дальше?', reply_markup=keyboards.menu)


@router.message(date_choise)
async def timeGotIncorrect(message: types.Message):
	await bot.send_message(message.chat.id, 'Введенная дата некорректна, попробуйте еще раз')

@router.message()
async def echoall(msg: types.Message):
	await msg.answer('Такой команды нет(')

async def main():

	dp.include_router(router)

	await bot.delete_webhook(drop_pending_updates=True)
	scheduler.start()
	await dp.start_polling(bot)


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	asyncio.run(main())