# 1. Каждое из слов «разработка», «сокет», «декоратор» представить
# в строковом формате и проверить тип и содержание соответствующих
# переменных. Затем с помощью онлайн-конвертера преобразовать строковые
# представление в формат Unicode и также проверить тип и содержимое переменных.

# Вместо онлайн-конвертера написал свою маленькую API (готовой в гугле не нашёл :D),
# принимающую на вход GET запрос, вида {action='string', value = 'string'}, где action может быть равно
# 'encode' или 'decode'. Апишку развернул на VDS под управлением Ubuntu 20.04 на
# связке NGINX + Node.js. Исходник приложу к пулл-реквесту с заданиями к 1 уроку (enc-decryptor.js)


import requests
# Получаем строку из слов, разделённых запятой, с которой будем работать
stringToEnc = str(input('Please input some words separeted by comma: '))
url = 'http://130.61.54.130'
decList = []

# функция, отправляющая GET запрос с action=encode и возвращающая ответ строкой


def myencoder(string):
    params = dict(action='encode',
                  value=string)
    res = requests.get(url, params=params)
    return str(res.text)

# функция, отправляющая GET запрос с action=decode и возвращающая ответ строкой


def mydecoder(string):
    params = dict(action='decode',
                  value=string)
    res = requests.get(url, params=params)
    return str(res.text)


# разбиваем строку на список слов, применяем к каждому из них функцию myencoder,
# результат выводим в консоль и пишем в список для decode
for word in stringToEnc.split(','):
    resEnc = myencoder(word)
    print(word, ':', resEnc, type(resEnc))
    decList += [str(resEnc)]

# каждое слово из списка decList передаём в функцию mydecoder, выводим в консоль результат
for word in decList:
    resDec = mydecoder(word)
    print(word, ':', resDec, type(resDec))
