from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove,KeyboardButton
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from random import randint
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN ='6076013457:AAHNcMdefmfJyq49hKwdZ-nH2t5LUXZhsV0'
# API_TOKEN = '5943420461:AAEkeVh6Y-B4tT9WOvEAPhBTiBbIMNe62co'
Admin_chat_id="711477359"
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

button1 = InlineKeyboardButton(text="Inventory", callback_data="Inventory")
cartButton = InlineKeyboardButton(text="Cart", callback_data="Cart")
keyboardinline=InlineKeyboardMarkup().add(button1)
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    # Get the user's chat ID
    chat_id = message.chat.id
    
    await storage.set_data(user=chat_id, data={})
    # Save the user's name in the storage
    initialdata={f'{chat_id}name': message.chat.first_name,
                 'items':{'cart':[],
                          'count':0,
                          }}
    await storage.set_data(chat=chat_id, data=initialdata)

    # Send a greeting message
    await bot.send_message(chat_id=chat_id, text=f"Hello, {message.chat.first_name}!")
    await message.reply("Welcome to The EveryDay Market.", reply_markup=keyboardinline)

@dp.message_handler(commands=['stop'])
async def stop_bot(message: types.Message):
    # stop the long-polling mechanism
    await dp.stop_polling()

@dp.callback_query_handler(text=["Inventory"])
async def inventoryfunction(call: types.CallbackQuery):
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
        button12= InlineKeyboardButton(text="Chocklates and Cold Drinks", callback_data="chocklates")
        inventorykeyboard.add(button3,button4,button5,button6,button7,button8,button9,button10,button11,button12)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the category :", reply_markup=inventorykeyboard)
    await call.answer()

def dict_to_table(data):
    # Find the maximum length of each column
    #category_width = max(len(row['category']) for row in data['items']['cart'])
    item_width = max(len(row['item']) for row in data['items']['cart'])
    price_width = max(len(str(row['price/item'])) for row in data['items']['cart'])
    quantity_width = max(len(str(row['quantity'])) for row in data['items']['cart'])
    total_price_width = max(len(str(row['totalprice'])) for row in data['items']['cart'])

    # Define the table format using the column widths
    table_format = f"{{:<{item_width}}}  {{:<{price_width}}}  {{:<{quantity_width}}}  {{:<{total_price_width}}}\n"

    # Build the table header
    table = table_format.format('Item', 'Price/Item', 'Quantity', 'Total Price')
    table += '-' * (item_width + price_width + quantity_width + total_price_width + 4) + '\n'

    # Build the table rows
    for row in data['items']['cart']:
        table += table_format.format(row['item'], row['price/item'], row['quantity'], row['totalprice'])

    return table

def calculate_cart_total(data):
    total = 0
    for cart_item in data['items']['cart']:
        # cart_item['totalprice'] = cart_item['price/item'] * cart_item['quantity']
        total += cart_item['totalprice']
    # data['total'] = total
    return total

@dp.callback_query_handler(text=["Cart"])
async def cartfunction(call: types.CallbackQuery):
    user_id=call.from_user.id
    if call.data == "Cart":
        cartkeyboard = InlineKeyboardMarkup()
        orderButton = InlineKeyboardButton(text="Send Order", callback_data="sendOrder")
        cartkeyboard.add(orderButton)
        await bot.send_message(chat_id=call.message.chat.id, text=f"Your Cart \n {dict_to_table(await storage.get_data(user=user_id))} \n\n Total Price = {calculate_cart_total(await storage.get_data(user=user_id))}", reply_markup=cartkeyboard)
    await call.answer()

@dp.callback_query_handler(text=["sendOrder"])
async def sendorderfunction(call: types.CallbackQuery):
    user_id=call.from_user.id
    if call.data == "sendOrder":
        data=await storage.get_data(user=user_id)
        await bot.send_message(chat_id=Admin_chat_id, text=f"Name : {data[f'{user_id}name']} \n User id : {user_id}\n{dict_to_table(data)}")
        await bot.send_message(chat_id=user_id, text=f"Order Sent")
    await call.answer()

# define a message handler function message for accept and rehect
async def handle_message(message: types.Message):
    chat_id = message.chat.id
    text = message.text
    print(chat_id)    
    if(chat_id==int(Admin_chat_id)):
        msg=text.split(" ")[1]
        await bot.send_message(int(text.split(" ")[0]), f"{msg}")
    else:
        await bot.send_message(chat_id=chat_id,text="Sorry, I don't understand what you mean.")

