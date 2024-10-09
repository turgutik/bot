import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from db import UsersInfo as user
from db import rows
import time
import random
from datetime import datetime





token = 'vk1.a.vOkKl-xdorSD9w0q5S3exOy0-GU7afr8bk-BnJmIdEoUcVLtQHpMuKQ_eI09lfx9BKQ1D7WXhLFQZTx2Hk7ds-yDchcCm6HRxEJeUL4Ngrb3h0VuLtSD5ebN-pE5SGgq4C2E_rRli8CQ-sSisuS-K1-ztFYzIP-YoaxL5T5psmH_TvkM0jZjemWzrWe3ogLBKDmpmOThvw_BxjozxtzpTA'
auth = vk_api.VkApi(token=token)
longpool = VkLongPoll(auth)
api = auth.get_api()
upload = VkUpload(auth)

main_keyboard = VkKeyboard(False)
main_keyboard.add_button('Клик ⛏', color=VkKeyboardColor.POSITIVE)
main_keyboard.add_line()
main_keyboard.add_button('Профиль 📱', color=VkKeyboardColor.PRIMARY)
main_keyboard.add_button('Вывод 💰', color=VkKeyboardColor.NEGATIVE)
main_keyboard.add_line()
main_keyboard.add_button('Кейсы 📦')

keys_keyboard = VkKeyboard(False)
keys_keyboard.add_button('Кейс 50', color=VkKeyboardColor.POSITIVE)
keys_keyboard.add_button('Кейс 500', color=VkKeyboardColor.POSITIVE)
keys_keyboard.add_button('Кейс 1000', color=VkKeyboardColor.POSITIVE)
keys_keyboard.add_line()
keys_keyboard.add_button('Меню', color=VkKeyboardColor.NEGATIVE)

def write_messages(sender, message, keyboard):
    auth.method('messages.send', {'user_id': sender, 'message': message, 'random_id': get_random_id(), 'keyboard': keyboard.get_keyboard()})

def send_photo(sender):
    photo = upload.photo_messages(photos='4493555-12.jpg')[0]
    auth.method('messages.send', {'user_id': sender, 'random_id': get_random_id(), 'attachment': 'photo{}_{}'.format(photo['owner_id'], photo['id'])})

def get_day():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y%m%d")
    return str(formatted_date)

