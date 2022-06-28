import logging
from telegram.ext import Updater, CommandHandler
import os 
import telegram
import random
import requests
import pandas as pd
import requests
import sys



#Configure Logging
logging.basicConfig(
    level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

#Solicitar TOKEN 
TOKEN = "5363622455:AAEoFyCSHrhOZhQzxSGD6MxOWKw9h9aoQqY"


def random_number(update,context):
    user_id = update.effective_user['id']
    chat_id = update.effective_chat['id']
    title = update.effective_chat['title']
    name = update.effective_user['first_name']
    logger.info(f"El usuario {name}, ha solicitado un numero aleatorio en el chat {title} (id = {chat_id} )")
    number = random.randint(0,10)
    context.bot.sendMessage(chat_id = chat_id,parse_mode="HTML", text=f"<b>Número</b> aleatorio:\n{number}")



def get_info(update, context):
    user_id = update.effective_user['id']
    chat_id = update.effective_chat['id']
    name = update.effective_user['first_name']
    print(type(chat_id))
    title = update.effective_chat['title']  
    cookie = COOKIE
    #message = f"Hello {name} this is your currently status."
    headers_r = {
            'authority': 'trader.osl.ltd',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://trader.osl.ltd/dashboard',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': cookie
        }
    transactions = requests.get('https://trader.osl.ltd/api/dashboard/accounts?uuid=dd6f15ef-ee94-4a8c-9d7c-ac8a71eed443&accountGroupUuid=dd6f15ef-ee94-4a8c-9d7c-ac8a71eed443', headers=headers_r)
    data = pd.DataFrame.from_dict(transactions.json())

    for i in range(len(data)):
            if(data['accounts'][i]['ccy']=="BTC"):
                BTC_balance = data['accounts'][i]['balance']

            if(data['accounts'][i]['ccy']=="ETH"):
                ETH_balance = data['accounts'][i]['balance']

            if(data['accounts'][i]['ccy']=="USD"):
                USD_balance = data['accounts'][i]['balance']

            if(data['accounts'][i]['ccy']=="USDC"):
                USDC_balance = data['accounts'][i]['balance']

    message = f'''Hello Keyboard this is your status:
        \n<b>BTC:</b> {BTC_balance}\n<b>ETH:</b> {ETH_balance}\n<b>USD:</b> {USD_balance}\n<b>USDC:</b> {USDC_balance}'''
    
    context.bot.sendMessage(chat_id = chat_id, parse_mode="HTML", text=message)
    logger.info(f"El usuario {name}, ha solicitado su Info en el chat {title} (id = {chat_id} )")



if __name__=="__main__":
    #Obtenemos la informacion del Bot
   COOKIE = str(input("COOKIE: "))
   my_bot = telegram.Bot(token=TOKEN)
    
    #print(my_bot.getMe())

#Enlazamos nuestro updater con nuestro bot 
updater = Updater(my_bot.token,use_context=True)

#Creamos un despachador
dp = updater.dispatcher

#Creamos los manejadores
dp.add_handler(CommandHandler("random",random_number))
dp.add_handler(CommandHandler("getinfo",get_info))


 #Pregunta al bot si hay nuevos msjs
updater.start_polling()
print("BOT CARGADO")
updater.idle() #finalizar el bot ctrl+c

