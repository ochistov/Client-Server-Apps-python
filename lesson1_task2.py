# 2. Каждое из слов «class», «function», «method» записать в байтовом типе
# без преобразования в последовательность кодов (не используя методы encode и decode)
# и определить тип, содержимое и длину соответствующих переменных.

# bytelist = [b'class', b'function', b'method']

bytelist = input('Please insert words divided by comma: ').split(',')


def toByter(elem):
    try:
        res = eval(f"b'{elem}'")
        print(type(res), res, len(res))
    except:
        print('Whoops, smth goes wrong')


for elem in bytelist:
    toByter(elem)
