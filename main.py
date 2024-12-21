from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor


# Создаем класс для состояний
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Инициализация бота и диспетчера
API_TOKEN = ''  # Замените на токен вашего бота
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Создание клавиатуры
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_calculate = types.KeyboardButton('Рассчитать')
button_info = types.KeyboardButton('Информация')
keyboard.add(button_calculate, button_info)


# Функция для начала ввода данных
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Привет! Я бот помогающий твоему здоровью:", reply_markup=keyboard)


# Функция для установки возраста
@dp.message_handler(lambda message: message.text == 'Рассчитать')
async def set_age(message: types.Message):
    await UserState.age.set()  # Установить состояние age
    await message.answer("Введите свой возраст:")


# Функция для установки роста
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)  # Сохранить возраст
    await UserState.growth.set()  # Установить состояние growth
    await message.answer("Введите свой рост:")


# Функция для установки веса
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)  # Сохранить рост
    await UserState.weight.set()  # Установить состояние weight
    await message.answer("Введите свой вес:")


# Функция для расчета нормы калорий
@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)  # Сохранить вес
    data = await state.get_data()  # Получить все данные


# Применим формулу Миффлина - Сан Жеора для мужчин
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

# Формула для расчета базального метаболизма (BMR)
    bmr = 10 * weight + 6.25 * growth - 5 * age + 5  # Для мужчин


# Убедитесь, что эти строки находятся внутри асинхронной функции
    await message.answer(f"Ваша норма калорий: {bmr:.2f} ккал.")
    await state.finish()  # Завершить состояние

# Хендлер для обработки любых других сообщений
@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Выберите команду /start, что бы начать общение.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
