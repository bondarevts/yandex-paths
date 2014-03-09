#!/usr/bin/env python3
# -*- coding: utf8 -*-

import route_processor


def get_time_str(duration):
    duration //= 60
    minutes = int(duration % 60)
    hours = int(duration // 60)
    if hours == 0:
        return '{} мин.'.format(minutes)
    return '{} ч. {} мин.'.format(hours, minutes)


def main():
    stations = input('Введите через запятую список станций, которые нужно посетить: ')
    station_list = stations.split(',')
    if len(station_list) == 1:
        print('Всего одна станция, можно никуда не ехать')
    else:
        all_duration = 0
        for route in route_processor.calc_path(station_list):
            print('{} -> {}: {}'.format(route.begin, route.end, route.get_string_info()))
            all_duration += route.duration
        print('Весь путь: {}'.format(get_time_str(all_duration)))


main()
# Пример ввода:
# автово, проспект просвещения, петроградская, ветеранов, ленинский проспект, Ладожская, Политехническая
