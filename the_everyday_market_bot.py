from typing import Final
from telegram import Update
from telegram import KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# TOKEN: Final = '6261264971:AAGdXEowrZzPfAMVMZIl1CmL4LGA53T9ufg'
TOKEN: Final = '5721307704:AAGFdU2ov3UcO5bItQTIhCE0bI3tgDAXzHI'
BOT_USERNAME: Final = '@TheEveryDayMarket_bot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Welcome to The EveryDay Market! \nFor Categories /inventory')

async def inventory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Here is the list of categories..\n1./milk Milk Products\n2./daily Daily Needs\n3./house House Cleaning\n4./grains Grains\n5./snacks Snack\n6./biscuits Biscuits\n7./food Food\n8./pooja Pooja items\n9./oils Oils and Ghee')

async def milk_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('1.200 ml milk packet\n2.500 ml milk packet\n3.100 gm curd\n4.100 gm panner')

async def daily_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('1.200 ml milk packet\n2.500 ml milk packet\n3.100 gm curd\n4.100 gm panner')

async def house_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('1.200 ml milk packet\n2.500 ml milk packet\n3.100 gm curd\n4.100 gm panner')

async def grains_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('1.200 ml milk packet\n2.500 ml milk packet\n3.100 gm curd\n4.100 gm panner')

async def snack_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('1.200 ml milk packet\n2.500 ml milk packet\n3.100 gm curd\n4.100 gm panner')

async def biscuit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('1.200 ml milk packet\n2.500 ml milk packet\n3.100 gm curd\n4.100 gm panner')

async def food_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('1.200 ml milk packet\n2.500 ml milk packet\n3.100 gm curd\n4.100 gm panner')

async def pooja_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('1.200 ml milk packet\n2.500 ml milk packet\n3.100 gm curd\n4.100 gm panner')

async def oils_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('1.200 ml milk packet\n2.500 ml milk packet\n3.100 gm curd\n4.100 gm panner')

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Its working')


#Responses

def handle_response(text: str)-> str:
    processed: str=text.lower()
    if 'hello' in processed:
        return 'Hey there!'
    return 'Please repeat'

async def handle_message(update: Update,context :ContextTypes.DEFAULT_TYPE):
    message_type: str=update.message.chat.type
    text: str=update.message.text
    

    print(f'User ({update.message.chat_id}) in {message_type}: "{text}"')

    if message_type=='group':
        if BOT_USERNAME in text:
            new_text: str =text.replace(BOT_USERNAME,'').strip()
            response: str - handle_response(new_text)
        else:
            return
    else:
        response: str=handle_response(text)

    print('Bot', response)
    await update.message.reply_text(response)

async def error(update: Update,context :ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__=='__main__':
    app=Application.builder().token(TOKEN).build()
    KeyboardButton("hello world", request_contact=None, request_location=None)
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('inventory',inventory_command))
    app.add_handler(CommandHandler('milk',milk_command))
    app.add_handler(CommandHandler('daily',daily_command))
    app.add_handler(CommandHandler('house',house_command))
    app.add_handler(CommandHandler('grains',grains_command))
    app.add_handler(CommandHandler('snacks',snack_command))
    app.add_handler(CommandHandler('biscuits',biscuit_command))
    app.add_handler(CommandHandler('food',food_command))
    app.add_handler(CommandHandler('pooja',pooja_command))
    app.add_handler(CommandHandler('oils',oils_command))
    app.add_handler(CommandHandler('test',test_command))

    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    app.add_error_handler(error)

    print('polling...')
    app.run_polling(poll_interval=3)