dp.register_message_handler(handle_message)
    

@dp.callback_query_handler(text=["milkProducts"])
async def categoryfunction(call: types.CallbackQuery):
    if call.data == "milkProducts":
        user_id = call.from_user.id
        user_data = await storage.get_data(user=user_id)
        print("user_data = "+ str(user_data))
        print(user_id)
        print(type(user_data))
        cnt=user_data["items"]["count"]
        user_data['items']['cart'].append({'category':"milk products"})
        # user_data["items"]["count"]=cnt+1
        if(user_data==None):
            user_data={}
        await storage.set_data(user=user_id, data=user_data)        
        milkkeyboard = InlineKeyboardMarkup()
        button12 = InlineKeyboardButton(text="250 ml Milk Packet ", callback_data="milk250")
        button13 = InlineKeyboardButton(text="500 ml Milk Packet", callback_data="milk500")
        button14 = InlineKeyboardButton(text="100 gm curd", callback_data="curd")
        button15 = InlineKeyboardButton(text="100 gm panner", callback_data="panner")        
        milkkeyboard.add(button12,button13,button14,button15)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the item :", reply_markup=milkkeyboard)
    await call.answer()

@dp.callback_query_handler(text=["milk250","milk500","curd","panner"])
async def quantityfunction(call: types.CallbackQuery):
        ###### milk products ######
        if(call.data=="milk250"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="250 ml milk packet"
            user_data['items']['cart'][cnt]['price/item']=20
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="milk500"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="500 ml milk packet"
            user_data['items']['cart'][cnt]['price/item']=38
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="curd"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="100 gm amul Curd"
            user_data['items']['cart'][cnt]['price/item']=90
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="panner"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="100 gm Paneer"
            user_data['items']['cart'][cnt]['price/item']=80
            await storage.set_data(user=user_id, data=user_data)
             

             
        quantitykeyboard = InlineKeyboardMarkup()
        button16 = InlineKeyboardButton(text="1 ", callback_data="q1")
        button17 = InlineKeyboardButton(text="2", callback_data="q2")
        button18 = InlineKeyboardButton(text="3", callback_data="q3")
        button19 = InlineKeyboardButton(text="4", callback_data="q4")        
        quantitykeyboard.add(button16,button17,button18,button19)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the quantity :", reply_markup=quantitykeyboard)
        await call.answer()

@dp.callback_query_handler(text=["soapandshampoo"])
async def categoryfunction(call: types.CallbackQuery):
    if call.data == "soapandshampoo":
        user_id = call.from_user.id
        user_data = await storage.get_data(user=user_id)
        print("user_data = "+ str(user_data))
        print(user_id)
        print(type(user_data))
        cnt=user_data["items"]["count"]
        user_data['items']['cart'].append({'category':"soap and shampoo"})
        if(user_data==None):
            user_data={}
        await storage.set_data(user=user_id, data=user_data)        
        soapkeyboard = InlineKeyboardMarkup()
        dovebutton = InlineKeyboardButton(text="Dove Soap 35rs", callback_data="dove")
        dettolbutton = InlineKeyboardButton(text="Dettol Soap 30rs", callback_data="dettol")
        santoorbutton = InlineKeyboardButton(text="Santoor Soap 20rs", callback_data="santoor")
        clinicbutton = InlineKeyboardButton(text="Clinic Plus Shampoo 70rs", callback_data="clinic")        
        panteenbutton = InlineKeyboardButton(text="Panteen Shampoo 90rs", callback_data="panteen")        
        soapkeyboard.add(dovebutton,dettolbutton,santoorbutton,clinicbutton,panteenbutton)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the item :", reply_markup=soapkeyboard)
    await call.answer()

@dp.callback_query_handler(text=["dove","dettol","santoor","clinic","panteen"])
async def quantityfunction(call: types.CallbackQuery):
        ###### milk products ######
        if(call.data=="dove"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Dove Soap"
            user_data['items']['cart'][cnt]['price/item']=35
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="dettol"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Dettol Soap"
            user_data['items']['cart'][cnt]['price/item']=30
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="santoor"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Santoot Soap"
            user_data['items']['cart'][cnt]['price/item']=70
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="clinic"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Clinic Plus Shampoo"
            user_data['items']['cart'][cnt]['price/item']=90
            await storage.set_data(user=user_id, data=user_data)
             

             
        quantitykeyboard = InlineKeyboardMarkup()
        button16 = InlineKeyboardButton(text="1 ", callback_data="q1")
        button17 = InlineKeyboardButton(text="2", callback_data="q2")
        button18 = InlineKeyboardButton(text="3", callback_data="q3")
        button19 = InlineKeyboardButton(text="4", callback_data="q4")        
        quantitykeyboard.add(button16,button17,button18,button19)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the quantity :", reply_markup=quantitykeyboard)
        await call.answer()

@dp.callback_query_handler(text=["facewashandshaving"])
async def categoryfunction(call: types.CallbackQuery):
    if call.data == "facewashandshaving":
        user_id = call.from_user.id
        user_data = await storage.get_data(user=user_id)
        print("user_data = "+ str(user_data))
        print(user_id)
        print(type(user_data))
        cnt=user_data["items"]["count"]
        user_data['items']['cart'].append({'category':"facewash and shaving"})
        if(user_data==None):
            user_data={}
        await storage.set_data(user=user_id, data=user_data)        
        facekeyboard = InlineKeyboardMarkup()
        garnierbutton = InlineKeyboardButton(text="Garnier Acne Remover 135rs", callback_data="garnier")
        cleanbutton = InlineKeyboardButton(text="Clean and Clear 25rs", callback_data="clean")
        gilletebutton = InlineKeyboardButton(text="Gillette Gaurd 55rs", callback_data="gillete")
        oldbutton = InlineKeyboardButton(text="Old Spice Shaving Cream 75rs", callback_data="oldspice")         
        facekeyboard.add(garnierbutton,cleanbutton,gilletebutton,oldbutton)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the item :", reply_markup=facekeyboard)
    await call.answer()

@dp.callback_query_handler(text=["garnier","clean","gillete","oldspice"])
async def quantityfunction(call: types.CallbackQuery):
        ###### milk products ######
        if(call.data=="garnier"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Garnier Acne Remover facewash"
            user_data['items']['cart'][cnt]['price/item']=135
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="clean"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Clean and Clear facewash"
            user_data['items']['cart'][cnt]['price/item']=25
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="gillete"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Gillette Gaurd"
            user_data['items']['cart'][cnt]['price/item']=75
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="oldspice"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Old Spice Shaving Cream"
            user_data['items']['cart'][cnt]['price/item']=55
            await storage.set_data(user=user_id, data=user_data)
             

             
        quantitykeyboard = InlineKeyboardMarkup()
        button16 = InlineKeyboardButton(text="1 ", callback_data="q1")
        button17 = InlineKeyboardButton(text="2", callback_data="q2")
        button18 = InlineKeyboardButton(text="3", callback_data="q3")
        button19 = InlineKeyboardButton(text="4", callback_data="q4")        
        quantitykeyboard.add(button16,button17,button18,button19)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the quantity :", reply_markup=quantitykeyboard)
        await call.answer()

@dp.callback_query_handler(text=["housecleaning"])
async def categoryfunction(call: types.CallbackQuery):
    if call.data == "housecleaning":
        user_id = call.from_user.id
        user_data = await storage.get_data(user=user_id)
        print("user_data = "+ str(user_data))
        print(user_id)
        print(type(user_data))
        cnt=user_data["items"]["count"]
        user_data['items']['cart'].append({'category':"House Cleaning"})
        if(user_data==None):
            user_data={}
        await storage.set_data(user=user_id, data=user_data)        
        cleankeyboard = InlineKeyboardMarkup()
        galabutton = InlineKeyboardButton(text="Gala Broom 178rs", callback_data="gala")
        harpicbutton = InlineKeyboardButton(text="Harpic 100ml 45rs", callback_data="harpic")
        colinbutton = InlineKeyboardButton(text="Collin 85rs", callback_data="collin")
        hitbutton = InlineKeyboardButton(text="Red hit 175rs", callback_data="redhit")         
        cleankeyboard.add(galabutton,harpicbutton,colinbutton,hitbutton)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the item :", reply_markup=cleankeyboard)
    await call.answer()

@dp.callback_query_handler(text=["gala","harpic","collin","redhit"])
async def quantityfunction(call: types.CallbackQuery):
        ###### milk products ######
        if(call.data=="gala"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Gala No dust Broom"
            user_data['items']['cart'][cnt]['price/item']=178
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="harpic"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Harpic Cleaner"
            user_data['items']['cart'][cnt]['price/item']=45
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="collin"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Collin Glass Cleaner"
            user_data['items']['cart'][cnt]['price/item']=85
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="redhit"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Red Hit"
            user_data['items']['cart'][cnt]['price/item']=175
            await storage.set_data(user=user_id, data=user_data)
             

             
        quantitykeyboard = InlineKeyboardMarkup()
        button16 = InlineKeyboardButton(text="1 ", callback_data="q1")
        button17 = InlineKeyboardButton(text="2", callback_data="q2")
        button18 = InlineKeyboardButton(text="3", callback_data="q3")
        button19 = InlineKeyboardButton(text="4", callback_data="q4")        
        quantitykeyboard.add(button16,button17,button18,button19)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the quantity :", reply_markup=quantitykeyboard)
        await call.answer()

@dp.callback_query_handler(text=["grains"])
async def categoryfunction(call: types.CallbackQuery):
    if call.data == "grains":
        user_id = call.from_user.id
        user_data = await storage.get_data(user=user_id)
        print("user_data = "+ str(user_data))
        print(user_id)
        print(type(user_data))
        cnt=user_data["items"]["count"]
        user_data['items']['cart'].append({'category':"Grains"})
        if(user_data==None):
            user_data={}
        await storage.set_data(user=user_id, data=user_data)        
        grainkeyboard = InlineKeyboardMarkup()
        wheatbutton = InlineKeyboardButton(text="Wheat 17rs/kg", callback_data="wheat")
        attabutton = InlineKeyboardButton(text="Ashirwad Atta(5 kg) 245rs", callback_data="atta")
        ricebutton = InlineKeyboardButton(text="Indrayani Rice 85rs/kg", callback_data="rice")
        bajrabutton = InlineKeyboardButton(text="Bajra 59rs/kg", callback_data="bajra")         
        grainkeyboard.add(wheatbutton,attabutton,ricebutton,bajrabutton)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the item :", reply_markup=grainkeyboard)
    await call.answer()

@dp.callback_query_handler(text=["wheat","atta","rice","bajra"])
async def quantityfunction(call: types.CallbackQuery):
        ###### milk products ######
        if(call.data=="wheat"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Wheat 1kg"
            user_data['items']['cart'][cnt]['price/item']=17
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="atta"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Ashirwad Atta 5kg"
            user_data['items']['cart'][cnt]['price/item']=245
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="rice"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Indrayani Rice"
            user_data['items']['cart'][cnt]['price/item']=85
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="bajra"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Bajra 1kg"
            user_data['items']['cart'][cnt]['price/item']=59
            await storage.set_data(user=user_id, data=user_data)
             

             
        quantitykeyboard = InlineKeyboardMarkup()
        button16 = InlineKeyboardButton(text="1 ", callback_data="q1")
        button17 = InlineKeyboardButton(text="2", callback_data="q2")
        button18 = InlineKeyboardButton(text="3", callback_data="q3")
        button19 = InlineKeyboardButton(text="4", callback_data="q4")        
        quantitykeyboard.add(button16,button17,button18,button19)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the quantity :", reply_markup=quantitykeyboard)
        await call.answer()

@dp.callback_query_handler(text=["snacks"])
async def categoryfunction(call: types.CallbackQuery):
    if call.data == "snacks":
        user_id = call.from_user.id
        user_data = await storage.get_data(user=user_id)
        print("user_data = "+ str(user_data))
        print(user_id)
        print(type(user_data))
        cnt=user_data["items"]["count"]
        user_data['items']['cart'].append({'category':"Snacks"})
        if(user_data==None):
            user_data={}
        await storage.set_data(user=user_id, data=user_data)        
        snackkeyboard = InlineKeyboardMarkup()
        balajibutton = InlineKeyboardButton(text="Balaji Wafers 10rs", callback_data="balaji")
        soyabutton = InlineKeyboardButton(text="Soya sticks 20rs", callback_data="soya")
        diamondbutton = InlineKeyboardButton(text="Diamond Kurkure 5rs", callback_data="diamond")
        farsanbutton = InlineKeyboardButton(text="Farsan 1kg 85rs", callback_data="farsan")         
        snackkeyboard.add(balajibutton,soyabutton,diamondbutton,farsanbutton)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the item :", reply_markup=snackkeyboard)
    await call.answer()

@dp.callback_query_handler(text=["balaji","soya","diamond","farsan"])
async def quantityfunction(call: types.CallbackQuery):
        ###### milk products ######
        if(call.data=="balaji"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Balaji Wafers"
            user_data['items']['cart'][cnt]['price/item']=10
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="soya"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Soya Sticks"
            user_data['items']['cart'][cnt]['price/item']=20
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="diamond"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Diamond Kurkure"
            user_data['items']['cart'][cnt]['price/item']=5
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="farsan"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Farsan 1kg"
            user_data['items']['cart'][cnt]['price/item']=85
            await storage.set_data(user=user_id, data=user_data)
             

             
        quantitykeyboard = InlineKeyboardMarkup()
        button16 = InlineKeyboardButton(text="1 ", callback_data="q1")
        button17 = InlineKeyboardButton(text="2", callback_data="q2")
        button18 = InlineKeyboardButton(text="3", callback_data="q3")
        button19 = InlineKeyboardButton(text="4", callback_data="q4")        
        quantitykeyboard.add(button16,button17,button18,button19)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the quantity :", reply_markup=quantitykeyboard)
        await call.answer()

@dp.callback_query_handler(text=["teaandbiscuits"])
async def categoryfunction(call: types.CallbackQuery):
    if call.data == "teaandbiscuits":
        user_id = call.from_user.id
        user_data = await storage.get_data(user=user_id)
        print("user_data = "+ str(user_data))
        print(user_id)
        print(type(user_data))
        cnt=user_data["items"]["count"]
        user_data['items']['cart'].append({'category':"Tea and Biscuits"})
        if(user_data==None):
            user_data={}
        await storage.set_data(user=user_id, data=user_data)        
        teakeyboard = InlineKeyboardMarkup()
        parleibutton = InlineKeyboardButton(text="Parle G 10rs", callback_data="parle")
        hidebutton = InlineKeyboardButton(text="Hide and Seek 25rs", callback_data="hide")
        redbutton = InlineKeyboardButton(text="Red Label 250gm 45rs", callback_data="red")
        tajbutton = InlineKeyboardButton(text="Taj tea 100gm 75rs", callback_data="taj")         
        teakeyboard.add(parleibutton,hidebutton,redbutton,tajbutton)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the item :", reply_markup=teakeyboard)
    await call.answer()

@dp.callback_query_handler(text=["parle","hide","red","taj"])
async def quantityfunction(call: types.CallbackQuery):
        ###### milk products ######
        if(call.data=="parle"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Parle G"
            user_data['items']['cart'][cnt]['price/item']=10
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="hide"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Hide and Seek"
            user_data['items']['cart'][cnt]['price/item']=25
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="red"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Red Label 250gm"
            user_data['items']['cart'][cnt]['price/item']=45
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="taj"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Taj tea 100gm"
            user_data['items']['cart'][cnt]['price/item']=75
            await storage.set_data(user=user_id, data=user_data)
             

             
        quantitykeyboard = InlineKeyboardMarkup()
        button16 = InlineKeyboardButton(text="1 ", callback_data="q1")
        button17 = InlineKeyboardButton(text="2", callback_data="q2")
        button18 = InlineKeyboardButton(text="3", callback_data="q3")
        button19 = InlineKeyboardButton(text="4", callback_data="q4")        
        quantitykeyboard.add(button16,button17,button18,button19)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the quantity :", reply_markup=quantitykeyboard)
        await call.answer()

@dp.callback_query_handler(text=["food"])
async def categoryfunction(call: types.CallbackQuery):
    if call.data == "food":
        user_id = call.from_user.id
        user_data = await storage.get_data(user=user_id)
        print("user_data = "+ str(user_data))
        print(user_id)
        print(type(user_data))
        cnt=user_data["items"]["count"]
        user_data['items']['cart'].append({'category':"Food"})
        if(user_data==None):
            user_data={}
        await storage.set_data(user=user_id, data=user_data)        
        foodkeyboard = InlineKeyboardMarkup()
        chingsbutton = InlineKeyboardButton(text="Chings Schezwan 69rs", callback_data="chings")
        rambutton = InlineKeyboardButton(text="Ram-Bandhu Papad Masala 106rs", callback_data="ram")
        sabudanabutton = InlineKeyboardButton(text="Sabudana 1kg 63rs", callback_data="sabudana")
        idlibutton = InlineKeyboardButton(text="Idli Rava 51rs", callback_data="idli")         
        foodkeyboard.add(chingsbutton,rambutton,sabudanabutton,idlibutton)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the item :", reply_markup=foodkeyboard)
    await call.answer()

@dp.callback_query_handler(text=["chings","ram","sabudana","idli"])
async def quantityfunction(call: types.CallbackQuery):
        ###### milk products ######
        if(call.data=="chings"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Chings Schezwan Chutney"
            user_data['items']['cart'][cnt]['price/item']=69
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="ram"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Ram-Bandhu Papad Masala"
            user_data['items']['cart'][cnt]['price/item']=106
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="sabudana"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Sabudana 1kg"
            user_data['items']['cart'][cnt]['price/item']=63
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="idli"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Idli Rava"
            user_data['items']['cart'][cnt]['price/item']=51
            await storage.set_data(user=user_id, data=user_data)
             

             
        quantitykeyboard = InlineKeyboardMarkup()
        button16 = InlineKeyboardButton(text="1 ", callback_data="q1")
        button17 = InlineKeyboardButton(text="2", callback_data="q2")
        button18 = InlineKeyboardButton(text="3", callback_data="q3")
        button19 = InlineKeyboardButton(text="4", callback_data="q4")        
        quantitykeyboard.add(button16,button17,button18,button19)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the quantity :", reply_markup=quantitykeyboard)
        await call.answer()

@dp.callback_query_handler(text=["poojaitems"])
async def categoryfunction(call: types.CallbackQuery):
    if call.data == "poojaitems":
        user_id = call.from_user.id
        user_data = await storage.get_data(user=user_id)
        print("user_data = "+ str(user_data))
        print(user_id)
        print(type(user_data))
        cnt=user_data["items"]["count"]
        user_data['items']['cart'].append({'category':"Pooja Items"})
        if(user_data==None):
            user_data={}
        await storage.set_data(user=user_id, data=user_data)        
        poojakeyboard = InlineKeyboardMarkup()
        cyclebutton = InlineKeyboardButton(text="Cycle Agarbatti 10rs", callback_data="cycle")
        camphorbutton = InlineKeyboardButton(text="Bhimsen Camphor 100gm 270rs", callback_data="camphor")
        gandhabutton = InlineKeyboardButton(text="Ashthagandha 50rs", callback_data="gandha")
        mangaldeepbutton = InlineKeyboardButton(text="Mangaldeep Agarbatti 50rs", callback_data="mangaldeep")         
        poojakeyboard.add(cyclebutton,camphorbutton,gandhabutton,mangaldeepbutton)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the item :", reply_markup=poojakeyboard)
    await call.answer()

@dp.callback_query_handler(text=["cycle","camphor","gandha","mangaldeep"])
async def quantityfunction(call: types.CallbackQuery):
        ###### milk products ######
        if(call.data=="cycle"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Cycle Agarbatti"
            user_data['items']['cart'][cnt]['price/item']=10
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="camphor"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Bhimsen Camphor 100gm"
            user_data['items']['cart'][cnt]['price/item']=270
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="gandha"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Ashthagandha"
            user_data['items']['cart'][cnt]['price/item']=50
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="mangaldeep"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Mangaldeep Agarbatti"
            user_data['items']['cart'][cnt]['price/item']=50
            await storage.set_data(user=user_id, data=user_data)
             

             
        quantitykeyboard = InlineKeyboardMarkup()
        button16 = InlineKeyboardButton(text="1 ", callback_data="q1")
        button17 = InlineKeyboardButton(text="2", callback_data="q2")
        button18 = InlineKeyboardButton(text="3", callback_data="q3")
        button19 = InlineKeyboardButton(text="4", callback_data="q4")        
        quantitykeyboard.add(button16,button17,button18,button19)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the quantity :", reply_markup=quantitykeyboard)
        await call.answer()

@dp.callback_query_handler(text=["chocklates"])
async def categoryfunction(call: types.CallbackQuery):
    if call.data == "chocklates":
        user_id = call.from_user.id
        user_data = await storage.get_data(user=user_id)
        print("user_data = "+ str(user_data))
        print(user_id)
        print(type(user_data))
        cnt=user_data["items"]["count"]
        user_data['items']['cart'].append({'category':"Chocklates and Cold Drinks"})
        if(user_data==None):
            user_data={}
        await storage.set_data(user=user_id, data=user_data)        
        coldkeyboard = InlineKeyboardMarkup()
        silkbutton = InlineKeyboardButton(text="Dairy Milk Silk 90rs", callback_data="silk")
        cokebutton = InlineKeyboardButton(text="Coca Coal 200ml 40rs", callback_data="coke")
        spritebutton = InlineKeyboardButton(text="Sprite 200ml 20rs", callback_data="sprite")
        starbutton = InlineKeyboardButton(text="5 Star nuts 50rs", callback_data="star")         
        coldkeyboard.add(silkbutton,cokebutton,spritebutton,starbutton)
        await bot.send_message(chat_id=call.message.chat.id, text="Please select the item :", reply_markup=coldkeyboard)
    await call.answer()

@dp.callback_query_handler(text=["silk","coke","sprite","star"])
async def quantityfunction(call: types.CallbackQuery):
        ###### milk products ######
        if(call.data=="silk"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Dairy Milk Silk"
            user_data['items']['cart'][cnt]['price/item']=90
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="coke"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Coca Cola 200ml"
            user_data['items']['cart'][cnt]['price/item']=40
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="sprite"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="Sprite 200ml"
            user_data['items']['cart'][cnt]['price/item']=20
            await storage.set_data(user=user_id, data=user_data)
        if(call.data=="star"):
            user_id = call.from_user.id
            user_data = await storage.get_data(user=user_id)
            print("user_data 2 = "+str(user_data))
            print(type(user_data))
            print(type(user_data['items']))
            if(user_data==None):
                user_data={}
            cnt=user_data['items']['count']
            user_data['items']['cart'][cnt]['item']="% star Nuts"
            user_data['items']['cart'][cnt]['price/item']=50
            await storage.set_data(user=user_id, data=user_data)
             

             
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
    if(call.data=="q1"):
        user_id = call.from_user.id
        user_data = await storage.get_data(user=user_id)
        if(user_data==None):
            user_data={}
        cnt=user_data['items']['count']
        price=user_data['items']['cart'][cnt]['price/item']
        user_data['items']['cart'][cnt]['quantity']=1
        user_data['items']['cart'][cnt]['totalprice']=price*1        
        user_data['items']['count']=cnt+1
        await storage.set_data(user=user_id, data=user_data)
        print(await storage.get_data(user=user_id))

        
    elif(call.data=="q2"):
        user_id = call.from_user.id
        user_data = await storage.get_data(user=user_id)
        if(user_data==None):
            user_data={}
        cnt=user_data['items']['count']
        price=user_data['items']['cart'][cnt]['price/item']
        user_data['items']['cart'][cnt]['quantity']=2
        user_data['items']['cart'][cnt]['totalprice']=price*2        
        user_data['items']['count']=cnt+1
        await storage.set_data(user=user_id, data=user_data)
        print(await storage.get_data(user=user_id))
    elif(call.data=="q3"):
        user_id = call.from_user.id
        user_data = await storage.get_data(user=user_id)
        if(user_data==None):
            user_data={}
        cnt=user_data['items']['count']
        price=user_data['items']['cart'][cnt]['price/item']
        user_data['items']['cart'][cnt]['quantity']=3
        user_data['items']['cart'][cnt]['totalprice']=price*3        
        user_data['items']['count']=cnt+1
        await storage.set_data(user=user_id, data=user_data)
        print(await storage.get_data(user=user_id))
    elif(call.data=="q4"):
        user_id = call.from_user.id
        user_data = await storage.get_data(user=user_id)
        if(user_data==None):
            user_data={}
        cnt=user_data['items']['count']
        price=user_data['items']['cart'][cnt]['price/item']
        user_data['items']['cart'][cnt]['quantity']=4
        user_data['items']['cart'][cnt]['totalprice']=price*4        
        user_data['items']['count']=cnt+1
        await storage.set_data(user=user_id, data=user_data)
        print(await storage.get_data(user=user_id))
    await bot.send_message(chat_id=call.message.chat.id, text="Item added to cart", reply_markup=InlineKeyboardMarkup().add(button1,cartButton))
    # await bot.send_message(chat_id=call.message.chat.id, text=f"Cart : \n {await storage.get_data(user=user_id)}")
    await call.answer()

executor.start_polling(dp)