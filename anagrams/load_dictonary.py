"""Загружает текстовый файл как список."""

def is_True(word):
    """Служебная функция для возврата True."""
    return True

def get_words(dictonary):
    """Загрузка слов из текстового файла и возврат списка."""
    with open(dictonary) as in_file:
        loaded_text = in_file.read().strip().split('\n')
        loaded_text = [x.lower() for x in loaded_text]
        return loaded_text
    
def get_filter_words(dictonary, func_filter = is_True):
    """Загружает слов из файла в список с учетом фильтра."""
    with open(dictonary) as in_file:
        loaded_text = in_file.read().strip().split('\n')
        loaded_text = [x.lower() for x in loaded_text if func_filter(x))]
        return loaded_text
    
