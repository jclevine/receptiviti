import networkx as nx


def parse_tracks_into_networkx_edge_list(tracks):
    """
    Parses track list into a NetworkX compatible edge list
    Note: Cities can only have 1 character as its name
    :param tracks: List of tracks in format [CITY][CITY][DISTANCE]
    :return: List of edges, including distance
    Eg.
    Input: ['AB1', 'BC5']
    Output: [ 'A B 1', 'B C 5']
    """
    if tracks is None:
        return []
    return [' '.join([track[0:1], track[1:2], track[2:]]) for track in tracks]


def build_railmap(tracks):
    return nx.parse_edgelist(
        parse_tracks_into_networkx_edge_list(tracks),
        data=[('distance', float)],
        create_using=nx.DiGraph()
    )


def get_distance(railmap, rails):
    return sum([railmap.get_edge_data(*rail)['distance'] for rail in rails])


def has_route(railmap, origin, destination):
    return nx.has_path(railmap, origin, destination)
