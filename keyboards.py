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
    [InlineKeyboardButton(text="📛 Удалить задачу", callback_data="removePlan"),
    InlineKeyboardButton(text="❌ Очистить список дел", callback_data="clearPlanner")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]
]

plans_list_kb = InlineKeyboardMarkup(inline_keyboard=plans_list)
planner_kb = InlineKeyboardMarkup(inline_keyboard=planner)
menu = InlineKeyboardMarkup(inline_keyboard=menu)

# Создать динамическую клавиатуру
def createKeyboard(jobsList: list) -> InlineKeyboardMarkup:
    targetList = []
    stepList = []
# Добавлять в массив пары клавиш (массивы)
    for i in range(len(jobsList)):
        stepList.append(InlineKeyboardButton(text=jobsList[i].name, callback_data=jobsList[i].id))
        if((i+1)%2 == 0):
            # Добавляем спаренные клавиши в targetList и обнуляем stepList
            targetList.append(stepList.copy())
            stepList = []

    # Если например длина массива задач 1, 3, 5 и т д, то последний элемент не в паре и не добавлен в targetList
    # поэтому добавляем его тут
    if(len(jobsList) % 2 != 0):
        targetList.append(stepList.copy())
    return InlineKeyboardMarkup(inline_keyboard=targetList)

#exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
#iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])