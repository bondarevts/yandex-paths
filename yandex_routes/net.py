# -*- coding: utf8 -*-

import json
import warnings

import requests

from yandex_routes import auth
from yandex_routes.exceptions import ResponseStatusWarning


def json_request(url, parameters):
    """
    Выполняет запрос к ресурсу, ожидая возвращения строки в формате json
    Позволяет сохранить полученные данные в файле
    """
    response = send_yandex_request(url, parameters)
    return json.loads(response.text)


def send_yandex_request(url, parameters):
    """
    Отправляет запрос, выставив cookie для yandex
    """
    cookie = {
        'yandexuid': auth.get_yandex_auth_keys().yandexuid,
    }
    response = requests.get(url, params=parameters, cookies=cookie)

    if response.status_code != 200:
        warnings.warn(u'response status: {}'.format(response.status_code), ResponseStatusWarning)

    return response

