import networkx as nx

from src.edge_parser import parse_tracks_into_networkx_edge_list, build_railmap, get_distance, has_route

# TODO: jlevine - Make constant for 'NO SUCH ROUTE' that can be configured?
from src.util import extend_and_return


class RouteFinder:

    def __init__(self, tracks):
        self._tracks = tracks
        if tracks:
            self._rail_map = build_railmap(tracks)

    def calculate_distance(self, route):
        # Special Cases
        if self._is_not_asking_for_distance_of_anything(route):
            return 0.0

        if self._no_possible_route_with_no_tracks(route):
            return -1

        if self._has_only_one_town(route):
            return 0.0 if route[0] in self._rail_map else -1

        # Normal Cases
        rails = self._build_rails(route)

        if self._do_some_towns_not_exist(route):
            return -1

        if not self._does_route_exist(rails):
            return 'NO SUCH ROUTE'

        return get_distance(self._rail_map, rails)

    def possible_routes(self, origin, destination, layover_range):
        layover_range = [layover_range] if type(layover_range) is not list else layover_range

        if layover_range == [0] or not has_route(self._rail_map, origin, destination):
            return 0

        all_routes = self.find_all_routes(origin, destination, layover_range)
        return len(list(all_routes))

    def find_all_routes(self, origin, destination, layover_range):
        is_out_of_range = max(layover_range) < 0
        if is_out_of_range:
            return []

        has_reached_desination_within_range = origin == destination and 0 in layover_range
        if has_reached_desination_within_range:
            return destination
        else:
            all_downstream_routes = []
            for adjacent_town in self._rail_map[origin]:
                decremented_layover_range = [i - 1 for i in layover_range]
                adjacent_town_routes = self.find_all_routes(adjacent_town, destination, decremented_layover_range)
                all_downstream_routes.extend(adjacent_town_routes)

            return [extend_and_return([origin], route) for route in all_downstream_routes]

    @staticmethod
    def _build_rails(path):
        """
        Convenience function to turn vertex list into edge tuples
        Eg.
        Input: ['A', 'B', 'C']
        Output: [('A', 'B'), ('B', 'C')]
        """
        return [tuple(path[i:i + 2]) for i in range(len(path) - 1)]

    def shortest_path_distance_but_cant_stay_here(self, origin, destination):
        if origin == destination:
            return min(
                [
                    # Distance from origin to adjacent town
                    self._rail_map.get_edge_data(origin, adjacent_town)['distance'] +
                    # Distance from that adjacent town to destination
                    nx.dijkstra_path_length(self._rail_map, adjacent_town, destination, 'distance')

                    for adjacent_town in self._rail_map[origin]
                ]
            )
        else:
            return nx.dijkstra_path_length(self._rail_map, origin, destination, 'distance')

    def count_routes(self, origin, destination, max_distance):
        # TODO: jlevine - Perf improvement by cloning if start and end are the same
        first_legs = [
            self.calculate_distance(path)
            for path in nx.all_simple_paths(self._rail_map, origin, destination)
            if self.calculate_distance(path) < max_distance
        ]

        cycle_legs = [
            self.calculate_distance(path)
            for path in nx.all_simple_paths(self._rail_map, destination, destination)
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
        return not self._tracks and not path

    def _no_possible_route_with_no_tracks(self, path):
        return not self._tracks and path

    def _does_route_exist(self, edge_tuples):
        return all([self._rail_map.has_edge(*edge) for edge in edge_tuples])

    @staticmethod
    def _has_only_one_town(path):
        return len(path) == 1

    def _do_some_towns_not_exist(self, path):
        return bool(set(path) - set(self._rail_map))
