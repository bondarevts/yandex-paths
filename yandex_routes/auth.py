# -*- coding: utf8 -*-

import re
import collections
import functools

import requests


@functools.lru_cache()
def get_yandex_auth_keys():
    """
    Создаёт подключение к Яндексу и получает авторизационные данные
    поле yandexuid должно быть выставлено в cookies, key передаётся в запросах
    """
    response = requests.get('http://maps.yandex.ru/')
    match = re.search("'secret-key':'(.*?)'", response.text)
    # noinspection PyPep8Naming
    YandexAuth = collections.namedtuple('YandexAuth', ['yandexuid', 'key'])
    return YandexAuth(key=match.group(1), yandexuid=response.cookies['yandexuid'])
