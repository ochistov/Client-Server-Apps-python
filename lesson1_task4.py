# Преобразовать слова «разработка», «администрирование», «protocol»,
# «standard» из строкового представления в байтовое и выполнить обратное
# преобразование (используя методы encode и decode).

list = ['разработка', 'администрирование', 'protocol', 'standart']

inputList = input('Please insert words divided by comma: ').split(',')


def encDecoder(word):
    encodedWord = word.encode('utf-8')
    print(f'Word {word} in bytes is: ', encodedWord)
    decodedWord = encodedWord.decode('utf-8')
    print(f'Bytes array {encodedWord} is: ', decodedWord)


for word in inputList:
    encDecoder(word)
