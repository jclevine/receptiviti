import networkx as nx

from src.edge_parser import parse_edge_list


class PathMaster:

    def __init__(self, edges):
        self._edges = edges
        if edges:
            self._directed_graph = nx.parse_edgelist(parse_edge_list(self._edges), data=[('weight', float)])

    def is_not_asking_for_distance_of_anything(self, path):
        return not self._edges and not path

    def no_possible_path_with_no_edges(self, path):
        return not self._edges and path

    @staticmethod
    def is_path_one_vertex(path):
        return len(path) == 1

    def calculate_distance(self, path):
        if self.is_not_asking_for_distance_of_anything(path):
            return 0.0

        if self.no_possible_path_with_no_edges(path):
            return -1

        if self.is_path_one_vertex(path):
            return 0.0 if self.is_path_one_vertex(path) and path[0] in nx.nodes(self._directed_graph) else -1
 
