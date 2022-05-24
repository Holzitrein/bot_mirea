import requests
from translate import Translator
from math import floor
from datetime import datetime, timedelta
import time
import pendulum
import PIL.Image as Image
from datetime import date
translator = Translator(from_lang="english", to_lang="russian")
api_key = "81f8953f98dfe25ad251384300929c47"
city = "moscow"
url1 = "http://api.openweathermap.org/data/2.5/weather?q=moscow&appid=81f8953f98dfe25ad251384300929c47&units=metric"
url2 = "http://api.openweathermap.org/data/2.5/forecast?q=moscow&appid=81f8953f98dfe25ad251384300929c47&units=metric"
list_vector = [
    "север",
    "северо-северо-восток",
    "северо-восток",
    "востоко-северо-восток",
    "восток",
    "востоко-юго-восток",
    "юго-восток",
    "юго-юго-восток",
    "юг",
    "юго-юго-запад",
    "юго-запад",
    "западо-юго-запад",
    "запад",
    "западо-северо-запад",
    "северо-запад",
    "северо-северо-запад"
]
list_wind = [
    "Тихий",
    "Лёгкий",
    "Слабый",
    "Умеренный",
    "Свежий",
    "Сильный",
    "Крепкий",
    "Очень крепкий",
    "Шторм",
    "Сильный шторм",
    "Жестокий шторм",
    "Ураган"
]


def pogoda(msg):
    if (msg == "сейчас"):
        return pogoda_1()
    if (msg == "на сегодня"):
        return pogoda_2()
    if (msg == "на завтра"):
        return pogoda_3()
    if (msg == "на 5 дней"):
        return pogoda_4()


def fun_wind(speed, deg):
    res = "Ветер: " + list_wind[floor(((speed + 1.5) % 33) / 3)] + ", "+str(
        speed) + " м/с, " + list_vector[floor(((deg + 11.25) % 360) / 22.5)] + "\n"
    return res


def pogoda_1():
    itog = ""
    mas_icon = []
    response = requests.get(url1)
    info = response.json()
    temp_min = info["main"]["temp_min"]
    temp_max = info["main"]["temp_max"]
    state_of_now = info["weather"][0]["main"]
    press = info["main"]["pressure"]
    hum = info["main"]["humidity"]
    wind_speed = info["wind"]["speed"]
    wind_deg = info["wind"]["deg"]
    print(state_of_now)
    print(press)
    print(hum)
    print(wind_speed)
    print(translator.translate(state_of_now))
    itog += "Погода в Москве: " + "\n" + translator.translate(
        state_of_now) + ", Температура:"+str(temp_min)+"-"+str(temp_max) + "'C"+"\n"
    itog += "Давление: " + str(press) + \
        " мм рт.ст, влажность: " + str(hum) + "%" + "\n"
    itog += fun_wind(wind_speed, wind_deg)
    print(itog)
    weather_photo = "http://openweathermap.org/img/w/" + str(info['weather'][0]['icon'])  +".png"
    mas_icon.append(weather_photo)
    for i in range(len(mas_icon)):
        image = requests.get(mas_icon[i], stream=True)
        with open(str(i)+".png", "wb") as f:
            f.write(image.content)
    img = Image.new('RGB', ((len(mas_icon))*50, 50))
    for i in range(len(mas_icon)):
        img1 = Image.open(str(i)+".png")
        print(i*50)
        img.paste(img1, (i*50, 0))
    img.save("image1.png")
    f.close
    return itog


