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
            self._edge_attributes = nx.get_edge_attributes(self._directed_graph, 'weight')

    def is_not_asking_for_distance_of_anything(self, path):
        return not self._edges and not path

    def no_possible_path_with_no_edges(self, path):
        return not self._edges and path

    def does_path_exist(self, edge_tuples):
        return all([edge in self._edge_attributes for edge in edge_tuples])

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

        return sum([self._edge_attributes[edge] for edge in edge_tuples])

    def trip_cardinality(self, start, end, stop_range):
        if stop_range == [0] or not nx.has_path(self._directed_graph, start, end):
            return 0

    @staticmethod
    def build_edge_tuples(path):
        return [tuple(path[i:i + 2]) for i in range(len(path) - 1)]
