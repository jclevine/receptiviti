import networkx as nx

from src.networkx_helper import build_railmap, get_distance, has_route

from src.util import extend_and_return


class RouteFinder:
    NO_SUCH_ROUTE = 'NO SUCH ROUTE'

    def __init__(self, tracks, no_route='NO SUCH ROUTE'):
        self.NO_SUCH_PROPERTY = no_route
        self._tracks = tracks
        if tracks:
            self._railmap = build_railmap(tracks)

    def calculate_distance(self, route):
        # Special Cases
        if self._is_not_asking_for_distance_of_anything(route):
            return 0.0

        if self._no_possible_route_with_no_tracks(route):
            return -1

        if self._has_only_one_town(route):
            return 0.0 if route[0] in self._railmap else -1

        # Normal Cases
        rails = self._build_rails(route)

        if self._do_some_towns_not_exist(route):
            return -1

        if not self._does_route_exist(rails):
            return self.NO_SUCH_ROUTE

        return get_distance(self._railmap, rails)

    def possible_route_count(self, origin, destination, layover_range):
        layover_range = [layover_range] if type(layover_range) is not list else layover_range

        if layover_range == [0] or not has_route(self._railmap, origin, destination):
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
            for adjacent_town in self._railmap[origin]:
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
                    self._railmap.get_edge_data(origin, adjacent_town)['distance'] +
                    # Distance from that adjacent town to destination
                    nx.dijkstra_path_length(self._railmap, adjacent_town, destination, 'distance')

                    for adjacent_town in self._railmap[origin]
                ]
            )
        else:
            return nx.dijkstra_path_length(self._railmap, origin, destination, 'distance')

    def count_routes(self, origin, destination, distance_limit):
        first_legs = self._simple_route_distances_with_max_distance(origin, destination, distance_limit)
        cycle_legs = self._simple_route_distances_with_max_distance(origin, destination, distance_limit) \
            if origin != destination else first_legs

        route_count = len(first_legs)

        for route_distance in first_legs:
            route_count += \
                self._route_combo_count_within_distance_limit(cycle_legs, distance_limit - route_distance)
        return route_count

    def _simple_route_distances_with_max_distance(self, origin, destination, max_distance):
        return [
            self.calculate_distance(route)
            for route in nx.all_simple_paths(self._railmap, origin, destination)
            if self.calculate_distance(route) < max_distance
        ]

    def _route_combo_count_within_distance_limit(self, potential_route_distances, distance_limit):
        total = 0
        for potential_route_distance in potential_route_distances:
            if potential_route_distance < distance_limit:
                updated_distance_limit = distance_limit - potential_route_distance
                total += (1 +
                          self._route_combo_count_within_distance_limit(
                              potential_route_distances, updated_distance_limit
                          ))
        return total

    def _is_not_asking_for_distance_of_anything(self, route):
        return not self._tracks and not route

    def _no_possible_route_with_no_tracks(self, route):
        return not self._tracks and route

    def _does_route_exist(self, rails):
        return all([self._railmap.has_edge(*edge) for edge in rails])

    @staticmethod
    def _has_only_one_town(route):
        return len(route) == 1

    def _do_some_towns_not_exist(self, route):
        return bool(set(route) - set(self._railmap))
