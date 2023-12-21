import asyncio
import logging
import time
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.utils.formatting import as_marked_list

import config
import keyboards

router = Router()
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()


class Planning(StatesGroup): # Планировщик (состояния)
	planner = State() 
	date_choise = State() # Состояние, когда пользователь вводит дату
	setting_plan_name = State()
	checking_plans = State()
	chose_for_delete = State()

@router.message(Command("start"))
async def echo_msg(message: types.Message):
	await message.answer(f'Привет, {message.from_user.full_name}', reply_markup=keyboards.menu)

# Главное меню
@router.callback_query(F.data == "menu")
async def openPlanner(query: types.CallbackQuery, state: FSMContext):
	await bot.send_message(query.message.chat.id, 'Меню', reply_markup=keyboards.menu)
	await state.clear()

# Получить текущее время
@router.callback_query(F.data == "getCurrentTime")
async def writeTime(query: types.CallbackQuery):
	structTime = time.localtime(time.time()) # Время типа struct_time(tm_year=2023 и т д)
	answerTime = 'Время ' + str(structTime.tm_hour) + ':' + str(structTime.tm_min) + ', Дата ' + time.strftime("%d.%m.%Y") #%H:%M:%S  время, %d.%m.%Y дата
	await bot.send_message(query.message.chat.id, answerTime)

# Открыть меню планнера
@router.callback_query(F.data == "planner")
async def openPlanner(query: types.CallbackQuery, state: FSMContext):
	await bot.send_message(query.message.chat.id, 'Планировщик задач', reply_markup=keyboards.planner_kb)
	await state.set_state(Planning.planner)

# Создать новую задачку
@router.callback_query(Planning.planner, F.data == "newPlan")
async def inputPlanName(query: types.CallbackQuery, state: FSMContext):
	await bot.send_message(query.message.chat.id, 'Введите название события')
	await state.set_state(Planning.setting_plan_name)

# Обработать название события, записать в state data и запросить время
@router.message(Planning.setting_plan_name, F.text)
async def inputPlanTime(message: types.Message, state: FSMContext):
	await state.update_data(planName = message.text)
	await bot.send_message(message.chat.id, 'Введите дату (день.месяц.год часы:минуты), когда вам необходимо получить уведомление:')
	await state.set_state(Planning.date_choise)

#Если от пользователя пришел не текст
@router.message(Planning.setting_plan_name)
async def inputPlanTime(message: types.Message, state: FSMContext):
	await bot.send_message(message.chat.id, 'Упс! Попробуй ввести название события еще раз')

# Дата выбрана, создаем работу scheduler'у, если это возможно
@router.message(Planning.date_choise, F.text.regexp(r'\d{1,2}.\d{1,2}.\d{4}\s+\d{1,2}:\d{2}'))
async def timeGot(message: types.Message, state: FSMContext):
	try:
		gotTime = time.strptime(message.text, "%d.%m.%Y %H:%M") # получаем данные типа struct_time(tm_year=2023 и т д)
		user_data = await state.get_data()
		jobsCntr = len(scheduler.get_jobs())
		jobid = f"job_{jobsCntr+1}_{message.chat.id}"
		scheduler.add_job(
			sendNotification,
			"date",
			run_date=datetime(gotTime.tm_year, gotTime.tm_mon, gotTime.tm_mday, gotTime.tm_hour, gotTime.tm_min),
			args=(message.chat.id, user_data['planName'], ), #это кортеж touple
			name=user_data['planName'],
			id=jobid
		)
		await bot.send_message(message.chat.id, 'Событие успешно внесено в список дел!')
	except ValueError:
		# Если дата выходит за рамки (типа 40.13.2000 33:33)
		await bot.send_message(message.chat.id, 'Введена некорректная дата!')
	finally:
		await bot.send_message(message.chat.id, 'Планировщик задач', reply_markup=keyboards.planner_kb)
		await state.set_state(Planning.planner)

# Если регулярка не прошла проверку
@router.message(Planning.date_choise)
async def timeGotIncorrect(message: types.Message):
	await bot.send_message(message.chat.id, 'Введенная дата некорректна, попробуйте еще раз')

# Непосредственно функция отправки уведомления
async def sendNotification(chatid, text):
	await bot.send_message(chatid, f'Внимание! У вас сейчас {text}')

# Составляем список задач и выводим его пользователю
@router.callback_query(Planning.planner, F.data == "checkPlanner")
async def checkPlans(query: types.CallbackQuery, state: FSMContext):
	jobsList = scheduler.get_jobs()
	if(len(jobsList) == 0):
		await bot.send_message(query.message.chat.id, 'В планировщике пусто 👻👀', reply_markup=keyboards.planner_kb)
		return
	itemsForDisplay = as_marked_list(*list(map(lambda x: f"{x.name} ({x.next_run_time.strftime('%d %b %Y, %H:%M')})", jobsList)), marker="✅  ")
	await bot.send_message(query.message.chat.id, **itemsForDisplay.as_kwargs(), reply_markup=keyboards.plans_list_kb)
	await state.set_state(Planning.checking_plans)

@router.callback_query(Planning.checking_plans, F.data == "clearPlanner")
async def clearPlanner(query: types.CallbackQuery, state: FSMContext):
	scheduler.remove_all_jobs()
	await bot.send_message(query.message.chat.id, 'Успешно удалены все задачи', reply_markup=keyboards.menu)
	await state.clear()


@router.callback_query(Planning.checking_plans, F.data == "removePlan")
async def removePlan(query: types.CallbackQuery, state: FSMContext):
	jobsList = scheduler.get_jobs()
	dynamicKeyboard = keyboards.createKeyboard(jobsList)
	await bot.send_message(query.message.chat.id, 'Выберите задачу для удаления', reply_markup=dynamicKeyboard)
	await state.set_state(Planning.chose_for_delete)


@router.callback_query(Planning.chose_for_delete)
async def removingPlan(query: types.CallbackQuery, state: FSMContext):
	jobsList = scheduler.get_jobs()
	#idRemovingPlan = jobsList
	scheduler.remove_job(str(query.data))
	await bot.send_message(query.message.chat.id, f'Задача {str(query.data)} успешно удалена')
	await bot.send_message(query.message.chat.id, 'Планировщик задач', reply_markup=keyboards.planner_kb)
	await state.set_state(Planning.planner)


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