def main():
    try:
        for event in longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.text and event.to_me:
                mess = event.text
                sender = event.user_id
                if user.is_reg(sender) == False:
                    if mess == 'Начать':
                        user_vk = auth.method("users.get", {"user_ids": sender})
                        name = user_vk[0]['first_name']
                        surname = user_vk[0]['last_name']
                        user.insert(sender, name, surname)
                        write_messages(sender, 'Вы были успешно зарегистрированы в боте', main_keyboard)
                else:
                    if mess == 'Клик ⛏':
                        user.update(sender, user.get_clicks(sender)+1)
                        write_messages(sender, '+1 Коин 💎', main_keyboard)
                    elif mess == 'Баланс' or mess == 'бал' or mess == 'баланс':
                        write_messages(sender, f'Ваш баланс : {user.get_clicks(sender)} 💎\nGolds : {user.get_gold(sender)} 🧈', main_keyboard)
                    elif mess == 'Профиль 📱':
                        value = user.get_info(sender)
                        write_messages(sender, f'Информация об аккаунте 📊:\n\nДанные пользователя: {value[0]} {value[1]}\n\n======================\nБаланс коинов 💎: {user.get_clicks(sender)}\nБаланс GOLD 🧈: {user.get_gold(sender)}\nPrime Status : {user.check_prime(sender)}\n======================\n', main_keyboard)
                    elif mess == 'Кейсы 📦':
                        write_messages(sender, f'Доступные кейсы: ', keys_keyboard)
                    elif "Кейс" in mess:
                        box = mess.replace('Кейс', '')
                        if "500" in box:
                            if user.get_clicks(sender) >= 500:
                                user.update(sender, user.get_clicks(sender)-500)
                                gold = random.randint(1, 1000)
                                if gold == 5 or gold == 500 or gold == 666 or gold == 777:
                                    gold_win = random.uniform(0.1, 15.0)
                                    user.update_gold(sender, user.get_gold(sender)+gold_win)
                                    write_messages(sender, f'Поздравляем!\n\nВы выиграли = {gold_win}', keys_keyboard)
                                else:

                                    write_messages(sender, f'К сожалению кейс оказался пустой (', keys_keyboard)
                            else:
                                write_messages(sender, f'На вашем счету недостаточно коинов для открытия кейса!', keys_keyboard)
                        elif "50" in box:
                            if user.get_clicks(sender) >= 50:
                                user.update(sender, user.get_clicks(sender)-50)
                                gold = random.randint(1, 1000)
                                if gold > 10 and gold < 100:
                                    gold_win = round(random.uniform(0.1, 3.0), 2)
                                    user.update_gold(sender, user.get_gold(sender)+gold_win)
                                    write_messages(sender, f'Поздравляем!\n\nВы выиграли = {gold_win}', keys_keyboard)
                                else:
                                    write_messages(sender, f'К сожалению кейс оказался пустой (', keys_keyboard)
                            else:
                                write_messages(sender, f'На вашем счету недостаточно коинов для открытия кейса!', keys_keyboard)


                        elif "1000" in box:
                            if user.get_clicks(sender) >= 1000:
                                user.update(sender, user.get_clicks(sender)-1000)
                                gold = random.randint(1, 1000)
                                if gold == 5 or gold == 500 or gold == 666 or gold == 777:
                                    gold_win = random.uniform(0.1, 30.0)
                                    user.update_gold(sender, user.get_gold(sender)+gold_win)
                                    write_messages(sender, f'Поздравляем!\n\nВы выиграли = {gold_win}', keys_keyboard)
                                else:
                                    write_messages(sender, f'К сожалению кейс оказался пустой (', keys_keyboard)
                            else:
                                write_messages(sender, f'На вашем счету недостаточно коинов для открытия кейса!', keys_keyboard)

                        else:
                            write_messages(sender, f'Нет такого кейса', main_keyboard)


                    elif mess == 'Бонус':
                        if user.check_get_bonus(sender, get_day()) is False:
                            write_messages(sender, f'Вы уже получали ежедневный бонус!', main_keyboard)
                        else:
                            if user.check_prime(sender) == 'Отсутствует':
                                user.update(sender, user.get_clicks(sender)+500)
                                write_messages(sender, f'Вы получили ежедневный бонус - 500 коинов.', main_keyboard)
                            else:
                                user.update(sender, user.get_clicks(sender)+1500)
                                write_messages(sender, f'Вы получили ежедневный бонус - 1500 коинов.\n(Prime Статус - выгода)', main_keyboard)

                    elif mess == 'Топ':
                        if rows() <= 15:
                            mes_text = "Топ игроков по кликам 👥\n\n"
                            top = user.get_top(rows())
                            data = api.users.get(user_ids=", ".join([str(i[0]) for i in top]))
                            for i, value in enumerate(top):
                                name = data[i]["first_name"]
                                family = data[i]["last_name"]
                                mes_text += f"{i+1}) {name} {family} = {value[1]} 💎\n"

                            mes_text += "\nКликайте больше и возвышайтесь в топы 📣"
                            write_messages(sender, f'{mes_text}', main_keyboard)
                        else:
                            mes_text = "Топ-15 игроков по кликам 👥\n\n"
                            top = user.get_top(15)
                            data = api.users.get(user_ids=", ".join([str(i[0]) for i in top]))
                            for i, value in enumerate(top):
                                name = data[i]["first_name"]
                                family = data[i]["last_name"]
                                mes_text += f"- {name} {family} = {value[1]} 💎\n"

                    elif mess == 'Меню':
                        write_messages(sender, 'Вы попали на главное меню: ', main_keyboard)
                    elif mess == "Вывод 💰":
                        if user.get_gold(sender) >= 50:
                            user.update_gold(sender, user.get_gold(sender)-user.get_gold(sender))
                            write_messages(sender, 'Заявка на вывод голды успешно создана!\nОжидайте сообщения администратора!', main_keyboard)

                            write_messages(669446779, f'Завка на вывод от {sender}', main_keyboard)
                        else:
                            write_messages(sender, 'Минимальная сумма для вывода: 50 🧈', main_keyboard)
                    else:
                        write_messages(sender, 'Неизвестная команда:', main_keyboard)
                        


    except TimeoutError:
        print("--------------- [ СЕТЕВАЯ ОШИБКА ] ---------------")
        print("Переподключение к серверам...")
        time.sleep(3)

main()