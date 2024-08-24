from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
import asyncio

api = "__________________"
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
kb_calc = InlineKeyboardMarkup()
bt3 = InlineKeyboardButton(text="Рассчитать", callback_data='calories')
bt4 = InlineKeyboardButton(text="Формулы расчёта", callback_data='formulas')
kb_calc.add(bt3, bt4)
start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Выберите пол:')],
        [
            KeyboardButton(text='Мужчина'),
            KeyboardButton(text='Женщина')
        ]
    ],
    resize_keyboard=True
)


class UserState(StatesGroup):
    gender = State()
    btt = State()
    age = State()
    growth = State()
    weight = State()


@dp.message_handler()
async def main_menu(message):
    await message.answer("Привет! Я бот, помогающий следить за здоровьем. Укажите свой пол.", reply_markup=start_menu)
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def set_gender(message, state):
    gender = message.text.lower()
    if gender not in ["мужчина", "женщина"]:
        await message.answer("Пожалуйста, выберите 'Мужчина' или 'Женщина'.")
        return
    await state.update_data(gender=gender)
    await message.answer("Выберите действие:", reply_markup=kb_calc)
    await UserState.btt.set()


@dp.callback_query_handler(text='calories', state=UserState.btt)
async def calculate_calories(call):
    await call.message.answer("Введите свой возраст.")
    await call.answer()
    await UserState.age.set()


@dp.callback_query_handler(text='formulas', state=UserState.btt)
async def show_formulas(call, state):
    data = await state.get_data()
    gender = data.get('gender')
    # Формулы расчета калорий
    if gender == 'мужчина':
        formula = "Формула для мужчин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5"
    else:
        formula = "Формула для женщин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161"
    await call.message.answer(formula)
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_age(message, state):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите возраст числом.")
        return
    await state.update_data(age=int(message.text))
    await message.answer(f"Принято! Ваш возраст: {message.text}")
    await message.answer('Введите свой рост.')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите рост числом.")
        return
    await state.update_data(growth=int(message.text))
    await message.answer(f"Принято! Ваш рост: {message.text}")
    await message.answer('Введите свой вес.')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_weight(message, state):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите вес числом.")
        return
    await state.update_data(weight=int(message.text))
    await message.answer(f"Принято! Ваш вес: {message.text}")
    data = await state.get_data()

    age = data['age']
    growth = data['growth']
    weight = data['weight']
    gender = data['gender']

    if gender == 'мужчина':
        calories = 10 * weight + 6.25 * growth - 5 * age + 5
    else:
        calories = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f"Ваша норма калорий: {calories} ккал в день.")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
