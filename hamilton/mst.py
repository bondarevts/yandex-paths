# -*- coding: utf8 -*-

from collections import namedtuple
from itertools import combinations

from hamilton.dsu import DSU

_Edge = namedtuple('_Edge', ['length', 'endpoints'])


def get_min_spanning_tree(distance_matrix, vertex_set):
    if len(vertex_set) == 1:
        return set()
    if len(vertex_set) == 2:
        return {tuple(vertex_set)}
    edge_set = sorted(_Edge(distance_matrix[edge[0]][edge[1]], edge) for edge in combinations(vertex_set, 2))
    dsu = DSU(vertex_set)
    tree = set()
    for edge in edge_set:
        if dsu.find(edge.endpoints[0]) != dsu.find(edge.endpoints[1]):
            tree.add(edge.endpoints)
            dsu.union(*edge.endpoints)
    return tree