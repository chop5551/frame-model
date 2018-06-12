__all__ = ('Slot',)


class Slot:
    """
    Слот
    """
    # Имена системных слотов
    SYSTEMS_NAMES = ('Процедура')

    # УКАЗАТЕЛИ НАСЛЕДОВАНИЯ
    # Значение слота наследуется
    SAME = 'НАСЛЕДУЕТСЯ'
    # Значение слота не наследуется
    UNIQUE = 'НЕ_НАСЛЕДУЕТСЯ'
    # При отсутствии значения в текущем слоте оно наследуется из фрейма верхнего уровня,
    # однако в случае определения значения текущего слота оно может быть уникальным
    OVERRIDE = 'ПЕРЕОПРЕДЕЛЯЕТСЯ'
    # При наследовании значения из родителя слот не записывается в json
    FINAL = 'НЕ_ЗАПИСЫВАЕТСЯ'

    def __init__(self, name, value, inheritance_type, daemon = None):
        self._name = name
        self._type = value.__class__.__name__
        self._inheritance_type = inheritance_type
        self._value = value
        self._daemon = daemon

    def __getattr__(self, attr):
        return getattr(self._value, attr)

    def __iter__(self):
        return iter(self._value)

    @property
    def is_system(self):
        return self._name in self.SYSTEMS_NAMES

    @property
    def has_daemon(self):
        return self._daemon != None

    @property
    def daemon(self):
        return self._daemon

    @property
    def inheritance_type(self):
        return self._inheritance_type

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        # FIXME: TypeError: Object of type 'function' is not JSON serializable
        return self._value  # or self._daemon

    # noinspection PyCallingNonCallable
    @value.setter
    def value(self, value):
        self._value = value

    @daemon.setter
    def daemon(self, daemon):
        self._daemon = daemon

    @property
    def type(self):
        return self._type

    def print(self, depth):
        if not self.is_system and self._value != None:
            print(" "*depth + self.name + ": " + str(self._value))