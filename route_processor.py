# -*- coding: utf8 -*-

from collections import namedtuple
from itertools import combinations
import numpy as np

import yandex_routes
import hamilton
from yandex_routes import TransportType, route


def calc_path(station_list, with_traffic=False):
    path_finder = PathFinder(station_list, with_traffic=with_traffic)
    return path_finder.get_path_from(station_list[0], station_list[-1])


class PathFinder():
    def __init__(self, station_list, with_traffic):
        self.station_list = station_list
        self.size = len(station_list)
        self.with_traffic = with_traffic

        # noinspection PyPep8Naming
        TransportTuple = namedtuple('TransportTuple', ['car', 'mass'])
        matrix_size = (self.size, self.size)
        self.durations = TransportTuple(np.zeros(matrix_size), np.zeros(matrix_size))
        self.routes = TransportTuple(np.empty(matrix_size, dtype=route.Route), np.empty(matrix_size, dtype=route.Route))
        self._fill_duration_matrices()

    def get_path_from(self, start, finish):
        assert start in self.station_list
        assert finish in self.station_list

        if len(self.station_list) == 2:
            min_route = min([self.routes.car[0][1], self.routes.mass[0][1]], key=lambda r: r.duration)
            min_route.begin = self.station_list[0]
            min_route.end = self.station_list[1]
            return [min_route]

        # noinspection PyPep8Naming
        PathInfo = namedtuple('PathInfo', ['car_path', 'mass_cycle', 'touch'])
        min_duration = float('inf')
        min_path_info = None

        start, finish = self.station_list.index(start), self.station_list.index(finish)

        for car_set, mass_set, touch in self._vertex_set_generator():
            if finish not in car_set or start not in car_set:
                continue
            car_path = hamilton.find_path(self.durations.car, car_set, start, finish)
            mass_cycle = hamilton.find_cycle(self.durations.mass, mass_set, touch)
            if len(mass_cycle) != 1:
                mass_cycle.append(mass_cycle[0])

            duration = self._calc_duration(car_path, self.routes.car) + self._calc_duration(mass_cycle, self.routes.mass)
            if duration < min_duration:
                min_duration = duration
                min_path_info = PathInfo(car_path=car_path, mass_cycle=mass_cycle, touch=touch)
        return self._create_routes_path(min_path_info)

    def get_min_route(self, start, finish, transport_type):
        return min(yandex_routes.routes_request(start, finish,
                                                transport_type, self.with_traffic), key=lambda r: r.duration)

    def _vertex_set_generator(self):
        station_set = set(range(self.size))
        # выберем вершину касания
        for touch_vertex in range(self.size):
            # выребем размер множества вершин, которые нужно объехать на автомобиле
            for car_set_size in range(self.size - 1):
                # выберем множество вершин, которые объедем на автомобиле
                for car_set in combinations(range(self.size), car_set_size):
                    car_set = set(car_set)
                    mass_set = station_set.difference(car_set)
                    car_set.add(touch_vertex)
                    mass_set.add(touch_vertex)
                    yield car_set, mass_set, touch_vertex

    def _create_routes_path(self, path_info):
        path = []
        touch_pos = path_info.car_path.index(path_info.touch)
        self._update_path(path, path_info.car_path, self.routes.car, end=touch_pos)
        self._update_path(path, path_info.mass_cycle, self.routes.mass)
        self._update_path(path, path_info.car_path, self.routes.car, begin=touch_pos)
        return path

    def _fill_duration_matrices(self):
        for i in range(self.size):
            for j in range(i):
                self._fill_routes(i, j, self.routes.car, self.durations.car, TransportType.CAR)
                self._fill_routes(i, j, self.routes.mass, self.durations.mass, TransportType.MASS_TRANSPORT)

    def _fill_routes(self, i, j, routes, durations, transport_type):
        routes[i][j] = self.get_min_route(self.station_list[i], self.station_list[j], transport_type)
        routes[j][i] = self.get_min_route(self.station_list[j], self.station_list[i], transport_type)
        durations[i][j] = durations[j][i] = sum((routes[i][j].duration,
                                                 routes[j][i].duration)) / 2.0

    def _update_path(self, routes, vertex_path, routes_matrix, begin=None, end=None):
        if begin is None:
            begin = 0
        if end is None:
            end = len(vertex_path)
        if end - begin < 2:
            return
        for i in range(begin + 1, end):
            segment = routes_matrix[vertex_path[i-1]][vertex_path[i]]
            segment.begin = self.station_list[vertex_path[i-1]]
            segment.end = self.station_list[vertex_path[i]]
            routes.append(segment)

    # noinspection PyMethodMayBeStatic
    def _calc_duration(self, path, routes):
        shift_path = iter(path)
        next(shift_path)
        return sum(routes[start][end].duration for start, end in zip(path, shift_path))
