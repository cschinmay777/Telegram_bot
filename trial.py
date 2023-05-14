import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5721307704:AAGFdU2ov3UcO5bItQTIhCE0bI3tgDAXzHI'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Define your inventory list with items and their prices
inventory = {
    'Milk 250 ml': 20,
    'Milk 500 ml': 30,
    'Curd': 15,
    'Paneer': 50
}

# Define the states for the bot
class OrderStates(StatesGroup):
    item = State()
    quantity = State()

# Define the handler for the '/start' command
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Welcome to our grocery store!\n"
                        "Please use the inline keyboard below to select the items you wish to purchase.")

# Define the handler for the inline keyboard with the inventory list
@dp.callback_query_handler(lambda c: c.data in inventory.keys())
async def process_item(callback_query: types.CallbackQuery, state: FSMContext):
    item = callback_query.data
    await state.update_data(item=item)
    quantity_keyboard = InlineKeyboardMarkup()
    for i in range(1, 5):
        quantity_keyboard.add(InlineKeyboardButton(text=f"{i}", callback_data=f"quantity:{i}"))
    await bot.send_message(callback_query.from_user.id, "Please select the quantity:", reply_markup=quantity_keyboard)
    await callback_query.answer()

# Define the handler for the quantity keyboard
@dp.callback_query_handler(lambda c: c.data.startswith('quantity:'))
async def process_quantity(callback_query: types.CallbackQuery, state: FSMContext):
    quantity = int(callback_query.data.split(':')[1])
    async with state.proxy() as data:
        item = data['item']
    await state.update_data(quantity=quantity)
    total_price = inventory[item] * quantity
    await bot.send_message(callback_query.from_user.id, f"You have selected {item} x {quantity}\nTotal Price: {total_price} INR",
                            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Confirm", callback_data="confirm")))
    await callback_query.answer()

# Define the handler for confirming the order
@dp.callback_query_handler(lambda c: c.data == "confirm")
async def process_confirm(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        item = data['item']
        quantity = data['quantity']
    # You can add your code here to process the order and store it in a database or send it to the shop owner
    await bot.send_message(callback_query.from_user.id, "Your order has been confirmed. Thank you for shopping with us!",
                            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Shop again", callback_data="shop_again")))
    await state.finish()
    await callback_query.answer()

# Define the handler for shopping again
@dp.callback_query_handler(lambda c: c.data == "shop_again")
async def process_shop_again(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Welcome back to our grocery store!\nPlease use the inline keyboard below to select the items you wis")

executor.start_polling(dp)