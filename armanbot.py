import telebot
from telebot import types

TOKEN = "8627530411:AAGr9VgTLOE5H8p8tuibxh76v61DpsnbL8Y"

bot = telebot.TeleBot(TOKEN)

user_data = {}

wallets = {
    "BTC": "bc1qexampletestwallet123456789",
    "ETH": "0x1234567890abcdef1234567890abcdef12345678",
    "USDT_TRC20": "TExampleWallet123456789ABCDEFG",
    "USDT_ERC20": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
    "USDT_BEP20": "0x1111111111111111111111111111111111111111"
}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("BTC", "ETH")
    markup.row("USDT")

    bot.send_message(
        message.chat.id,
        "💰 Welcome!\n\nSelect Crypto:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: m.text in ["BTC", "ETH", "USDT"])
def coin_selected(message):

    user_data[message.chat.id] = {}
    user_data[message.chat.id]["coin"] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if message.text == "BTC":
        markup.row("BTC")

    elif message.text == "ETH":
        markup.row("ERC20")

    else:
        markup.row("TRC20", "ERC20")
        markup.row("BEP20")

    bot.send_message(
        message.chat.id,
        "🌐 Select Network:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: True)
def network_selected(message):

    if message.chat.id not in user_data:
        return

    coin = user_data[message.chat.id]["coin"]

    network = message.text

    user_data[message.chat.id]["network"] = network

    if coin == "BTC":
        address = wallets["BTC"]

    elif coin == "ETH":
        address = wallets["ETH"]

    elif coin == "USDT":

        if network == "TRC20":
            address = wallets["USDT_TRC20"]

        elif network == "ERC20":
            address = wallets["USDT_ERC20"]

        else:
            address = wallets["USDT_BEP20"]

    bot.send_message(
        message.chat.id,
        f"""📥 Send Payment To

{address}

After payment click OK."""
    )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("OK")

    bot.send_message(
        message.chat.id,
        "Press OK after payment.",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: m.text == "OK")
def ask_amount(message):

    msg = bot.send_message(
        message.chat.id,
        "💵 Enter Amount:"
    )

    bot.register_next_step_handler(msg, get_amount)


def get_amount(message):

    user_data[message.chat.id]["amount"] = message.text

    msg = bot.send_message(
        message.chat.id,
        "🔗 Enter TX Hash:"
    )

    bot.register_next_step_handler(msg, get_txhash)


def get_txhash(message):

    user_data[message.chat.id]["txhash"] = message.text

    data = user_data[message.chat.id]

    bot.send_message(
        message.chat.id,
        f"""
✅ Payment Request Submitted

🪙 Coin: {data['coin']}
🌐 Network: {data['network']}
💵 Amount: {data['amount']}

🔗 TX Hash:
{data['txhash']}

⏳ Please wait while we review your payment.
"""
    )


print("✅ Bot Running...")

bot.infinity_polling()