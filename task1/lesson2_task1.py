# 1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:

#     Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
#     Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
#     Проверить работу программы через вызов функции write_to_csv().
import csv
import os
import re
import pprint as p


def getData():
    osProdList = []
    osNameList = []
    osCodeList = []
    osTypeList = []
    mainData = ['Изготовитель системы',
                'Название ОС', 'Код продукта', 'Тип системы']
    workList = []
    result = [mainData]
    for elem in os.listdir(os.getcwd()):
        if os.path.isfile(os.path.join(os.getcwd(), elem)) and re.fullmatch('\S*\s*\d*.txt', elem):
            if bool(input(f'Is that - {elem} - file with data? 1- yes, 0 - no: ')):
                workList += [elem]

    for file in workList:
        with open(file) as nowOpened:
            lines = nowOpened.readlines()
            for line in lines:
                if re.match('^Изготовитель ОС', line):
                    osProdList += [line.split(':')[1].strip()]
                elif re.match('^Название ОС', line):
                    osNameList += [line.split(':')[1].strip()]
                elif re.match('^Код продукта', line):
                    osCodeList += [line.split(':')[1].strip()]
                elif re.match('^Тип системы', line):
                    osTypeList += [line.split(':')[1].strip()]
    for i in range(len(workList)):
        result += [[osProdList[i], osNameList[i],
                   osCodeList[i], osTypeList[i]]]
    return result


def writeToCsv(csvfilename):
    with open(csvfilename, 'w', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(getData())
    print('Created CSV file contents:')
    with open(csvfilename, encoding='utf-8') as donefile:
        print(donefile.read())


writeToCsv('task1.csv')
