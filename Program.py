# -*- coding: utf-8 -*-

import colorama
import os
import time
from sys import platform
import requests
import webbrowser

colorama.init()

# функция которая отобразит банер нашего скрипта
def banner():
    print('-' * 50,'green')
    print(' ' * 17 + 'DefendMySystem','red')
    print('-' * 50,'green')

# функция для очистки консоли(для красоты)
def cleaner():
    if platform == "linux" or platform == "linux2":
        os.system('clear')
    if platform == "win32":
        os.system('cls')


# Я решил, что часть настроек будет лежать в .conf файлах. Поэтому я написал функцию для проверки существования этих файлов.
def checkfiles():
    arr = os.listdir('.')
    for x in arr:
        if 'delay.conf' not in arr:
            handle = open('delay.conf','w')
            handle.close()

        if 'api.conf' not in arr:
            handle = open('api.conf','w')
            handle.close()


# функция настройки скрипта.
def setting():
    handle = open('config.conf')
    data = handle.read()
    handle.close()
 
    handle = open('delay.conf')
    data2 = handle.read()
    handle.close()
    if data2 == '':
        print("Установите задержку для проверки папки загрузки(в секундах)","cyan")
        delay = input(':')
        handle = open('delay.conf','w')
        handle.write(delay)
        handle.close()
        cleaner()
    handle = open('api.conf')
    data3 = handle.read()
    handle.close()

    if data3 == '':
        print("Введите ваш api ключ","cyan")
        webbrowser.open("https://www.virustotal.com/ru/", new=2)
        api = input(':')
        handle = open('api.conf','w')
        handle.write(api)
        handle.close()
        cleaner()

# функция отправки файла на вирустотал
def sendfiles(filename,api):
    params = {'apikey': api}
    response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files={'file': (filename, open(filename, 'rb'))}, params=params)
    json_response = response.json()
    dct = eval(str(json_response))
    link = dct['permalink']
    webbrowser.open(link, new=2)

# главнуя функция, которая выполняет всю тяжелую работу
def main():
    temp = []
    path = 'C:\\Users\\Vadim\\Downloads'

    handle = open('delay.conf')
    delay = handle.read()
    handle.close()
    delay = int(delay)

    handle = open('api.conf')
    api = handle.read()
    handle.close()
    files = os.listdir(path)
    while True:
        files2 = os.listdir(path)
        if files != files2:
            for x in files2:
                if x not in files:
                    temp.append(x)
                    for x in temp:
                        filename = path + x
                    sendfiles(filename,api)
            temp = []
            files = files2
        time.sleep(delay)

banner()
checkfiles()
setting()
try:
    main()
except KeyboardInterrupt:
    exit()
