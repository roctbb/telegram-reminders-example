import json
import telebot
import time
from config import token

bot = telebot.TeleBot(token)


def save(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)


def load():
    global users
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except:
        return {}


users = load()


@bot.message_handler(commands=['start', 'help'])
def on_start_message(message):
    bot.reply_to(message, 'Please use the following commands:\n'
                          '/enable <interval> - to enable notifications\n'
                          '/disable - to disable notifications')


@bot.message_handler(commands=['enable'])
def on_enable_command(message):
    interval = int(message.text.split(' ')[1])  # parse the interval from the message
    user_id = str(message.from_user.id)
    chat_id = message.chat.id

    users[user_id] = {'notifications': True, 'interval': interval, 'chat_id': chat_id,
                      'last_notification': int(time.time())}
    bot.reply_to(message, f'Notifications enabled with interval of {interval} seconds.')

    save(users)


@bot.message_handler(commands=['disable'])
def on_disable_command(message):
    user_id = str(message.from_user.id)

    users[user_id]['notifications'] = False
    bot.reply_to(message, 'Notifications disabled.')

    save(users)


@bot.message_handler(func=lambda message: True)
def on_message(message):
    bot.reply_to(message, 'Use /enable <interval> or /disable commands')


if __name__ == '__main__':
    bot.polling()
