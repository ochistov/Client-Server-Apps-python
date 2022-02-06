# Создать текстовый файл test_file.txt, заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор». Далее забыть о том,
# что мы сами только что создали этот файл и исходить из того, что перед
# нами файл в неизвестной кодировке. Задача: открыть этот файл БЕЗ ОШИБОК
# вне зависимости от того, в какой кодировке он был создан.
strCount = int(input('Please insert integer number of strings in file: '))
stringsToFile = []
for i in range(strCount):
    stringsToFile += [str(input(f'Insert {i + 1} string: '))]
file = './lesson1_task6.txt'
with open(file, 'w') as newfile:
    for string in stringsToFile:
        newfile.write(string + '\n')
file1 = open(file, 'r')
file1.close
fileEncoding = file1.encoding

with open(file, 'r', encoding=fileEncoding) as readFile:
    for line in readFile:
        print(line, end='')
