#chatbot.py
import os #Lab5.7.1
import json
import telegram
from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext)
# import configparser #Lab5.7.2 and Lab8P2
#import configparser Lab8P2Step1
import logging
import redis
import requests


from ChatGPT_HKBU import HKBU_ChatGPT
def equiped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

#global redis1
def main():
    #Load your token and create an Updater for your Bot
    #lab8P2 as below
    #config = configparser.ConfigParser() Lab8P2Step1
    # config.read('config.ini') Lab8P2Step1
    #Lab8.P2 as below:
    updater = Updater(token=(os.environ['ACCESS_TOKEN_TG']), use_context=True)
    # updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    # updater = Updater(token=('6565812077:AAEl-75tFOKjtPYhglY_xXCx7dswWEvsTxo'), use_context=True) #Lab5.7.
    dispatcher = updater.dispatcher
    
    global redis1
    # redis1 = redis.Redis(host=(config['REDIS']['HOST']),password=(config['REDIS']['PASSWORD']),port=(config['REDIS']['REDISPORT']))
    #lab8P2 as below
    redis1 = redis.Redis(os.environ['HOST_REDIS'], password=(os.environ['PASSWORD_REDIS']), port=(os.environ['PORT_REDIS']))  

    #you can set this logging module, so you will know when
    #and why things do not as expected Meanwhile, update your config.ini as:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    #register a dispatcher to handle message: here we register an echo dispatchr
    #echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    #dispatcher.add_handler(echo_handler)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)
    # dispatcher for chatgpt
    global chatgpt
    chatgpt = HKBU_ChatGPT('./config.ini')
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command),
                    equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)
    
    #on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add",add))
    dispatcher.add_handler(CommandHandler("help", help_command))

    #To start the bot:
    updater.start_polling()
    updater.idle()
    

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)
    #Define a few command handlers. These usually take the two arguments update and
    #context. Error handlers also receive the raised TelegramError object in error.

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')
def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        redis1.incr(msg)

        update.message.reply_text('You have said ' + msg +  ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')
        
# See following code in 'ChatGPT_HKBU.py'
#----------------------------------------
# def submit(self, message):
#     conversation = [{"role": "user", "content": message}]
#     # url = (os.environ['BASICURL']) + "/deployments/" + (os.environ['MODELNAME']) + "/chat/completion/?api-version=" + (os.environ{APIVERSION})
#     headers = {'Content-Type': 'application/json','api-key': (os.environ['ACCESS_TOKEN_CHATGPT'])}
#     url = 
#     payload = {'messages': conversation }
#     response = requests.post(url,json=payload, headers=headers)
#     if response.status_code == 200;
#         data = response.json()
#         return data['choices'][0]['message']['content']
#     else:
#         return 'Error:', response
#----------------------------------------    
    
if __name__ == '__main__':
    main()
    #print('test')Print terminal log

