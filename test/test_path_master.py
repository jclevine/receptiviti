from unittest import TestCase

from src.path_master import PathMaster


# TODO: jlevine - Change names to be in the domain (eg. trips, stops)
class TestPathMaster(TestCase):
    edges = ['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE10']

    def test_initialize_graph_with_no_edges(self):
        self.assertIsNotNone(PathMaster(None))

    def test_initialize_graph_with_edges(self):
        self.assertIsNotNone(PathMaster(self.edges))

    def test_calculates_0_distance_with_no_edges_and_no_vertices_specified(self):
        path_master = PathMaster(None)
        actual = path_master.calculate_distance(None)
        self.assertEqual(0.0, actual)

    def test_calculates_0_distance_with_no_edges_and_empty_vertices_specified(self):
        path_master = PathMaster(None)
        actual = path_master.calculate_distance([])
        self.assertEqual(0.0, actual)

    def test_calculates_0_distance_with_empty_edges_and_no_vertices_specified(self):
        path_master = PathMaster([])
        actual = path_master.calculate_distance(None)
        self.assertEqual(0.0, actual)

    def test_calculates_0_distance_with_empty_edges_and_empty_vertices_specified(self):
        path_master = PathMaster([])
        actual = path_master.calculate_distance([])
        self.assertEqual(0.0, actual)

    def test_returns_neg1_if_no_edges_and_any_edges_specified(self):
        path_master = PathMaster(None)
        actual = path_master.calculate_distance(['A'])
        self.assertEqual(-1, actual)

    def test_returns_neg1_if_empty_edges_and_any_edges_specified(self):
        path_master = PathMaster([])
        actual = path_master.calculate_distance(['A'])
        self.assertEqual(-1, actual)

    def test_returns_0_distance_if_only_one_existing_vertex(self):
        path_master = PathMaster(['AB3'])
        actual = path_master.calculate_distance(['A'])
        self.assertEqual(0, actual)

    # TODO: jlevine - Write validation tests/implementation for both graph input and path

    def test_returns_neg1_distance_if_only_one_non_existent_vertex(self):
        path_master = PathMaster(['AB3'])
        actual = path_master.calculate_distance(['C'])
        self.assertEqual(-1, actual)

    def test_returns_neg1_distance_if_any_vertex_does_not_exist(self):
        path_master = PathMaster(['AB3'])
        actual = path_master.calculate_distance(['A', 'C'])
        self.assertEqual(-1, actual)

    def test_returns_NO_SUCH_ROUTE_distance_if_path_does_not_exist(self):
        path_master = PathMaster(['AB3', 'CD9'])
        actual = path_master.calculate_distance(['A', 'C'])
        self.assertEqual('NO SUCH ROUTE', actual)

    def test_returns_distance_if_single_edge_exists(self):
        path_master = PathMaster(['AB3'])
        actual = path_master.calculate_distance(['A', 'B'])
        self.assertEqual(3, actual)

    def test_returns_distance_if_3_edge_path_exists(self):
        path_master = PathMaster(['AB3', 'BC10', 'CD100'])
        actual = path_master.calculate_distance(['A', 'B', 'C', 'D'])
        self.assertEqual(113, actual)

    def test_returns_NO_SUCH_ROUTE_if_path_exists_from_start_to_end_vertices_but_not_by_given_path(self):
        path_master = PathMaster(['AB3', 'AC5'])
        actual = path_master.calculate_distance(['A', 'B', 'C'])
        self.assertEqual('NO SUCH ROUTE', actual)

    def test_trip_cardinality_with_max_0_stops_is_0(self):
        path_master = PathMaster(['AB3', 'BC10'])
        actual = path_master.trip_cardinality(start='A', end='B', stop_range=[0])
        self.assertEqual(0, actual)
