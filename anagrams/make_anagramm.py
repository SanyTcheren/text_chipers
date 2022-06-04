"""Интерактивный поиск анаграмм."""

import argparse
from sys import stderr
from collections import Counter

def get_words(in_file):
    """Загрузка слов из открытого текстового файла и возврат списка."""
    loaded_text = in_file.read().strip().split('\n')
    loaded_text = [x.lower() for x in loaded_text]
    return loaded_text

def inner_word(component,target):
    """
    Проверка что component входит в target.

    Работает с Counter.
    Для суффиксов и сокращений испоьзуем "-" и '.'
    """
    for key in component:
        if key in '-.':
            continue
        if not key in target or component[key] > target[key]:
            return False
    return True

def get_dict_for_anagramm(word, words):
    """Выборка слов которые могут участвовать в построениии анаграммы."""
    target = Counter(word)
    dictonary = dict()
    for component in words:
        if inner_word(Counter(component), target):
            dictonary[component] = Counter(component)
    return dictonary

def refresh_dict(target, dict_anagramm):
    """Обновление словаря для анаграмм."""
    clon = dict_anagramm.copy()
    for component in clon:
        if not inner_word(clon[component], target):
            dict_anagramm.pop(component)

def get_prt(word):
    """Замыкаем функцию на базовое слово."""
    def prt(dict_anagramm, target):
        """Печать текущего состояния анаграммы."""
        nonlocal word
        print(f'Составляем анаграмму для {word}')
        print('Выберете слово из предложенных [буквы которые останутся для следующего шага]:')
        for candidat in dict_anagramm:
            balance = target.copy()
            candidat_dict = dict_anagramm[candidat]
            for letter in candidat_dict:
                if letter in '-.':
                    continue
                balance[letter] = balance[letter] - candidat_dict[letter]
                if balance[letter] == 0:
                    balance.pop(letter)
            print(candidat, '[', *[f'{x}:{balance[x]}' for x in balance],']')
    return prt

def get_next_word(anagramm, target, dict_anagramm):
    """Добавление следущего слова в анаграмму."""
    while True:
        print('Продолжите анаграмму (для сброса оставьте пустым)')
        print(*anagramm, sep=' ', end=' :')
        word = input()
        if word == '':
            return False
        if word in dict_anagramm:
            break
        print('Ваше слово отсутствует в предложенных', file=stderr)
    anagramm.append(word)
    for letter,value in dict_anagramm[word].items():
        target[letter] = target[letter] - value
        if target[letter] == 0:
            target.pop(letter)
    refresh_dict(target, dict_anagramm)
    return True

def convert_to_anagramm(word, dict_anagramm):
    """Составление анаграммы."""
    anagramm = []
    target = Counter(word)
    if ' ' in target:
        target.pop(' ')
    prt_condition = get_prt(word)
    while True:
        prt_condition(dict_anagramm, target)
        if not get_next_word(anagramm, target, dict_anagramm):
            print('Отмена поиска анаграммы!')
            break
        if len(target) == 0:
            print('Анаграмма составлена:')
            print(*anagramm, sep=' ')
            break
        if len(dict_anagramm) == 0:
            print('Неудача! Закончились слова')
            break

def main(dictonary):
    """Поиск и печать анаграмм."""
    words = get_words(dictonary)
    while True:
        print('Интерактивный поиск анаграмм, (если хотите выйти ничего не вводите).')
        base_word = input('Слово для составления анаграммы: ').lower()
        if base_word == '':
            break
        dict_anagramm = get_dict_for_anagramm(base_word, words)
        convert_to_anagramm(base_word,dict_anagramm)

def create_parser ():
    """Создаем парсер аргументов."""
    parser = argparse.ArgumentParser(
        prog = 'make_anagramm',
        description='Интерактивное составление анаграмм',
        epilog='@2022 Sany Tcheren')
    parser.add_argument('-d','--dictonary', type=argparse.FileType(),
                        help='файл со словарем в формате txt и кодировкой UTF-8')
    return parser

if __name__ == '__main__':
    my_parser = create_parser()
    my_namespace = my_parser.parse_args()
    main(my_namespace.dictonary)
