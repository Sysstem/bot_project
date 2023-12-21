from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

menu = [
    [InlineKeyboardButton(text="⏰ Узнать текущее время", callback_data="getCurrentTime"),
    InlineKeyboardButton(text="📝 Планировщик задач", callback_data="planner")]
]

planner = [
    [InlineKeyboardButton(text="✍ Запланировть новую задачу", callback_data="newPlan"),
    InlineKeyboardButton(text="📖 Просмотреть список задач", callback_data="checkPlanner")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]
]

plans_list = [
    [InlineKeyboardButton(text="✍ Удалить задачу", callback_data="removePlan"),
    InlineKeyboardButton(text=" Очистить список дел", callback_data="clearPlanner")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]
]

plans_list_kb = InlineKeyboardMarkup(inline_keyboard=plans_list)
planner_kb = InlineKeyboardMarkup(inline_keyboard=planner)
menu = InlineKeyboardMarkup(inline_keyboard=menu)

#exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
#iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])