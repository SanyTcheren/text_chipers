"""Classes ofr coder/decoder projects."""

import code_exc as exc


class Coder:
    """Coder."""

    empty_default = 'rest is just filler'

    def __init__(self, key, table=None, empty=None):
        self.key = key
        self.table = table if table else {}
        self.empty = empty.strip() if empty else self.empty_default

    def _normalize(self, text, length):
        """Normalize length of text."""
        text = text.split()
        while len(text) != length:
            if len(text) < length:
                text = text + self.empty.split()
            else:
                text = text[:-1]
        return ' '.join(text)

    def _map(self, text):
        """Replace word from table in text."""
        result = []
        for word in text.strip().lower().split():
            result.append(word)
            for key, value in self.table.items():
                if word == value:
                    result.pop()
                    result.append(key)
                    break
        return ' '.join(result)

    def _route(self, text):
        """Route word in text."""
        len_key = len(self.key)
        matrix = [[] for _ in range(len_key)]
        indx = 0
        for word in text.strip().split():
            matrix[indx].append(word)
            indx = 0 if indx == len_key-1 else indx+1
        result = []
        for col in self.key:
            if col > 0:
                temp = ' '.join(matrix[col-1])
            else:
                temp = ' '.join(matrix[abs(col)-1][::-1])
            result.append(temp)
        return ' '.join(result)

    def add_table(self, table):
        """Add table."""
        self.table = self.table | table

    def encode(self, text, length):
        """Encode text."""
        if length < len(text.split()):
            raise exc.LengthSmall(length)
        if length % len(self.key) != 0:
            raise exc.LengthNotKey(length, len(self.key))
        code = self._map(text)
        code = self._normalize(code, length)
        code = self._route(code)
        return code


class Decoder:
    """Decode text."""

    def __init__(self, key, table=None):
        self.key = key
        self.table = table if table else {}

    def check_key(self, text):
        """Проверка ключа на кратность длине текста."""
        if len(text.split()) % len(self.key) != 0:
            raise exc.KeyNotLength(len(self.key), len(text.split()))
        return int(len(text.split())/len(self.key))

    def _route(self, text, key=None):
        """Decode text."""
        if key is not None:
            self.key = key
        height = self.check_key(text)
        matrix = [[] for _ in range(len(self.key))]
        indx = 0
        for col in self.key:
            if col > 0:
                matrix[col-1] = text.split()[indx*height:(indx+1)*height][::-1]
            else:
                matrix[abs(col)-1] = text.split()[indx*height:(indx+1)*height]
            indx += 1
        result = []
        while len(matrix[0]) != 0:
            for col in matrix:
                result.append(col.pop())
        return ' '.join(result)

    def _map(self, text, table=None):
        """Меняем закодированые слова в соответствии с таблицей."""
        result = []
        table = self.table if table is None else table
        for word in text.lower().split():
            if word in table.keys():
                word = table[word]
            result.append(word)
        return ' '.join(result)

    def decode(self, text, length=None):
        """Decode text."""
        length = length if length else len(text.split())
        text = self._route(text)
        text = self._map(text)
        if length is not None:
            text = ' '.join(text.split()[:length])
        return text


def main():
    """Test all."""
    table = {
        'village': 'enemy',
        'roanoke': 'cavalry',
        'goodwin': 'tennessee',
        'snow': 'rebels'
    }
    text = 'Enemy cavalry heading to Tennessee with Rebels gone ' +\
        'you are free to transport your supplies south'
    code = 'rest transport you goodwin village ' +\
        'roanoke with are your is just suppleis free ' +\
        'snow heading to gone to south filler'
    key = [-1, 2, -3, 4]
#   length = 20
#   coder = Coder(key, table)
#   print(code)
#   print(coder.encode(text, length))
    decoder = Decoder(key, table)
    print(text)
    print(decoder.decode(code, 16))


if __name__ == '__main__':
    main()