def pogoda_2():
    response = requests.get(url2)
    info = response.json()
    mas_icon = []
    itog = "Погода в Москве на сегодня" + "\n"
    itog += "/ " + str(info["list"][0]["main"]["temp"]) + " 'C // " + str(info["list"][2]["main"]["temp"]) + \
        " 'C // " + str(info["list"][4]["main"]["temp"]) + \
        " 'C // " + str(info["list"][6]["main"]["temp"]) + " 'C /"
    itog += "\n" + "УТРО" + "\n"

    itog += translator.translate(info["list"][0]["weather"][0]["main"]) + ", Температура:"+str(
        info["list"][0]["main"]["temp_min"])+"-"+str(info["list"][0]["main"]["temp_max"]) + "'C"+"\n"
    itog += "Давление: " + str(info["list"][0]["main"]["pressure"]) + \
        " мм рт.ст, влажность: " + \
            str(info["list"][0]["main"]["humidity"]) + "%" + "\n"
    itog += fun_wind(info["list"][0]["wind"]["speed"],
                     info["list"][0]["wind"]["deg"]) + "\n"
    itog += "\n" + "ДЕНЬ" + "\n"

    itog += translator.translate(info["list"][2]["weather"][0]["main"]) + ", Температура:"+str(
        info["list"][2]["main"]["temp_min"])+"-"+str(info["list"][2]["main"]["temp_max"]) + "'C"+"\n"
    itog += "Давление: " + str(info["list"][2]["main"]["pressure"]) + \
        " мм рт.ст, влажность: " + \
            str(info["list"][2]["main"]["humidity"]) + "%" + "\n"
    itog += fun_wind(info["list"][2]["wind"]["speed"],
                     info["list"][2]["wind"]["deg"]) + "\n"
    itog += "\n" + "ВЕЧЕР" + "\n"
    itog += translator.translate(info["list"][4]["weather"][0]["main"]) + ", Температура:"+str(
        info["list"][4]["main"]["temp_min"])+"-"+str(info["list"][4]["main"]["temp_max"]) + "'C"+"\n"
    itog += "Давление: " + str(info["list"][4]["main"]["pressure"]) + \
        " мм рт.ст, влажность: " + \
            str(info["list"][4]["main"]["humidity"]) + "%" + "\n"
    itog += fun_wind(info["list"][4]["wind"]["speed"],
                     info["list"][4]["wind"]["deg"]) + "\n"
    itog += "\n" + "НОЧЬ" + "\n"
    itog += translator.translate(info["list"][6]["weather"][0]["main"]) + ", Температура:"+str(
        info["list"][6]["main"]["temp_min"])+"-"+str(info["list"][6]["main"]["temp_max"]) + "'C"+"\n"
    itog += "Давление: " + str(info["list"][6]["main"]["pressure"]) + \
        " мм рт.ст, влажность: " + \
            str(info["list"][6]["main"]["humidity"]) + "%" + "\n"
    itog += fun_wind(info["list"][6]["wind"]["speed"],
                     info["list"][6]["wind"]["deg"]) + "\n"
    weather_photo = "http://openweathermap.org/img/w/" + str(info['list'][0]['weather'][0]['icon'])  +".png"
    mas_icon.append(weather_photo)
    weather_photo = "http://openweathermap.org/img/w/" + str(info['list'][2]['weather'][0]['icon'])  +".png"
    mas_icon.append(weather_photo)
    weather_photo = "http://openweathermap.org/img/w/" + str(info['list'][4]['weather'][0]['icon'])  +".png"
    mas_icon.append(weather_photo)
    weather_photo = "http://openweathermap.org/img/w/" + str(info['list'][6]['weather'][0]['icon'])  +".png"
    mas_icon.append(weather_photo)
    print(itog)
    for i in range(len(mas_icon)):
        image = requests.get(mas_icon[i], stream=True)
        with open(str(i)+".png", "wb") as f:
            f.write(image.content)
    img = Image.new('RGB', ((len(mas_icon))*50, 50))
    for i in range(len(mas_icon)):
        img1 = Image.open(str(i)+".png")
        print(i*50)
        img.paste(img1, (i*50, 0))
    img.save("image2.png")
    f.close
    return itog

