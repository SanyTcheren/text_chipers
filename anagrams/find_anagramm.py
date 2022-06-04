"""Поиск анаграмм в словаре по заданному слову."""

import argparse
from sys import stderr
from functools import reduce

def check_ru_word(word):
    """Проверка введеного слова на использование русского алфавита."""
    return reduce(
        lambda a,b: a and b,
        [letter.lower() in 'абвгдежзиклмнопрстуфхцчшщьыъэюяё' for letter in list(word)]
    )

def ask_word():
    """Запрос слова для поиска анаграмм. Возвращает сортированный список."""
    while True:
        word = input('Базовое слово: ')
        if word == '':
            return ''
        if len(word) < 3:
            print('Слово должно быть не менее чем из 3-x букв!', file=stderr)
            continue
        if not check_ru_word(word):
            print('Слово должно состоять только из букв русского алфавита', file=stderr)
            continue
        return sorted(list(word))

def condition(word):
    """Проверка что слово является реальным."""
    return not (len(word) < 3 or ('-' in word) or ('.' in word))

def get_filter_words(dictonary, func_filter):
    """Загружает слов из потока файла в список с учетом фильтра."""
    loaded_text = dictonary.read().strip().split('\n')
    loaded_text = [x.lower() for x in loaded_text if func_filter(x)]
    return loaded_text

def main(word, dictonary):
    """Печатает список найденных анаграмм."""
    words = get_filter_words(dictonary, condition)
    dictonary.close()
    while word != '':
        anagramms = []
        for anagramm in words:
            if word == sorted(list(anagramm)):
                anagramms.append(anagramm)
        print(f'Найдено {len(anagramms)} анаграмм:')
        print(*anagramms, sep='\n')
        print('Введите новое слово для поиска анаграмм (для выхода не вводите ничего)')
        word = ask_word()

def create_parser ():
    """Создаем парсер аргументов."""
    parser = argparse.ArgumentParser(
        prog = 'find_paligramm',
        description='Программа поиска анаграмм в словаре',
        epilog='@2022 Sany Tcheren')
    parser.add_argument('-d','--dictonary', type=argparse.FileType(),
                        help='файл со словарем в формате txt и кодировкой UTF-8')
    parser.add_argument('-w','--word',
                        help='слово для поиска анаграмм')
    return parser

if __name__ == '__main__':
    my_parser = create_parser()
    my_namespace = my_parser.parse_args()
    main(sorted(list(my_namespace.word)), my_namespace.dictonary)
