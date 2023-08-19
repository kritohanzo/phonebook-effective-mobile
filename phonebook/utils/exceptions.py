class ValidationError(Exception):
    "Исключение, выбрасываемое при ошибке валидации данных, поданных пользователем."

class NoMorePages(Exception):
    pass

class InvalidPage(Exception):
    pass