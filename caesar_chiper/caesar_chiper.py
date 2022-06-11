"""Шифр Цезаря."""

import curses
from functools import reduce
from buttons_curses import GroupButton
from pyxclip import Clerk


class CoderCaesar:
    """Code caesar chiper."""

    text = ''
    code = ''
    addition = 0
    alfabet = {
        'ru': ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л',
               'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш',
               'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я'],
        'RU': ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л',
               'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш',
               'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я'],
        'en': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
        'EN': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
        'num': ['0', '1', '2', '3', '4', '5', '6', '7', '8','9']
    }
    files = {
        'ru': 'russian.txt'
    }
    dictionary = None

    def clear(self):
        """Clear text and code."""
        self.text = ''
        self.code = ''

    def encode(self):
        """Encode text."""
        code = ''
        for char in self.text:
            for base in self.alfabet.values():
                if char in base:
                    index = base.index(char)
                    char = base[(index+self.addition)%len(base)]
                    break
            code += char
        self.code = code

    def load_dictionary(self, path):
        """Ленивая загрузка словаря."""
        if self.dictionary is None:
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as in_file:
                    load_text = in_file.read().strip().split()
                    self.dictionary = {w.lower() for w in load_text}
            except FileNotFoundError:
                pass

    def hack(self, language='ru'):
        """Hack text."""
        self.load_dictionary(self.files[language])
        if self.dictionary is None:
            self.code = 'Не удалось загрузить файл словаря.'
        else:
            find_words = []
            for add in range(len(self.alfabet[language])):
                self.addition = add
                self.encode()
                words = self.code.lower().split()
                find_words.append(reduce(
                    lambda res, inst: res + (inst in self.dictionary),
                    words, 0))
            # Преобразуем добавку в отрицательное значение для удобства
            self.addition = (find_words.index(max(find_words)) -
                             len(self.alfabet[language]))
            self.encode()


class CaesarApp:
    """Caesar application."""

    def __init__(self, stdscr):
        """Init app."""
        curses.curs_set(0)
        self.stdscr = stdscr
        self.is_alive = True
        self.clerk = Clerk()
        self.coder = CoderCaesar()

        self.buttons = GroupButton(stdscr, 'PASTE', self._paste)
        self.buttons.add('COPY', self._copy)
        self.buttons.add('CLEAR', self.coder.clear)
        self.buttons.add('HACK', self._hack)
        self.buttons.add('QUIT', self._quit)

    def _copy(self):
        self.clerk.copy(self.coder.code)

    def _paste(self):
        self.coder.text = self.clerk.paste()
        self.coder.encode()

    def  _hack(self):
        self.coder.hack()

    def _quit(self):
        self.is_alive = False

    def render(self):
        """Render app."""
        _, width = self.stdscr.getmaxyx()
        self.stdscr.erase()
        self.buttons.render(0,(width-26)//2)
        self.stdscr.addstr(f'\n{"⠿"*width}')
        self.stdscr.addstr(self.coder.text)
        addition_sign = '+' if self.coder.addition > 0 else ''
        addition_str = f'ADDITION:{addition_sign}{self.coder.addition} '.center(width,'⠿')
        self.stdscr.addstr('\n' + addition_str)
        self.stdscr.addstr(self.coder.code)

    def input(self):
        """Input keyboard."""
        key = self.stdscr.get_wch()
        if key == '\n':
            self.buttons.push()
        elif key == 261:
            self.buttons.next()
        elif key == 260:
            self.buttons.back()
        elif key == 259:
            self.coder.addition+= 1
            self.coder.encode()
        elif key == 258:
            self.coder.addition -= 1
            self.coder.encode()
        elif isinstance(key, str):
            self.coder.text += key
            self.coder.encode()
        elif key == 263:
            self.coder.text = self.coder.text[:-2]
            self.coder.encode()

    def run(self):
        """Start render and input."""
        while self.is_alive :
            self.render()
            self.input()


def main(stdscr):
    """Run app."""
    app = CaesarApp(stdscr)
    app.run()


if __name__ == '__main__':
    print("""
                    ШИФР ЦЕЗАРЯ
    Шифр Цезаря — это вид шифра подстановки, в котором каждый символ
    в открытом тексте заменяется символом, находящимся на некотором
    постоянном числе позиций левее или правее него в алфавите.

    Управление:
    ⬆ ⬇      изменение ключа шифра
    ➡ ⬅      выбор активной кнопки
    <Enter>  исполнение активной кнопки
    [PASTE]  вставка из системного буфера
    [COPY]   копирование в системный буфер
    [CLEAR]  очистка окна ввода текста
    [HACK]   подбор ключа к шифру (только ru)
    [QUIT]   выход из приложения

    @2022 Sany Tcheren.
     """)
    input()
    curses.wrapper(main)
