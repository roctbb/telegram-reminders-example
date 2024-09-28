from bot import bot, load, save
import time

while True:
    users = load()
    print(users)
    current_time = int(time.time())

    for user_id, user in users.items():
        if user['notifications']:
            last_sent = user['last_notification']
            interval = user['interval']
            if current_time - last_sent > interval:
                try:
                    bot.send_message(user_id, "Reminder!")
                    users[user_id]['last_notification'] = int(time.time())
                    print(users)
                except Exception as e:
                    print(e)
    save(users)

    time.sleep(1)
