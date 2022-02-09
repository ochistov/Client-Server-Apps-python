# 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. Для этого:

#     Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
#     Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
import json
import pprint as p

# из текста задания я понял, что JSON надо не переписывать, а дополнять. Далее задание выполнял исходя из такого условия


def writeOrderToJson(item, quantity, price, buyer, date):
    with open('orders.json', encoding='utf-8') as jsonfile:
        doneDict = json.load(jsonfile)
        tempdict = {'item': item, 'quantity': quantity,
                    'price': price, 'buyer': buyer, 'date': date}
        doneDict['orders'] += [tempdict]
    with open('orders.json', 'w', encoding='utf-8') as outputfile:
        json.dump(doneDict, outputfile, indent=4)


########## tests ##########
count = int(input('How much test_data to add?: '))  # it was 6 :)
for i in range(count):
    writeOrderToJson(f'test_item_{i+1}', f'test_quantity_{i+1}',
                     f'test_price_{i+1}', f'test_buyer_{i+1}', f'test_date_{i+1}')
