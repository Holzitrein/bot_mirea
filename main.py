import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
import datetime
import requests
from vk_api.utils import get_random_id
from parser_kor import *
from parser_pogoda import *
from parser_ras import *
vk_session = vk_api.VkApi(token='ebf43a5ef04e9f368475b0f9d1cc300958a834e7157f1e4d7f029b4d8c5015aee971ef203f440eae95350')
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
class User():
    def __init__(self, id, mode, state):
        self.id = id
        self.mode = mode
        self.state = state
users = []

def set_button(text, color):
    return {
        "action": {
            "type": "text",
            "label": f"{text}"
        },
        "color": f"{color}"
    }
start = {
    "one_time" : False,
    "buttons" : [
        [set_button('Начать', 'positive')]
    ]
}
start = json.dumps(start, ensure_ascii = False).encode('utf-8')
start = str(start.decode('utf-8'))

weather_but = {
    "one_time" : False,
    "buttons" : [
        [set_button('сейчас', 'positive'), set_button('на сегодня', 'negative')],
        [set_button('на завтра', 'positive'), set_button('на 5 дней', 'negative')]
    ]
}
weather_but = json.dumps(weather_but, ensure_ascii = False).encode('utf-8')
weather_but = str(weather_but.decode('utf-8'))

raspisanie_but = {
    "one_time" : False,
    "buttons" : [
        [set_button('сегодня', 'positive'), set_button('завтра', 'negative')],
        [set_button('на эту неделю', 'positive'), set_button('на следующую неделю', 'negative')],
        [set_button('какая неделя?', 'primary'), set_button('какая группа?', 'primary')]
    ]
}
raspisanie_but = json.dumps(raspisanie_but, ensure_ascii = False).encode('utf-8')
raspisanie_but = str(raspisanie_but.decode('utf-8'))

prepod_but = {
    "one_time" : False,
    "buttons" : [
        [set_button('сегодня', 'positive'), set_button('завтра', 'negative')],
        [set_button('на эту неделю', 'positive'), set_button('на следующую неделю', 'negative')],
    ]
}
prepod_but = json.dumps(prepod_but, ensure_ascii = False).encode('utf-8')
prepod_but = str(prepod_but.decode('utf-8'))

menu = {
    "one_time" : False,
    "buttons" : [
        [set_button('расписание', 'positive'), set_button('погода', 'negative'), set_button('Коронавирус', 'primary')]
    ]
}
menu = json.dumps(menu, ensure_ascii = False).encode('utf-8')
menu = str(menu.decode('utf-8'))

prepod_menu = {
    "one_time" : False,
    "buttons" : [
        [set_button('на сегодня', 'positive'), set_button('на завтра', 'negative')],
        [set_button('на эту неделю', 'positive'), set_button('на следующую неделю', 'negative')]
    ]
}
prepod_menu = json.dumps(prepod_menu, ensure_ascii = False).encode('utf-8')
prepod_menu = str(prepod_menu.decode('utf-8'))
def send_vk(id, text, key):
    vk_session.method('messages.send', {'user_id' : id ,'message' : text, 'random_id' : 0, 'keyboard' : key})


def send_vk_img(id, attachments,text, key):
    attachment = ','.join(attachments)
    vk_session.method('messages.send', {'user_id' : id, 'attachment' :  attachment, 'message' : text, 'random_id' : 0, 'keyboard' : key})


