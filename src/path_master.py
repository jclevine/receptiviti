from itertools import chain

import networkx as nx

from src.edge_parser import parse_edge_list


# TODO: jlevine - Make constant for 'NO SUCH ROUTE' that can be configured?
class PathMaster:

    def __init__(self, edges):
        self._edges = edges
        if edges:
            self._directed_graph = nx.parse_edgelist(
                parse_edge_list(self._edges),
                data=[('weight', float)],
                create_using=nx.DiGraph()
            )

    def is_not_asking_for_distance_of_anything(self, path):
        return not self._edges and not path

    def no_possible_path_with_no_edges(self, path):
        return not self._edges and path

    def does_path_exist(self, edge_tuples):
        return all([self._directed_graph.has_edge(*edge) for edge in edge_tuples])

    @staticmethod
    def is_path_one_vertex(path):
        return len(path) == 1

    def any_vertex_does_not_exist(self, path):
        return bool(set(path) - set(nx.nodes(self._directed_graph)))

    def calculate_distance(self, path):
        # Special Cases
        if self.is_not_asking_for_distance_of_anything(path):
            return 0.0

        if self.no_possible_path_with_no_edges(path):
            return -1

        if self.is_path_one_vertex(path):
            return 0.0 if self.is_path_one_vertex(path) and path[0] in nx.nodes(self._directed_graph) else -1

        # Normal Cases
        edge_tuples = self.build_edge_tuples(path)

        if self.any_vertex_does_not_exist(path):
            return -1

        if not self.does_path_exist(edge_tuples):
            return 'NO SUCH ROUTE'

        return sum([self._directed_graph.get_edge_data(*edge)['weight'] for edge in edge_tuples])

    def trip_cardinality(self, start, end, stop_range):
        stop_range = [stop_range] if type(stop_range) is not list else stop_range

        if stop_range == [0] or not nx.has_path(self._directed_graph, start, end):
            return 0

        all_paths = self.find_all_paths(start, end, stop_range)
        return len(all_paths)

    def find_all_paths(self, start, end, stop_range):
        is_out_of_range = max(stop_range) < 0
        if is_out_of_range:
            return []

        has_reached_vertex_within_range = start == end and 0 in stop_range
        if has_reached_vertex_within_range:
            return end
        else:
            def extend_and_return(a, b):
                a.extend(b)
                return a
            downstream_paths = []
            for adj in self._directed_graph[start]:
                adj_paths = self.find_all_paths(adj, end, [i - 1 for i in stop_range])
                downstream_paths.extend(adj_paths)

            all_paths = [extend_and_return([start], path) for path in downstream_paths]
            return all_paths

    @staticmethod
    def build_edge_tuples(path):
        return [tuple(path[i:i + 2]) for i in range(len(path) - 1)]