def pogoda_3():
    response = requests.get(url2)
    info = response.json()
    mas_icon = []
    itog = "Погода в Москве на завтра" + "\n"
    itog += "/ " + str(info["list"][8]["main"]["temp"]) + " 'C // " + str(info["list"][10]["main"]["temp"]) + \
        " 'C // " + str(info["list"][12]["main"]["temp"]) + \
        " 'C // " + str(info["list"][14]["main"]["temp"]) + " 'C /"
    itog += "\n" + "УТРО" + "\n"

    itog += translator.translate(info["list"][8]["weather"][0]["main"]) + ", Температура:"+str(
        info["list"][8]["main"]["temp_min"])+"-"+str(info["list"][8]["main"]["temp_max"]) + "'C"+"\n"
    itog += "Давление: " + str(info["list"][8]["main"]["pressure"]) + \
        " мм рт.ст, влажность: " + \
            str(info["list"][8]["main"]["humidity"]) + "%" + "\n"
    itog += fun_wind(info["list"][8]["wind"]["speed"],
                     info["list"][8]["wind"]["deg"]) + "\n"
    itog += "\n" + "ДЕНЬ" + "\n"

    itog += translator.translate(info["list"][10]["weather"][0]["main"]) + ", Температура:"+str(
        info["list"][10]["main"]["temp_min"])+"-"+str(info["list"][10]["main"]["temp_max"]) + "'C"+"\n"
    itog += "Давление: " + str(info["list"][10]["main"]["pressure"]) + \
        " мм рт.ст, влажность: " + \
            str(info["list"][10]["main"]["humidity"]) + "%" + "\n"
    itog += fun_wind(info["list"][10]["wind"]["speed"],
                     info["list"][10]["wind"]["deg"]) + "\n"
    itog += "\n" + "ВЕЧЕР" + "\n"
    itog += translator.translate(info["list"][12]["weather"][0]["main"]) + ", Температура:"+str(
        info["list"][12]["main"]["temp_min"])+"-"+str(info["list"][12]["main"]["temp_max"]) + "'C"+"\n"
    itog += "Давление: " + str(info["list"][12]["main"]["pressure"]) + \
        " мм рт.ст, влажность: " + \
            str(info["list"][12]["main"]["humidity"]) + "%" + "\n"
    itog += fun_wind(info["list"][12]["wind"]["speed"],
                     info["list"][12]["wind"]["deg"]) + "\n"
    itog += "\n" + "НОЧЬ" + "\n"
    itog += translator.translate(info["list"][14]["weather"][0]["main"]) + ", Температура:"+str(
        info["list"][14]["main"]["temp_min"])+"-"+str(info["list"][14]["main"]["temp_max"]) + "'C"+"\n"
    itog += "Давление: " + str(info["list"][14]["main"]["pressure"]) + \
        " мм рт.ст, влажность: " + \
            str(info["list"][14]["main"]["humidity"]) + "%" + "\n"
    itog += fun_wind(info["list"][14]["wind"]["speed"],
                     info["list"][14]["wind"]["deg"]) + "\n"
    print(itog)
    weather_photo = "http://openweathermap.org/img/w/" + str(info['list'][8]['weather'][0]['icon'])  +".png"
    mas_icon.append(weather_photo)
    weather_photo = "http://openweathermap.org/img/w/" + str(info['list'][10]['weather'][0]['icon'])  +".png"
    mas_icon.append(weather_photo)
    weather_photo = "http://openweathermap.org/img/w/" + str(info['list'][12]['weather'][0]['icon'])  +".png"
    mas_icon.append(weather_photo)
    weather_photo = "http://openweathermap.org/img/w/" + str(info['list'][14]['weather'][0]['icon'])  +".png"
    mas_icon.append(weather_photo)
    print(itog)
    for i in range(len(mas_icon)):
        image = requests.get(mas_icon[i], stream=True)
        with open(str(i)+".png", "wb") as f:
            f.write(image.content)
    img = Image.new('RGB', ((len(mas_icon))*50, 50))
    for i in range(len(mas_icon)):
        img1 = Image.open(str(i)+".png")
        print(i*50)
        img.paste(img1, (i*50, 0))
    img.save("image3.png")
    return itog


def pogoda_4():
    mas_icon = []
    response = requests.get(url2)
    info = response.json()
    named_tuple = time.localtime()
    time_string = time.strftime("%m-%d", named_tuple)
    itog = "Погода в Москве на 5 дней с " + time_string + "\n"
    itog += "/ " + str(info["list"][3]["main"]["temp"]) + " 'C // " + str(info["list"][11]["main"]["temp"]) + " 'C // " + str(info["list"][19]
                                                                                                                              ["main"]["temp"]) + " 'C // " + str(info["list"][27]["main"]["temp"]) + " 'C // " + str(info["list"][35]["main"]["temp"]) + " 'C ДЕНЬ" + "\n"
    itog += "/ " + str(info["list"][0]["main"]["temp"]) + " 'C // " + str(info["list"][8]["main"]["temp"]) + " 'C // " + str(info["list"][17]
                                                                                                                             ["main"]["temp"]) + " 'C // " + str(info["list"][24]["main"]["temp"]) + " 'C // " + str(info["list"][32]["main"]["temp"]) + " 'C НОЧЬ" + "\n"
    weather_photo = "http://openweathermap.org/img/w/" + str(info['list'][3]['weather'][0]['icon'])  +".png"
    mas_icon.append(weather_photo)
    weather_photo = "http://openweathermap.org/img/w/" + str(info['list'][11]['weather'][0]['icon'])  +".png"
    mas_icon.append(weather_photo)
    weather_photo = "http://openweathermap.org/img/w/" + str(info['list'][19]['weather'][0]['icon'])  +".png"
    mas_icon.append(weather_photo)
    weather_photo = "http://openweathermap.org/img/w/" + str(info['list'][27]['weather'][0]['icon'])  +".png"
    mas_icon.append(weather_photo)
    weather_photo = "http://openweathermap.org/img/w/" + str(info['list'][35]['weather'][0]['icon'])  +".png"
    mas_icon.append(weather_photo)
    print(itog)
    for i in range(len(mas_icon)):
        image = requests.get(mas_icon[i], stream=True)
        with open(str(i)+".png", "wb") as f:
            f.write(image.content)
    img = Image.new('RGB', ((len(mas_icon))*50, 50))
    for i in range(len(mas_icon)):
        img1 = Image.open(str(i)+".png")
        print(i*50)
        img.paste(img1, (i*50, 0))
    img.save("image4.png")
    return(itog)
