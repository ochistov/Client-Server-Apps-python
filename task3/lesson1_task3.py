# 3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата. Для этого:

#     Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке ASCII (например, €);
#     Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
#     Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
import yaml
testData = {
    'list': ['test1', 2, 'test3'],
    'integer': 2,
    'dict': {'key1': '2€', 'key2': '3†', 'key3': '4☺'}
}
with open('task3.yaml', 'w', encoding='utf-8') as outputfile:
    yaml.dump(testData, outputfile,
              default_flow_style=True, allow_unicode=True)

######  TEST  ######
with open('task3.yaml', encoding='utf-8') as inputfile:
    fileContent = yaml.load(inputfile, Loader=yaml.FullLoader)
    print(fileContent)
