import requests
from bs4 import BeautifulSoup
import openpyxl
import datetime
import pendulum
import time
import re
now = datetime.datetime.now()

def num_week(): #узнать какая сейчас неделя
    ab = (datetime.date(2021, now.month, now.day).isocalendar()[1])-5
    return ab
def parsing(): #поиск ссылки с расписанием
    mas_href = []
    page = requests.get("https://www.mirea.ru/schedule/")
    soup = BeautifulSoup(page.text, "html.parser")
    result = soup.find("div", {"class":"rasspisanie"}).find(string = "Институт информационных технологий").find_parent("div").find_parent("div")
    href = 0
    for i in result.find_all('a', href=True):
        if(href>0 and href<4):
            mas_href.append(i['href'])
        href+=1
    return mas_href

def pars_prepod(group, vk_msg,when):
    When = datetime.datetime.today().weekday()
    mas_prepod = []
    mas_name_prepod = []
    if(when=="на завтра"):
        When += 1
        print(When)
        if(When == 7):
            When = 0
        parsing_start = (When*12)+4
        parsing_end = (When*12)+16
        print(parsing_start,parsing_end)
        if(((datetime.date(2021, now.month, now.day+1).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "II"
        else:
            parsing_week = "I"
    elif(when=="на сегодня"):
        if(When == 7):
            When = 0
        parsing_start = (When*12)+4
        parsing_end = (When*12)+16
        print(parsing_start,parsing_end)
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "II"
        else:
            parsing_week = "I"
    elif(when=="на эту неделю"):
        parsing_start = 4
        parsing_end = 76
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "II"
        else:
            parsing_week = "I"
    elif(when=="на следующую неделю"):
        parsing_start = 4
        parsing_end = 76
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "I"
        else:
            parsing_week = "II"
    link = parsing()
    vk_group = str(group[len(group) - 2])+str(group[len(group) - 1])
    if(vk_group=="20"):
        link_to_fl = link[0]
        parsing_row = 421
    elif(vk_group=="19"):
        link_to_fl = link[1]
        parsing_row = 342
    elif(vk_group=="18"):
        link_to_fl = link[2]
        parsing_row = 221
    filename = link_to_fl.split('/')[-1]
    r = requests.get(link_to_fl, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    book = openpyxl.open(filename, read_only=True)
    sheet = book.active
    paracount = 1
    mas_info_prepod = []
    vk_msg = vk_msg[6:].lower()
    #print(str(sheet[22][17].value))
    for i in range(7, parsing_row, 5):
        for j in range(parsing_start, parsing_end):
            #print(i ,j)
            time.sleep(1)
            if(paracount==7):
                paracount = 1
            if(str(sheet[j][4].value) == parsing_week):
                if(len(mas_name_prepod)==0):
                    if(str(sheet[j][i].value).lower().find(vk_msg.lower())!=-1):
                        mas_name_prepod.append(str(sheet[j][i].value).lower()[str(sheet[j][i].value).lower().find(vk_msg.lower()):str(sheet[j][i].value).lower().find(vk_msg)+len(vk_msg)+5])
                        mas_info_prepod.append(["","","","","",""])
                        mas_info_prepod[0][paracount-1] += str(sheet[j][i-2].value) +" " + str(sheet[2][i-2].value)+ " " +str(sheet[j][i+1].value) +" \n"
                elif(str(sheet[j][i].value).lower().find(vk_msg.lower())!=-1):
                    if(str(sheet[j][i].value).lower()[str(sheet[j][i].value).lower().find(vk_msg.lower()):str(sheet[j][i].value).lower().find(vk_msg)+len(vk_msg)+5] in mas_name_prepod):
                        for k in range(len(mas_name_prepod)):
                            print(mas_name_prepod[k])
                            if(str(sheet[j][i].value).lower().find(mas_name_prepod[k])!=-1):
                                mas_info_prepod[k][paracount-1] += str(sheet[j][i-2].value) +" " +str(sheet[2][i-2].value)+ " " +str(sheet[j][i+1].value) +" \n"
                    else:
                        mas_name_prepod.append(str(sheet[j][i].value).lower()[str(sheet[j][i].value).lower().find(vk_msg.lower()):str(sheet[j][i].value).lower().find(vk_msg)+len(vk_msg)+5])
                        mas_info_prepod.append(["","","","","",""])
                        mas_info_prepod[len(mas_info_prepod)-1][paracount-1] += str(sheet[j][i-2].value) +" " +str(sheet[2][i-2].value) +" " + str(sheet[j][i+1].value) +" \n"
                paracount += 1
    return mas_name_prepod, mas_info_prepod

def pars_stud(group, mes, mode): #расписание-парсер-экселя
    link_of_site = parsing()
    data_pars = datetime.datetime.now()
    parsing_colum = 0
    parsing_start = 0
    parsing_end = 0
    parsing_week = ""
    colum = 0
    info_respisanie = "" #итоговое сообщение
    day_counter = ""
    para_counter = 1
    num_of_group = group[8:]
    print (num_of_group)

    if(num_of_group=="20"): #определение номера группы
        link_to_download = link_of_site[0]
        parsing_row = 421
    elif(num_of_group=="19"):
        link_to_download = link_of_site[1]
        parsing_row = 342
    elif(num_of_group=="18"):
        link_to_download = link_of_site[2]
        parsing_row = 221

    filename = link_to_download.split('/')[-1] #скачивание расписания
    r = requests.get(link_to_download, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    book = openpyxl.open(filename, read_only=True)
    sheet = book.active
    data_pars = now.weekday()
    if(mes=="завтра"):  #опрделение среза расписания
        data_pars += 1 #опрделение дня недели
        if(data_pars == 7): #сброс, если конец недели
            data_pars = 0
        parsing_start = (data_pars*12)+4 #определение с какой ячейки смотреть
        parsing_end = (data_pars*12)+16 # до какой ячейки
        print(parsing_start,parsing_end)
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0): # определние чётности недели
            parsing_week = "II"
        else:
            parsing_week = "I"
    elif(mes=="сегодня"):
        if(data_pars == 7):
            data_pars = 0
        parsing_start = (data_pars*12)+4 
        parsing_end = (data_pars*12)+16
        print(parsing_start,parsing_end)
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "II"
        else:
            parsing_week = "I"
    elif(mes=="на эту неделю"):
        parsing_start = 4
        parsing_end = 76
        data_pars = 7
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "II"
        else:
            parsing_week = "I"
    elif(mes=="на следующую неделю"):
        data_pars = 8
        parsing_start = 4
        parsing_end = 76
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "I"
        else:
            parsing_week = "II"
    print(parsing_week)
    if(info_respisanie.find("Расписание на")!=False): #указание даты в итоговом сообщении
        info_respisanie +="Расписание на "
        if (data_pars == 0):
            info_respisanie +="понедельник" + "\n"
        if (data_pars == 1):
            info_respisanie +="вторник" + "\n"
        if (data_pars == 2):
            info_respisanie +="среду" + "\n"
        if (data_pars == 3):
            info_respisanie +="четверг" + "\n"
        if (data_pars == 4):
            info_respisanie +="пятницу" + "\n"
        if (data_pars == 5):
            info_respisanie +="субботу" + "\n"
        if (data_pars == 6):
            info_respisanie +="воскресенье" + "\n"
        if (data_pars == 7):
            info_respisanie +="эту неделю" + "\n"
        if (data_pars == 8):
            info_respisanie +="следующую неделю" + "\n"

    try: #поиск группы
        for i in range(0, 500):
            if(str(sheet[2][i].value).lower()==group):
                colum = i
                break
    except IndexError:
        return "Такая группа не найдена"
    
    if (data_pars < 9):
        for i in range(parsing_start, parsing_end):  #формирование расписания
            if(str(sheet[i][colum-1].value) == parsing_week):
                if(para_counter==7):
                    para_counter = 1
                    info_respisanie +="\n"+ "\n"
                if(str(sheet[i][colum].value) != "None"):
                    info_respisanie +=re.sub("^\s+|\n|\r|\s+$", '', str(para_counter) + " | "+(str(sheet[i][colum].value) + " | " + str(sheet[i][colum+1].value) + " | " + str(sheet[i][colum+2].value) + " | "+ str(sheet[i][colum+3].value))) + "\n"
                else:
                    info_respisanie += str(para_counter)+" | "+"Нету пар" + "\n"
                para_counter += 1

    info_respisanie = info_respisanie.replace("None", "Нету пар") #правка итогового сообщения
    return info_respisanie
    
