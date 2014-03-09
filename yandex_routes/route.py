# -*- coding: utf8 -*-


class Route(object):
    def __init__(self, response_info, with_traffic, begin=None, end=None):
        duration_info = response_info['properties']['RouteMetaData']['Duration']
        self.begin, self.end = begin, end
        self.duration_text = duration_info['text']
        self.duration = duration_info['value']
        self.with_traffic = with_traffic


class CarRoute(Route):
    def __init__(self, response_info, with_traffic, begin=None, end=None):
        super().__init__(response_info, with_traffic, begin, end)
        distance_info = response_info['properties']['RouteMetaData']['Distance']
        self.distance_text = distance_info['text']
        self.distance = distance_info['value']

    def get_string_info(self):
        return 'На автомобиле, длительность {} пробок: {self.duration_text} ({self.distance_text})'.format(
            'с учётом' if self.with_traffic else 'без учёта', self=self)


class MassTransportRoute(Route):
    def __init__(self, response_info, with_traffic, begin=None, end=None):
        super().__init__(response_info, with_traffic, begin, end)

    def get_string_info(self):
        return 'На общественном транспорте, {}: {self.duration_text}' \
            .format('с учётом пробок' if self.with_traffic else 'без учёта пробок', self=self)


def create_route_from_response_data(response_info, transport_type, with_traffic):
    from yandex_routes import TransportType
    # noinspection PyPep8Naming
    ResultRoute = CarRoute if transport_type == TransportType.CAR else MassTransportRoute
    return ResultRoute(response_info, with_traffic)\
