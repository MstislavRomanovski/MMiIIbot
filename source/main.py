import os
from dotenv import load_dotenv
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    filters, ApplicationBuilder,
    ContextTypes, CommandHandler,
    MessageHandler,Application,
    CallbackQueryHandler,CommandHandler,
    ContextTypes,ConversationHandler,)
    
from file_utils import *
from utils import *
from buttons import *

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)
TOKEN = os.getenv("TOKEN")

DIR = os.getenv("DIR")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    # last_name = update.message.chat.last_name
    # username = update.message.chat.username
    await context.bot.send_message(chat_id=update.effective_chat.id, text= f"Здраствуйте, {first_name}! Я чат-бот кафедры ММиИИ РУДН. Чем могу быть полезен? /menu .")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=(f"В данной версии бота доступны следующие команды:\n"
                                                                          f"/help - справка о командах\n"
                                                                          f"/menu - меню"))

async def question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #user_arg = " ".join(context.args)
    message = update.message or update.edited_message
    if not message or not message.text:
        return
    user_arg = message.text
    index = classify_text(user_arg)
    answer = get_answer(index)
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=str(index))
    if index in (4,5):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
        await send_all(update, context,DIR+f"/documents/{index[0]}")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    question_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), question)
    help_handler = CommandHandler('help', help)
    #menu |
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("menu", main_menu.handle)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(main_menu.handle, pattern=f"^{MAIN_MENU}$"),
                CallbackQueryHandler(vkr_menu.handle, pattern=f"^{VKR_MENU}$"),
                CallbackQueryHandler(gia_menu.handle, pattern=f"^{GIA_MENU}$"),
                CallbackQueryHandler(info.handle, pattern=f"^{INFO}$"),
                CallbackQueryHandler(dates.handle, pattern=f"^{DATES}$"),
                CallbackQueryHandler(contacts.handle, pattern=f"^{CONTACTS}$"),
                CallbackQueryHandler(v5fl.handle, pattern=f"^{V5FL}$"),
                CallbackQueryHandler(v6fl.handle, pattern=f"^{V6FL}$"),
            ] + [
                CallbackQueryHandler(btn.handle, pattern=f"^{key}$") for key, btn in vkr_buttons.items()
            ] + [
                CallbackQueryHandler(btn.handle, pattern=f"^{key}$") for key, btn in gia_buttons.items()
            ]
        },
        fallbacks=[CommandHandler("menu", main_menu.handle)],
    )

    application.add_handler(start_handler)
    application.add_handler(question_handler)
    application.add_handler(help_handler)
    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
