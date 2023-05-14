from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove,KeyboardButton
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from random import randint
from aiogram.contrib.fsm_storage.memory import MemoryStorage
bot=Bot(token='5721307704:AAGFdU2ov3UcO5bItQTIhCE0bI3tgDAXzHI')
storage = MemoryStorage()
dp=Dispatcher(bot,storage=storage)

########### storage lists  ##############
temp =[]
cart=[]
id=""


############  Inventory and Offers ###################

button1 = InlineKeyboardButton(text="Inventory", callback_data="Inventory")  #callback is reference to the function
button2 = InlineKeyboardButton(text="Offers", callback_data="Offers")
keyboard_inline = InlineKeyboardMarkup().add(button1,button2)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    # Get the user's chat ID
    chat_id = message.chat.id
    id=message.chat.id
    cart.clear()

    # Save the user's name in the storage
    await storage.set_data(chat=chat_id, data={f'{chat_id}name': message.chat.first_name})

    # Send a greeting message
    await bot.send_message(chat_id=chat_id, text=f"Hello, {message.chat.first_name}!")
    await message.reply("Welcome to The EveryDay Market.", reply_markup=keyboard_inline)

# @dp.message_handler(commands=['start'])

# async def random_answer(message : types.Message):
#     await message.reply("Welcome to The EveryDay Market.", reply_markup=keyboard_inline)

@dp.message_handler(commands=['help'])
async def welcome(message: types.Message):
    await message.reply("Hello! In Gunther Bot, Please follows my YT channel")

@dp.callback_query_handler(text=["Inventory","Offers"])
async def random_value(call: types.CallbackQuery):
    global temp
    temp = []
    if call.data == "Inventory":
        inventorykeyboard = InlineKeyboardMarkup()
        button3 = InlineKeyboardButton(text="Milk Products", callback_data="milkProducts")
        button4 = InlineKeyboardButton(text="Soap and Shampoo", callback_data="soapandshampoo")
        button5 = InlineKeyboardButton(text="Facewash and shaving", callback_data="facewashandshaving")
        button6 = InlineKeyboardButton(text="House Cleaning", callback_data="housecleaning")
        button7 = InlineKeyboardButton(text="Grains", callback_data="grains")
        button8 = InlineKeyboardButton(text="Snacks", callback_data="snacks")
        button9 = InlineKeyboardButton(text="Tea and Biscuits", callback_data="teaandbiscuits")
        button10 = InlineKeyboardButton(text="Food", callback_data="food")
        button11= InlineKeyboardButton(text="Pooja Items", callback_data="poojaitems")
        inventorykeyboard.add(button3,button4,button5,button6,button7,button8,button9,button10,button11)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the category :", reply_markup=inventorykeyboard)
    if call.data == "Offers":
        await call.message.answer(randint(1,100))
    await call.answer()

############  Category functions ###################

@dp.callback_query_handler(text=["milkProducts","soapandshampoo","facewashandshaving","housecleaning","grains","snacks","teaandbiscuits","food","poojaitems"])
async def categoryfunction(call: types.CallbackQuery):
    global temp
    if call.data == "milkProducts":
        temp.append("Milk Products")
        milkkeyboard = InlineKeyboardMarkup()
        button12 = InlineKeyboardButton(text="250 ml Milk Packet ", callback_data="milk250")
        button13 = InlineKeyboardButton(text="500 ml Milk Packet", callback_data="milk500")
        button14 = InlineKeyboardButton(text="100 gm curd", callback_data="curd")
        button15 = InlineKeyboardButton(text="100 gm panner", callback_data="panner")        
        milkkeyboard.add(button12,button13,button14,button15)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the item :", reply_markup=milkkeyboard)
    if call.data == "Offers":
        await call.message.answer(randint(1,100))
    await call.answer()


############  Adding to cart   ###################
@dp.callback_query_handler(text=["milk250","milk500","curd","panner"])
async def quantityfunction(call: types.CallbackQuery):
        ###### milk products ######
        global temp
        if(call.data=="milk250"):
            temp.append("Milk 250 ml ")
            # print(temp)
        elif(call.data=="milk500"):
            temp.append("Milk 500 ml ")
        elif(call.data=="curd"):
            temp.append("curd ")
        if(call.data=="panner"):
            temp.append("Paneer ")
        quantitykeyboard = InlineKeyboardMarkup()
        button16 = InlineKeyboardButton(text="1 ", callback_data="q1")
        button17 = InlineKeyboardButton(text="2", callback_data="q2")
        button18 = InlineKeyboardButton(text="3", callback_data="q3")
        button19 = InlineKeyboardButton(text="4", callback_data="q4")        
        quantitykeyboard.add(button16,button17,button18,button19)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the quantity :", reply_markup=quantitykeyboard)
        await call.answer()

@dp.callback_query_handler(text=["q1","q2","q3","q4"])
async def finalcount(call: types.CallbackQuery):
    global temp,cart
    temp2 = []
    temp2 = temp.copy()
    if(call.data=="q1"):
        temp2.append(" 1 unit ")
        cart.append(temp2)
        await storage.set_data(chat=call.message.chat.id, data={'f{call.message.chat.id}': cart})
    elif(call.data=="q2"):
        temp2.append(" 2 units ")
        cart.append(temp2)
        await storage.set_data(chat=call.message.chat.id, data={'f{call.message.chat.id}': cart})
    elif(call.data=="q3"):
        temp2.append(" 3 units ")
        cart.append(temp2)
        await storage.set_data(chat=call.message.chat.id, data={'f{call.message.chat.id}': cart})
    elif(call.data=="q4"):
        temp2.append(" 4 units ")
        cart.append(temp2)
        await storage.set_data(chat=call.message.chat.id, data={'f{call.message.chat.id}': cart})
    data = await storage.get_data(chat=call.message.chat.id)
    await bot.send_message(chat_id=call.message.chat.id, text=f"{data.get('f{call.message.chat.id}','Unknown')}")
    temp.clear()
    await bot.send_message(chat_id=call.message.chat.id, text="Item added to cart", reply_markup=InlineKeyboardMarkup().add(button1))
    await call.answer()



executor.start_polling(dp)