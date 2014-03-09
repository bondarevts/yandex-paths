def find_euler_cycles(adjacency_list):
    visited_edges = set()
    edges_count = sum(len(edges) for edges in adjacency_list.values())
    cycles = []
    while len(visited_edges) != edges_count:
        for vertex in adjacency_list.keys():
            if _have_not_visited_edge(adjacency_list, visited_edges, vertex):
                start = vertex
                break
        else:
            raise Exception('Algorithm error: any vertex must have not visited edge')
        cycles.append(_find_cycle(adjacency_list, visited_edges, start))
    return cycles


def _get_next_edge(adjacency_list, visited_edges, start):
    for end in adjacency_list[start]:
        if (start, end) not in visited_edges:
            return end


def _find_cycle(adjacency_list, visited_edges, start):
    current, end, cycle = start, None, [start]
    while end != start:
        end = _get_next_edge(adjacency_list, visited_edges, current)
        visited_edges.add((current, end))
        cycle.append(end)
        current = end
    return cycle


def _have_not_visited_edge(adjacency_list, visited_edges, vertex):
    return not all((vertex, end) in visited_edges for end in adjacency_list[vertex])