# -*- coding: utf8 -*-

from collections import defaultdict

from hamilton.euler import find_euler_cycles
from hamilton.mst import get_min_spanning_tree


def find_cycle(distance_matrix, vertex_set, start=None):
    """
    Ищет приближённый гамильтонов цикл по вершинам из vertex_set, используя расстояния, указанные в матрице
    distance_matrix.
    Если указана вершина start, то возвращаемый цикл начинается с этой вершины.
    """
    if len(vertex_set) == 1:
        return list(vertex_set)
    tree = get_min_spanning_tree(distance_matrix, vertex_set)
    adjacency_list = defaultdict(list)
    for edge in tree:
        adjacency_list[edge[0]].append(edge[1])
        adjacency_list[edge[1]].append(edge[0])
    cycles = find_euler_cycles(adjacency_list)
    path = _get_path_from_euler_cycles(cycles)
    if start is not None:
        assert start in vertex_set, start
        _turn_cycle(path, start)
    return path


def find_path(distance_matrix, vertex_set, start, finish):
    """
    Ищет приближённый гамильтонов путь по вершинам из vertex_set, используя расстояния, указанные в матрице
    distance_matrix.
    """
    if len(vertex_set) == 1:
        return list(vertex_set)
    path = find_cycle(distance_matrix, vertex_set, start)
    path.remove(finish)
    path.append(finish)
    return path


def _get_path_from_euler_cycles(cycles):
    vertex_set = set()
    path = []
    for cycle in cycles:
        for vertex in cycle:
            if vertex not in path:
                path.append(vertex)
                vertex_set.add(vertex)
    return path


def _turn_cycle(path, start):
    pos = path.index(start)
    return path[pos:] + path[:pos]