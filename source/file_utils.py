from telegram.ext import (
    filters, ApplicationBuilder,
    ContextTypes, CommandHandler,
    MessageHandler,Application,
    CallbackQueryHandler,CommandHandler,
    ContextTypes,ConversationHandler,)

from telegram import Update
import os
from inspect import getsourcefile

async def send_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dir_path = os.getcwd()+"\documents"
    files = os.listdir(dir_path)
    sent_message_ids = []
    for file in files:
       sent_message = await context.bot.send_document(update.effective_chat.id,dir_path + "/" + file)
       sent_message_ids.append(sent_message.message_id)
    
    return sent_message_ids

async def delete_bot_messages(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    """Delete bot messages tracked in user_data."""
    message_ids = context.user_data.get("bot_messages", [])
    for message_id in message_ids:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception as e:
            logger.warning(f"Failed to delete message {message_id}: {e}")
    context.user_data["bot_messages"] = []
    
    
