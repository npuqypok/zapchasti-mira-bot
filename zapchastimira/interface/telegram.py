from enum import StrEnum
from pydantic import BaseModel
import telebot
from telebot.types import Message
from zapchastimira.common.settings import TelegramSettings
from zapchastimira.repositories.part import PartDTO
from zapchastimira.services.search_service import search_by_products

settings = TelegramSettings()

API_TOKEN = settings.token

bot = telebot.TeleBot(API_TOKEN)
class UserStateEnum(StrEnum):
    START = "start"
    SEARCH = "search"

user_states = {}

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    user_id = message.from_user.id
    if user_states.get(user_id) is None:
        user_states[user_id] = UserStateEnum.START
    else:
        user_states[user_id] = UserStateEnum.START
    bot.reply_to(message, """
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!
""")


@bot.message_handler(commands=["search"])
def start_search(message: Message):
    user_id = message.from_user.id
    user_states[user_id] = UserStateEnum.SEARCH
    bot.reply_to(message, """
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!
""")


class OutputSearchDataProduct(BaseModel):
    name: str
    price: float
    stock_quantity: int
    description: str
    url: str

    def __str__(self):
        return f"""
Название товара: {self.name}
цена: {self.price}
количество {self.stock_quantity}
описание: {self.description}
ссылка: {self.url}
"""
    
class OutputSearchDataPart(BaseModel):
    name: str
    brand: str
    part_number: str
    price: float
    stock_quantity: int
    description: str
    url: str
    compatibility: str

    def __str__(self):
        return f"""
Название товара: {self.name}
цена: {self.price}
номер запчасти: {self.part_number}
бренд: {self.brand}
совместимость: {self.compatibility}
количество {self.stock_quantity}
описание: {self.description}
ссылка: {self.url}
"""


@bot.message_handler(func=lambda message: True)
def search(message: Message):
    user_id = message.from_user.id
    if user_states[user_id] != UserStateEnum.SEARCH:
        pass
    result = search_by_products(message.text, user_id)
    result_answer = ""
    for i in result:
        if isinstance(i, PartDTO):
            tmp = OutputSearchDataPart(
                name=i.name,
                brand=i.brand,
                part_number=i.part_number,
                price=i.price,
                stock_quantity=i.stock_quantity,
                description=i.description,
                url=i.page_url,
                compatibility=i.compatibility
            )
        else:
            tmp = OutputSearchDataProduct(
                name=i.name,
                price=i.price,
                stock_quantity=i.stock_quantity,
                description=i.description,
                url=i.url
            )
        result_answer += str(tmp)

    bot.reply_to(message, result_answer)

bot.infinity_polling()
