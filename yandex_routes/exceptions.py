# -*- coding: utf8 -*-


class ResponseStatusWarning(UserWarning):
    """
    Статус запроса не 200
    """
    pass


class StationNotFoundException(Exception):
    """
    Исключение, возникающее если нечёткий поиск по названию станции не дал результата
    """
    pass