def main():
    
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.text:
            print('New from {}, text = {}'.format(event.user_id, event.text))
            print(users)
            id = event.user_id
            msg = event.text.lower() 
            if msg == 'старт':
                flag1 = 0
                for user in users:
                        if user.id == id:
                            send_vk(id, "Привет, я бот от Андрейчука\n "
                                 "Введи пожалуйста номер группы, а иначе ты ничего не получишь\n "
                                 , menu)
                            user.mode = 'start'
                            user.state = "menu"
                            flag1 = 1
                if flag1 == 0:
                    users.append(User(id, 'start', 'menu'))
                    send_vk(id, "Привет, я бот от Андрейчука\n "
                                "Введи пожалуйста номер группы, а иначе ты ничего не получишь\n "
                                 "Команды бота:\n "
                                "Старт - для запуска бота\n"
                                "Меню - переход в меню\n"
                                "Погода - переход в раздел погоды\n"
                                "Коронавирус - переход в раздел коронавируса\n"
                                "Найти 'Фамилия' - поиск расписания преподователя\n"
                                "Расписание - переход в раздел расписания\n", menu)
            for user in users:
                if user.id == id:
                    if msg.lower() == 'меню':
                        user.state = "menu"
                        send_vk(id, "переход в меню", menu)
                    try :
                        if msg[4].lower()== '-' and msg[7].lower() and msg[5].lower().isdigit() and msg[8].lower().isdigit():
                            user.mode = msg.lower()
                            send_vk(id, "Твою группу теперь знает весь гос.деп.: "+user.mode, menu)
                    except IndexError:
                        pass        
                    
                if msg.lower() == "коронавирус":
                    send_vk(id, "Отправтье 'Корона', если хотите увидеть общую статистику\n"
                            "Если же хотите увидеть статистику по региону, отправтье 'регион (название региона)'\n", menu)
                if ((msg.split())[0].lower() == "регион"):
                    send_vk(id, corona(msg.lower()[7:]), menu)
                if msg.lower() == "корона":
                    info_corona = corona(0)
                    upload = VkUpload(vk_session)
                    attachments = []
                    photo = upload.photo_messages(photos = "grafik.png")[0]
                    attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                    send_vk_img(id, attachments, info_corona, menu)
                if msg.lower() == "погода":
                    send_vk(id, "выберите действие", weather_but)
                if msg.lower() == "сейчас":
                    info_weather = pogoda("сейчас")
                    upload = VkUpload(vk_session)
                    attachments = []
                    photo = upload.photo_messages(photos = "image1.png")[0]
                    attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                    send_vk_img(id, attachments, info_weather, menu)
                if msg.lower() == "на сегодня":
                    info_weather = pogoda("на сегодня")
                    upload = VkUpload(vk_session)
                    attachments = []
                    photo = upload.photo_messages(photos = "image2.png")[0]
                    attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                    send_vk_img(id, attachments, info_weather, menu)
                if msg.lower() == "на 5 дней":
                    info_weather = pogoda("на 5 дней")
                    upload = VkUpload(vk_session)
                    attachments = []
                    photo = upload.photo_messages(photos = "image4.png")[0]
                    attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                    send_vk_img(id, attachments, info_weather, menu)
                if msg.lower() == "на завтра":
                    info_weather = pogoda("на завтра")
                    upload = VkUpload(vk_session)
                    attachments = []
                    photo = upload.photo_messages(photos = "image3.png")[0]
                    attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                    send_vk_img(id, attachments, info_weather, menu)

                if msg.lower()=="расписание":
                    send_vk(id, "выберите действие", raspisanie_but)
                    user.state = "raspisanie"
                if(user.state == "raspisanie"):
                    if msg.lower()=="какая неделя?":
                        send_vk(id, num_week(), menu)
                        user.state = ""
                    if msg.lower()=="какая группа?":
                        send_vk(id, user.mode, menu)
                        user.state = ""
                    if msg.lower()=="сегодня":
                        send_vk(id, pars_stud(user.mode, msg.lower(), 0), menu)
                        user.state = ""
                    if msg.lower()=="завтра":
                        send_vk(id, pars_stud(user.mode, msg.lower(), 0), menu)
                        user.state = ""
                    if msg.lower()=="на эту неделю":
                        send_vk(id, pars_stud(user.mode, msg.lower(), 0), menu)
                        user.state = ""
                    if msg.lower()=="на следующую неделю":
                        send_vk(id, pars_stud(user.mode, msg.lower(), 0), menu)
                        user.state = ""
                if ((msg.split())[0].lower() == "найти"):
                    user.state = "prepod"
                    send_vk(id, "выберите действие", prepod_but)
                    prep = msg.lower()
                if(user.state == "prepod"):
                    if msg.lower()=="на сегодня":
                        send_vk(id, pars_prepod(user.mode, prep, "на сегодня"), menu)
                        user.state = ""
                    if msg.lower()=="на завтра":
                        send_vk(id, pars_prepod(user.mode, prep, "на завтра"), menu)
                        user.state = ""
                    if msg.lower()=="на эту неделю":
                        send_vk(id, pars_prepod(user.mode, prep, "на эту неделю"), menu)
                        user.state = ""
                    if msg.lower()=="на следующую неделю":
                        send_vk(id, pars_prepod(user.mode, prep, "на следующую неделю"), menu)
                        user.state = ""
                    
if __name__ == '__main__':
    main()
