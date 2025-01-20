import telebot
from telebot.types import Message
from zapchastimira.common.settings import TelegramSettings

settings = TelegramSettings()

API_TOKEN = settings.token

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


@bot.message_handler(commands=["search"])
def start_search(message: Message):
    pass


bot.infinity_polling()
