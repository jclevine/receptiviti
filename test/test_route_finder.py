from unittest import TestCase

from src.route_finder import RouteFinder


# TODO: jlevine - Change names to be in the domain (eg. trips, stops)
class TestPathMaster(TestCase):
    tracks = ['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE10']

    def test_initialize_route_finder_with_no_tracks(self):
        self.assertIsNotNone(RouteFinder(None))

    def test_initialize_route_finder_with_tracks(self):
        self.assertIsNotNone(RouteFinder(self.tracks))

    def test_calculates_0_distance_with_no_tracks_and_no_route_specified(self):
        path_master = RouteFinder(None)
        actual = path_master.calculate_distance(None)
        self.assertEqual(0.0, actual)

    def test_calculates_0_distance_with_no_tracks_and_empty_route_specified(self):
        path_master = RouteFinder(None)
        actual = path_master.calculate_distance([])
        self.assertEqual(0.0, actual)

    def test_calculates_0_distance_with_empty_tracks_and_no_route_specified(self):
        path_master = RouteFinder([])
        actual = path_master.calculate_distance(None)
        self.assertEqual(0.0, actual)

    def test_calculates_0_distance_with_empty_tracks_and_empty_route_specified(self):
        path_master = RouteFinder([])
        actual = path_master.calculate_distance([])
        self.assertEqual(0.0, actual)

    def test_returns_neg1_if_no_rails_and_any_route_specified(self):
        path_master = RouteFinder(None)
        actual = path_master.calculate_distance(['A'])
        self.assertEqual(-1, actual)

    def test_returns_neg1_if_empty_rails_and_any_route_specified(self):
        path_master = RouteFinder([])
        actual = path_master.calculate_distance(['A'])
        self.assertEqual(-1, actual)

    def test_returns_0_distance_if_only_one_town_in_route(self):
        path_master = RouteFinder(['AB3'])
        actual = path_master.calculate_distance(['A'])
        self.assertEqual(0, actual)

    # TODO: jlevine - Write validation tests/implementation for both graph input and path

    def test_returns_neg1_distance_if_only_calculating_one_non_existent_town_route(self):
        path_master = RouteFinder(['AB3'])
        actual = path_master.calculate_distance(['C'])
        self.assertEqual(-1, actual)

    def test_returns_neg1_distance_if_any_town_in_route_does_not_exist(self):
        path_master = RouteFinder(['AB3'])
        actual = path_master.calculate_distance(['A', 'C'])
        self.assertEqual(-1, actual)

    def test_returns_NO_SUCH_ROUTE_distance_if_route_does_not_exist(self):
        path_master = RouteFinder(['AB3', 'CD9'])
        actual = path_master.calculate_distance(['A', 'C'])
        self.assertEqual('NO SUCH ROUTE', actual)

    def test_returns_distance_if_calculating_one_existing_rail(self):
        path_master = RouteFinder(['AB3'])
        actual = path_master.calculate_distance(['A', 'B'])
        self.assertEqual(3, actual)

    def test_returns_distance_if_calculating_existing_size_3_rail_route(self):
        path_master = RouteFinder(['AB3', 'BC10', 'CD100'])
        actual = path_master.calculate_distance(['A', 'B', 'C', 'D'])
        self.assertEqual(113, actual)

    def test_returns_NO_SUCH_ROUTE_if_route_exists_from_origin_to_destination_but_not_by_given_route(self):
        path_master = RouteFinder(['AB3', 'AC5'])
        actual = path_master.calculate_distance(['A', 'B', 'C'])
        self.assertEqual('NO SUCH ROUTE', actual)

    def test_possible_route_count_with_range_of_0_layovers_is_0(self):
        path_master = RouteFinder(['AB3', 'BC10'])
        actual = path_master.possible_route_count(origin='A', destination='B', layover_range=[0])
        self.assertEqual(0, actual)

    def test_possible_route_count_with_range_of_1_layover_is_0_if_route_does_not_exist(self):
        path_master = RouteFinder(['AB3', 'BC10', 'DA4'])
        actual = path_master.possible_route_count(origin='A', destination='D', layover_range=[1])
        self.assertEqual(0, actual)

    def test_possible_route_count_with_range_of_1_layover_is_1_if_route_exists(self):
        path_master = RouteFinder(['AB3'])
        actual = path_master.possible_route_count(origin='A', destination='B', layover_range=[1])
        self.assertEqual(1, actual)

    def test_possible_route_count_is_0_if_all_routes_out_of_range(self):
        path_master = RouteFinder(['AB3'])
        actual = path_master.possible_route_count(origin='A', destination='B', layover_range=[2])
        self.assertEqual(0, actual)

    def test_possible_route_count_is_1_if_layover_range_is_1_if_path_exists(self):
        path_master = RouteFinder(['AB3'])
        actual = path_master.possible_route_count(origin='A', destination='B', layover_range=1)
        self.assertEqual(1, actual)

    def test_possible_route_count_is_2_if_layover_count_is_1to2_and_there_are_2_routes_in_range(self):
        path_master = RouteFinder(['AB3', 'AC10', 'CB1'])
        actual = path_master.possible_route_count(origin='A', destination='B', layover_range=[1, 2])
        self.assertEqual(2, actual)

    def test_possible_route_count_is_2_if_layover_count_is_1to2_and_there_are_only_2_routes_in_range(self):
        path_master = RouteFinder(['AB3', 'AC10', 'CB1', 'CD1', 'DB1'])
        actual = path_master.possible_route_count(origin='A', destination='B', layover_range=[1, 2])
        self.assertEqual(2, actual)

    def test_find_all_routes_for_railmap_with_one_rail(self):
        path_master = RouteFinder(['AB3'])
        self.assertEqual([['A', 'B']], path_master.find_all_routes('A', 'B', [1]))

    def test_find_all_paths_for_railmap_with_3_rails(self):
        path_master = RouteFinder(['AB3', 'AC10', 'CB1'])
        self.assertEqual([['A', 'B'], ['A', 'C', 'B']], path_master.find_all_routes('A', 'B', [1, 2]))
