from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
import asyncio
api = "_________________"
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()

@dp.message_handler()
async def start(message):
    await message.answer("Привет! Я бот, помогающий следить за здоровьем. Укажите свой пол.")
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def set_gender(message, state):
    gender = message.text.lower()
    if gender not in ["мужчина", "женщина"]:
        await message.answer("Пожалуйста, выберите 'Мужчина' или 'Женщина'.")
        return
    await state.update_data(gender=gender)
    await message.answer("Введите 'Calories', чтобы начать расчет калорий:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_age(message, state):
    if message.text.lower() == 'calories':
        await message.answer("Введите свой возраст.")
        return
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите возраст числом.")
        return
    await state.update_data(age=message.text)
    await message.answer(f"Принято! Ваш возраст: {message.text}")
    await message.answer('Введите свой рост.')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите рост числом.")
        return
    await state.update_data(growth=message.text)
    await message.answer(f"Принято! Ваш рост: {message.text}")
    await message.answer('Введите свой вес.')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_weight(message, state):
    await message.answer(f"Принято! Ваш вес: {message.text}")
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите вес числом.")
        return
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    gender = data['gender']

    if gender == 'мужчина':
        calories = 10 * weight + 6.25 * growth - 5 * age + 5
    else:
        calories = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f"Ваша норма калорий: {calories} ккал в день.")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)