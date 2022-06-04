"""Exception for coder/decoder projects."""


class LengthSmall(Exception):
    """Длинна кодируемого сообщения меньше  длинны текста."""

    def __init__(
        self, length,
        message='длина кодируемого сообщения, меньше самого сообщения.'
    ):
        self.length = length
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'({self.length}) -> {self.message}'


class LengthNotKey(Exception):
    """Длинна кодируемого сообщения не кратна длине ключа."""

    def __init__(
        self, length, len_key,
        message='длина кодируемого сообщения не кратна длине ключа'
    ):
        self.multiplicity = f'{length}/{len_key}'
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'({self.multiplicity}) -> {self.message}'


class KeyNotLength(Exception):
    """Длина ключа не кратна длине текста."""

    def __init__(
        self, len_key, length,
        message='длина ключа не кратна длине сообщения'
    ):
        self.multiplicity = f'{len_key}/{length}'
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'({self.multiplicity}) -> {self.message}'
