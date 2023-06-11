import requests
import re
import random
import schedule
import time
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

url = "https://us.puma.com/us/en/pd/porsche-design-pwrplate-motorsport-mens-sneakers/307452?swatch=01&referrer-category=mens-shop-all-mens"
user_agent_list = [
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/E7FBAF',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15',
	'Mozilla/5.0 (X11; CrOS x86_64 14092.77.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.107 Safari/537.36',
]

def check_availability():
    headers = {'User-Agent': random.choice(user_agent_list)}
    page_body = requests.get(url, headers=headers).text
    message = "Not in stock"
    check = bool(re.search('<label data-disabled="false" data-size="0180" class="relative border flex items-center justify-center flex-none rounded-sm cursor-pointer">', page_body, re.IGNORECASE))
    if check == True:
        message = "In stock"
    return message


bot_token = ""
channel_id = ""

updater = Updater(bot_token, use_context=True)

def start(update: Update, context: CallbackContext):
	update.message.reply_text("Ready for new shoes?")

def help(update: Update, context: CallbackContext):
	update.message.reply_text(check_availability())
 
def unknown_text(update: Update, context: CallbackContext):
	update.message.reply_text("Sorry, '%s' is not a valid command for me" % update.message.text)
 
updater.dispatcher.add_handler(CommandHandler('hello', start))
updater.dispatcher.add_handler(CommandHandler('help', help))

updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()

def send():
    if check_availability() == "In stock":
        message = "Time to buy new shoes!!!\nhttps://us.puma.com/us/en/pd/porsche-design-pwrplate-motorsport-mens-sneakers/307452?swatch=01&referrer-category=mens-shop-all-mens"
	send_message = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={channel_id}&text={message}"
	requests.get(send_message)
  
  
schedule.every(24).hours.do(send)

while True:
    schedule.run_pending()
    time.sleep(1)
    


