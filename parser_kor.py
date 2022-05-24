import requests
from bs4 import BeautifulSoup
from datetime import date
import datetime
import time
import matplotlib.pyplot as graf
import numpy as np
import re
now = datetime.datetime.now()
named_tuple = time.localtime()
time_string = time.strftime("%H:%M", named_tuple)

def corona(mes):
    if (mes != 0):
        return corona_2(mes)
    else:
        return corona_1()
    
def corona_img():
    page = requests.get("https://coronavirusstat.ru/country/russia/")
    soup = BeautifulSoup(page.text, "html.parser")
    res = []
    res_1 = []
    res_2 = []
    res_3 = []
    res_4 = []
    itog = soup.find("table", {"class":"table table-bordered small"}).find_all("th")
    for i in range(5,len(itog)-5):
        res_4.append(itog[i].text[:-5])
    itog = soup.find("table", {"class":"table table-bordered small"}).find_all("td")
    count_1 = 1
    for i in range(len(itog)-20):
        if(count_1 == 4):
            count_1 = 1
        else:
            res.append(str(itog[i].text))
            count_1 += 1
    for i in range(len(res)):
        res[i] = res[i][1:]
        res[i] = res[i][:res[i].find(" ")]
    for i in range(0,len(res),3):
        res_1.append(int(res[i]))
    for i in range(1,len(res),3):
        res_2.append(int(res[i]))
    for i in range(2,len(res),3):
        res_3.append(int(res[i]))
    graf.plot([], [], color ='red',
         label ='Заражённых')
    graf.plot([], [], color ='green',
         label ='Вылеченных')
    graf.plot([], [], color ='black',
         label ='Погибших')
    graf.stackplot(res_4, res_1, res_2, res_3, baseline ='zero', colors =['red', 'green', 'black'])
    graf.xticks(rotation='25')
    graf.legend()
    graf.title('Россия статистика по коронавирусу')
    fig1 = graf.gcf()
    graf.grid(True)
    graf.draw()
    fig1.savefig('grafik.png', dpi=200)

def corona_1():
    page = requests.get("https://coronavirusstat.ru/country/russia/")
    soup = BeautifulSoup(page.text, "html.parser")
    res_1 = []
    res_2 = []
    return_file = ""
    itog = soup.findAll("span", {"class":"text-muted"})
    for i in range(len(itog)):
        if(str(itog[i].text)[1:].isdigit()):
            res_2.append(int(itog[i].text))
    itog = soup.findAll("div", {"class":"row justify-content-md-center"})
    res_1.append(str(itog[0].find("div", {"title":"Короновирус Россия: Случаев"}).find("b").text)[:-5].replace(",", "."))
    res_1.append(str(itog[0].find("div", {"title":"Короновирус Россия: Активных"}).find("b").text)[:-5].replace(",", "."))
    res_1.append(str(itog[0].find("div", {"title":"Короновирус Россия: Вылечено"}).find("b").text)[:-5].replace(",", "."))
    res_1.append(str(itog[0].find("div", {"title":"Короновирус Россия: Умерло"}).find("b").text)[:-5].replace(",", "."))
    res_1[0] = float(res_1[0])*1000000
    res_1[1] = float(res_1[1])*1000
    res_1[2] = float(res_1[2])*1000000
    res_1[3] = float(res_1[3])*1000
    return_file += "По состоянию на " + str(now.day) +  "." + str(now.month) +" "+   str(time_string) + "\n"
    return_file += "Случаев: " + str(res_1[0]) + " (" + str(res_2[0]) + " за сегодня)" + "\n"
    return_file += "Активных: " + str(res_1[1]) + " (" + str(res_2[1]) + " за сегодня)" + "\n"
    return_file += "Вылечено: " + str(res_1[2]) + " (" + str(res_2[2]) + " за сегодня)" + "\n"
    return_file += "Умерло: " + str(res_1[3]) + " (" + str(res_2[3]) + " за сегодня)" + "\n"
    print(return_file)
    corona_img()
    return return_file

def corona_2(mes):
    ziv = 0
    murder = 0
    return_file = ""
    res = ""
    page = requests.get("https://coronavirusstat.ru")
    soup = BeautifulSoup(page.text, "html.parser")
    itog = soup.findAll("div", {"class":"row border border-bottom-0 c_search_row"})
    for i in range(len(itog)):
        if((itog[i].find("span", {"class":"small"}).text.lower()).find(mes)!=-1):
            region = (itog[i].find("a").text)
            res = (itog[i].find_all("div", {"class":"p-1 col-4 col-sm-2"}))
            ziv = (itog[i].find("div", {"class":"p-1 col-4 col-sm-3"}).text)
            murder = (itog[i].find("div", {"class":"p-1 col-3 col-sm-2 d-none d-sm-block"}).text)
    res[0] = (res[0].find("div", {"class":"h6 m-0"}).text)[:-2]
    res[0] = re.sub("^\s+|\n|\r|\t|\s+$", '', res[0])
    res[0] = res[0][:-1]
    res[1] = (res[1].find("div", {"class":"h6 m-0"}).text)
    res[1] = re.sub("^\s+|\n|\r|\s+$", '', res[1])
    r_1 = res[0].replace("+", " ")
    r_1 = r_1.split()
    r_2 = res[1].replace("+", " ")
    r_2 = r_2.split()
    ziv = re.sub("^\s+|\n|\r|\t|\s+$", '', ziv)
    ziv = ziv[:-2]
    ziv = re.sub('\D', '', ziv)
    murder = re.sub("^\s+|\n|\r|\t|\s+$", '', murder)
    murder = re.sub('\D', '', murder)
    return_file += "По состоянию на " + str(now.day) +  "." + str(now.month) +" "+   str(time_string) + "\n"
    return_file += "Регион: " + str(region) +"\n"
    return_file += "Случаев: " + str(res[0]) + "\n"
    return_file += "Активных: " + str(ziv) + "\n"
    return_file += "Вылечено: " + str(res[1]) + "\n"
    return_file += "Умерло: " + str(murder) + "\n"
    print(return_file)
    return return_file
    
