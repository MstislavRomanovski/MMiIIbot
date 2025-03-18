from telegram.ext import (
    filters, ApplicationBuilder,
    ContextTypes, CommandHandler,
    MessageHandler,Application,
    CallbackQueryHandler,CommandHandler,
    ContextTypes,ConversationHandler,)

from telegram import Update
import os
from inspect import getsourcefile
from dotenv import load_dotenv
import requests
import tqdm


load_dotenv()
DIR = os.getenv("DIR")

def download_weights():
    
    def wfromresponse(filename,link):
        response = requests.get(link, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        with open(filename, "wb") as f,tqdm.tqdm(desc=f"Загрузка {filename}", total=total_size, unit="B", unit_scale=True) as bar:
            for chunk in response.iter_content(4096):
                f.write(chunk)
                bar.update(len(chunk))

    links = ["https://www.dropbox.com/scl/fi/etdxrg7hgewsikgih1pn0/multiclass.pt?rlkey=9dsja3vop2it9382ndh01fixp&st=temnsvb4&dl=0",
    "https://www.dropbox.com/scl/fi/u41kb03z5b2tbdlxhk37k/oneclass.pt?rlkey=yh03d0n11z6hmsiz02nyczjj9&st=nv8rm6m3&dl=0"]
    links = [link.replace("www.dropbox.com", "dl.dropboxusercontent.com").replace("&dl=0","") for link in links]
    
    save_dir = os.path.join(DIR,"pretrained")
    
    os.makedirs(save_dir, exist_ok=True)
    
    multiclass = os.path.join(save_dir,"multiclass.pt")
    oneclass = os.path.join(save_dir,"oneclass.pt")
    
    if os.path.exists(multiclass) and os.path.exists(oneclass):
        return 0
    else:    
        wfromresponse(multiclass,links[0])
        wfromresponse(oneclass,links[1])
        return 1
    
async def send_all(update: Update, context: ContextTypes.DEFAULT_TYPE, dir_path):
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
    
    
