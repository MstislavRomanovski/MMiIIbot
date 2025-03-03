import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ( 
    filters, ApplicationBuilder,
    ContextTypes, CommandHandler,
    MessageHandler,Application,
    CallbackQueryHandler,CommandHandler,
    ContextTypes,ConversationHandler,)
from utils import get_answer
from file_utils import *

# cant return to main menu from menu
# need to replace numbers with question groups
# and subgroups to answers with end..


logger = logging.getLogger(__name__)
START_ROUTES, END_ROUTES = range(2)
MAIN_MENU, MENU, INFO, A1, A2, A3, A4, A5, GETFLBTN = range(9)

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [
            InlineKeyboardButton("Вопросы", callback_data=str(MENU)),
            InlineKeyboardButton("Команды", callback_data=str(INFO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:  
        await update.message.reply_text("Выберите:", reply_markup=reply_markup)
    elif update.callback_query:  
        query = update.callback_query
        await query.answer()
        await query.edit_message_text("Выберите:", reply_markup=reply_markup)
    return START_ROUTES

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await delete_bot_messages(context, update.effective_chat.id)
    keyboard = [
        [
            InlineKeyboardButton("О кафедре", callback_data=str(A1)),
            InlineKeyboardButton("Программы обучения", callback_data=str(A2)),]
        ,[
            InlineKeyboardButton("Дисциплины", callback_data=str(A3)),
            InlineKeyboardButton("Контакты", callback_data=str(A4)),]
        ,[
            InlineKeyboardButton("ВКР", callback_data=str(A5))
        ,]
        ,[
            InlineKeyboardButton("Вернуться", callback_data=str(MAIN_MENU))
        ,]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Выберите интересующий вас вопрос:", reply_markup=reply_markup
    )
    return START_ROUTES

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    answer = (f'В данной версии бота доступны следующие команды:\n'
              f'/help - справка о командах\n'
              f'/q - задать вопрос в текстовом виде\n'
              f'/menu - меню с вопросами\n')
    keyboard = [[InlineKeyboardButton("Вернуться", callback_data=str(MAIN_MENU)),],]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=answer,reply_markup=reply_markup)
    return START_ROUTES


async def a1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    answer = get_answer(1)
    keyboard = [

            InlineKeyboardButton("Вернуться", callback_data=str(MENU)), ],

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=answer, reply_markup=reply_markup
    )
    return START_ROUTES


async def a2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    answer =  get_answer(2)
    keyboard = [

        InlineKeyboardButton("Вернуться", callback_data=str(MENU)), ], 

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=answer, reply_markup=reply_markup
    )
    return START_ROUTES


async def a3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    answer =  get_answer(3)
    keyboard = [

        InlineKeyboardButton("Вернуться", callback_data=str(MENU)), ],  

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=answer, reply_markup=reply_markup
    )
    return START_ROUTES


async def a4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    answer = get_answer(4)
    keyboard = [

        InlineKeyboardButton("Вернуться", callback_data=str(MENU)), ],  

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=answer, reply_markup=reply_markup
    )
    return START_ROUTES

async def a5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    answer =  get_answer(5)
    keyboard = [

        [InlineKeyboardButton("Вернуться", callback_data=str(MENU)), 
        InlineKeyboardButton("Получить файлы", callback_data=str(GETFLBTN)),],]  # menu

    # return query.edit_message_text(text=answer)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=answer, reply_markup=reply_markup
    )
    return START_ROUTES
    
async def getflbtn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    answer =  get_answer(5)
    keyboard = [[
        InlineKeyboardButton("Вернуться", callback_data=str(MENU)),],]
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    sent_messages = await send_all(update, context)
    context.user_data.setdefault("bot_messages", []).extend(sent_messages)
    await query.edit_message_text(
        text=answer, reply_markup=reply_markup
    )
    return START_ROUTES

