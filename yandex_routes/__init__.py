# -*- coding: utf8 -*-

from collections import namedtuple
import functools

from yandex_routes import auth
from yandex_routes.exceptions import StationNotFoundException
from yandex_routes.net import json_request
from yandex_routes.route import create_route_from_response_data


class TransportType(object):
    CAR, MASS_TRANSPORT = 0b01, 0b10


def routes_request(start, finish, transport_type=TransportType.CAR, with_traffic=True):
    """
    Отправляет запрос на получение маршрута из точки start в точку finish
    Учитывает тип транспорта (личный, общественный) и влияние пробок(влияет, не влияет)
    """
    print('Request: ', start, ' -> ', finish, ', ', 'car' if transport_type == TransportType.CAR else 'mass')
    yandex_maps_url = 'http://maps.yandex.ru/'
    parameters = _get_route_request_parameters(start, finish, transport_type, with_traffic)
    response = json_request(yandex_maps_url, parameters)
    response_data = response['vpage']['data']['response']['data']['features']
    return [create_route_from_response_data(unique_route, transport_type, with_traffic)
            for unique_route in response_data]


@functools.lru_cache()
def get_subway_station_info(subway_station_name):
    """
    По неточному названию станции возвращает полное название станции метро и её координаты
    Если станция не найдена, бросает исключение
    """
    print('Request: ', subway_station_name)
    response = _subway_station_info_request(subway_station_name)
    name, coordinates = _parse_station_info_response(response)

    if not _is_station_name(name):
        raise StationNotFoundException(subway_station_name)

    name = name[6:]  # crop prefix 'метро '

    # noinspection PyPep8Naming
    StationInfo = namedtuple('StationInfo', ['name', 'coordinates'])
    return StationInfo(name, coordinates)


def _subway_station_info_request(subway_station_name):
    request_text = u"Россия, Санкт-Петербург, метро {}".format(subway_station_name)
    yandex_geo_service_url = 'http://maps.yandex.ru/services/search/1.x/search.json'
    parameters = {
        'text': request_text,
        'results': '1',
        'origin': 'maps-router',
        'lang': 'ru_RU',
        'type': 'geo',
    }
    return json_request(yandex_geo_service_url, parameters)


def _parse_station_info_response(response):
    feature = response['features'][0]
    name = feature['properties']['name']

    # noinspection PyPep8Naming
    GeoCoordinate = namedtuple('GeoCoordinate', ['latitude', 'longitude'])
    coordinates = GeoCoordinate(longitude=feature['geometry']['coordinates'][0],
                                latitude=feature['geometry']['coordinates'][1])
    return name, coordinates


def _is_station_name(name):
    return name.split()[0] == 'метро'


def _get_route_request_parameters(start, finish, transport_type, with_traffic):
    parameters = _route_request_base_parameters(start, finish)
    parameters['rtm'] = 'dtr' if with_traffic else 'atm'
    if transport_type == TransportType.MASS_TRANSPORT:
        parameters['rtt'] = 'mt'
    return parameters


def _route_request_base_parameters(start, finish):
    a = get_subway_station_info(start).coordinates
    b = get_subway_station_info(finish).coordinates
    base_parameters = {
        'rtext': u'{start.latitude},{start.longitude}~{finish.latitude},{finish.longitude}'.format(start=a, finish=b),
        'source': 'form',
        'output': 'json',
        'key': auth.get_yandex_auth_keys().key
    }
    return base_parameters
