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

    def calculate_distance(self, path):
        # Special Cases
        if self._is_not_asking_for_distance_of_anything(path):
            return 0.0

        if self._no_possible_path_with_no_edges(path):
            return -1

        if self._is_path_one_vertex(path):
            return 0.0 if path[0] in nx.nodes(self._directed_graph) else -1

        # Normal Cases
        edge_tuples = self._build_edge_tuples(path)

        if self._any_vertex_does_not_exist(path):
            return -1

        if not self._does_path_exist(edge_tuples):
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
    def _build_edge_tuples(path):
        """
        Convenience function to turn vertex list into edge tuples
        Eg.
        Input: ['A', 'B', 'C']
        Output: [('A', 'B'), ('B', 'C')]
        """
        return [tuple(path[i:i + 2]) for i in range(len(path) - 1)]

    def shortest_path_distance(self, start, end):
        if start == end:
            return min([nx.dijkstra_path_length(self._directed_graph, one_away, end, 'weight') +
                        self._directed_graph.get_edge_data(start, one_away)['weight'] for one_away in
                        self._directed_graph[start]])
        return nx.dijkstra_path_length(self._directed_graph, start, end, 'weight')

    def count_routes(self, start, end, max_distance):
        # TODO: jlevine - Perf improvement by cloning if start and end are the same
        first_legs = [
            self.calculate_distance(path)
            for path in nx.all_simple_paths(self._directed_graph, start, end)
            if self.calculate_distance(path) < max_distance
        ]

        cycle_legs = [
            self.calculate_distance(path)
            for path in nx.all_simple_paths(self._directed_graph, end, end)
            if self.calculate_distance(path) < (max_distance - min(first_legs))
        ]

        count = len(first_legs)

        for path in first_legs:
            count += self.max_dfs(cycle_legs, max_distance - path)
        return count

    def max_dfs(self, potential_paths, max_distance):
        total = 0
        for path in potential_paths:
            if path < max_distance:
                total += 1 + self.max_dfs(potential_paths, max_distance - path)
        return total

    def _is_not_asking_for_distance_of_anything(self, path):
        return not self._edges and not path

    def _no_possible_path_with_no_edges(self, path):
        return not self._edges and path

    def _does_path_exist(self, edge_tuples):
        return all([self._directed_graph.has_edge(*edge) for edge in edge_tuples])

    @staticmethod
    def _is_path_one_vertex(path):
        return len(path) == 1

    def _any_vertex_does_not_exist(self, path):
        return bool(set(path) - set(nx.nodes(self._directed_graph)))
