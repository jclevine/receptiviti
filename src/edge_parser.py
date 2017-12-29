def parse_edge_list(edges):
    if edges is None:
        return []
    return [' '.join([edge[0:1], edge[1:2], edge[2:]]) for edge in edges]
