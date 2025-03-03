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

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)
TOKEN = "8167879602:AAHzHPS_nyUOKq2-PCdbtJI4YmpBW-qT1Qo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    # last_name = update.message.chat.last_name
    # username = update.message.chat.username
    await context.bot.send_message(chat_id=update.effective_chat.id, text= f"Здраствуйте, {first_name}! Я чат-бот кафедры ММиИИ РУДН. Чем могу быть полезен? /menu .")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=(f"В данной версии бота доступны следующие команды:\n"
                                                                          f"/help - справка о командах\n"
                                                                          f"/q - задать вопрос\n/feedback - оставить свои мнения и предложения по улучшению бота\n"
                                                                          f"/menu - менюшка"))

async def question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_arg = " ".join(context.args)
    index = classify_text(user_arg)
    answer = get_answer(index)
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=str(index))
    if index == 5:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
        await send_all(update, context)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    question_handler = CommandHandler('q', question)
    help_handler = CommandHandler('help', help)
    #menu |
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("menu", main_menu)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(menu, pattern="^" + str(MENU) + "$"),
                CallbackQueryHandler(main_menu, pattern="^" + str(MAIN_MENU) + "$"),
                CallbackQueryHandler(info, pattern="^" + str(INFO) + "$"),
                CallbackQueryHandler(a1, pattern="^" + str(A1) + "$"),
                CallbackQueryHandler(a2, pattern="^" + str(A2) + "$"),
                CallbackQueryHandler(a3, pattern="^" + str(A3) + "$"),
                CallbackQueryHandler(a4, pattern="^" + str(A4) + "$"),
                CallbackQueryHandler(a5, pattern="^" + str(A5) + "$"),
                CallbackQueryHandler(getflbtn, pattern="^" + str(GETFLBTN) + "$")
                
            ],
            # END_ROUTES: [
            #     CallbackQueryHandler(main_menu, pattern="^" + str(ONE) + "$"),
            # ],
        },
        fallbacks=[CommandHandler("menu", main_menu)],
    )
    

    application.add_handler(start_handler)
    application.add_handler(question_handler)
    application.add_handler(help_handler)
    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
