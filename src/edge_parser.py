def parse_edge_list(edges):
    if edges is None:
        return []
    return [' '.join([*edge]) for edge in edges]
