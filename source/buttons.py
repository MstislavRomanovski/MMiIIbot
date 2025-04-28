import logging
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ( 
    filters, ApplicationBuilder,
    ContextTypes, CommandHandler,
    MessageHandler,Application,
    CallbackQueryHandler,ConversationHandler,)
from utils import get_answer
from file_utils import *

load_dotenv()
DIR = os.getenv("DIR")

logger = logging.getLogger(__name__)
START_ROUTES = range(1)
MAIN_MENU, DATES, CONTACTS , INFO, GIA_MENU, VKR_MENU ,V1, V2, V3, V4, V5, V6, V7, G1, G2, G3, G4, V5FL, V6FL = range(19)

class BasicButton:
    def __init__(self, keyboard, answer, ismenu = False, senddir=None):
        self.keyboard = keyboard
        self.answer = answer
        self.ismenu = ismenu
        self.senddir = senddir
        
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        reply_markup = InlineKeyboardMarkup(self.keyboard)

        if  query: 
            await query.answer()
            if self.ismenu:
                await delete_bot_messages(context, update.effective_chat.id)

            if self.senddir:
                sent_messages = await send_all(update, context, self.senddir)
                context.user_data.setdefault("bot_messages", []).extend(sent_messages)

            await query.edit_message_text(text=self.answer, reply_markup=reply_markup)
        elif update.message: 
            await update.message.reply_text(text=self.answer, reply_markup=reply_markup)

        return START_ROUTES

main_menu = BasicButton(
    keyboard=[
        [InlineKeyboardButton("ВКР", callback_data=str(VKR_MENU)),
         InlineKeyboardButton("ГИА", callback_data=str(GIA_MENU)),],
        [InlineKeyboardButton("Даты", callback_data=str(DATES)),
         InlineKeyboardButton("Контакты", callback_data=str(CONTACTS)),],
        [InlineKeyboardButton("Команды", callback_data=str(INFO)),]
    ],
    answer="Выберите:",
    ismenu=True
)

vkr_menu = BasicButton(
    keyboard=[
        [InlineKeyboardButton("О ВКР", callback_data=str(V1)),
         InlineKeyboardButton("Общие Требования", callback_data=str(V2))],
        [InlineKeyboardButton("Согласование ВКР", callback_data=str(V3)),
         InlineKeyboardButton("Проверка на плагиат", callback_data=str(V4))],
        [InlineKeyboardButton("Оформление ВКР", callback_data=str(V5)),
         InlineKeyboardButton("Документы", callback_data=str(V6))],
        [InlineKeyboardButton("Апробация ВКР", callback_data=str(V7)),],
        [InlineKeyboardButton("Вернуться", callback_data=str(MAIN_MENU))]
    ],
    answer="Это раздел посвященный ВКР, выберите интересующий вас вопрос:",
    ismenu=True
)

gia_menu = BasicButton(
    keyboard=[
        [InlineKeyboardButton("Допуск к ГИА", callback_data=str(G1)),],
        [InlineKeyboardButton("Тестирование ГОС", callback_data=str(G2)),],
        [InlineKeyboardButton("Формат ГОС", callback_data=str(G3)),],
        [InlineKeyboardButton("Вернуться", callback_data=str(MAIN_MENU))]
    ],
    answer="Это раздел посвященный ГИА и ГОС, выберите интересующий вас вопрос:",
    ismenu=True
)

info = BasicButton(
    keyboard=[[InlineKeyboardButton("Вернуться", callback_data=str(MAIN_MENU))]],
    answer="В данной версии бота доступны следующие команды:\n"
           "/help - справка о командах\n"
           "/q - задать вопрос в текстовом виде\n"
           "/menu - меню с вопросами"
)

dates = BasicButton(
        keyboard=[[InlineKeyboardButton("Вернуться", callback_data=str(MAIN_MENU))]],
        answer=get_answer(12)
)

contacts = BasicButton(
        keyboard=[[InlineKeyboardButton("Вернуться", callback_data=str(MAIN_MENU))]],
        answer=get_answer(8)
)

# Вопросы ВКР
vkr_buttons = {
    V1: BasicButton(
        keyboard=[[InlineKeyboardButton("Вернуться", callback_data=str(VKR_MENU))]],
        answer=get_answer(7)
    ),
    V2: BasicButton(
        keyboard=[[InlineKeyboardButton("Вернуться", callback_data=str(VKR_MENU))]],
        answer=get_answer(1)
    ),
    V3: BasicButton(
        keyboard=[[InlineKeyboardButton("Вернуться", callback_data=str(VKR_MENU))]],
        answer=get_answer(2)
    ),
    V4: BasicButton(
        keyboard=[[InlineKeyboardButton("Вернуться", callback_data=str(VKR_MENU))]],
        answer=get_answer(3)
    ),
    V5: BasicButton(
        keyboard=[[InlineKeyboardButton("Вернуться", callback_data=str(VKR_MENU)),
                   InlineKeyboardButton("Получить файлы", callback_data=str(V5FL))]],
        answer=get_answer(4)
    ),
    V6: BasicButton(
        keyboard=[[InlineKeyboardButton("Вернуться", callback_data=str(VKR_MENU)),
                   InlineKeyboardButton("Получить файлы", callback_data=str(V6FL))]],
        answer=get_answer(5)
    ),
    V7: BasicButton(
        keyboard=[[InlineKeyboardButton("Вернуться", callback_data=str(VKR_MENU))]],
        answer=get_answer(6)
    )
}

gia_buttons = {
    G1: BasicButton(
        keyboard=[[InlineKeyboardButton("Вернуться", callback_data=str(GIA_MENU))]],
        answer=get_answer(9)  # Получаем ответ по индексу для ГИА
    ),
    G2: BasicButton(
        keyboard=[[InlineKeyboardButton("Вернуться", callback_data=str(GIA_MENU))]],
        answer=get_answer(10)
    ),
    G3: BasicButton(
        keyboard=[[InlineKeyboardButton("Вернуться", callback_data=str(GIA_MENU))]],
        answer=get_answer(11)
    ),
}

v5fl = BasicButton(
    keyboard=[[InlineKeyboardButton("Вернуться", callback_data=str(VKR_MENU))]],
    answer=get_answer(4),
    senddir=DIR+"/documents/4"
)

v6fl = BasicButton(
    keyboard=[[InlineKeyboardButton("Вернуться", callback_data=str(VKR_MENU))]],
    answer=get_answer(5),
    senddir=DIR+"/documents/5"
)

