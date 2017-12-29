from unittest import TestCase

from src.path_master import PathMaster


class TestPathMaster(TestCase):
    edges = ['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7']

    def test_initialize_graph_with_no_edges(self):
        self.assertIsNotNone(PathMaster(None))

    def test_initialize_graph_with_edges(self):
        self.assertIsNotNone(PathMaster(self.edges))

    def test_initialize_graph(self):
        self.assertIsNotNone(PathMaster(self.edges))

    def test_calculates_0_distance_with_no_edges_and_no_vertices_specified(self):
        path_master = PathMaster(None)
        actual = path_master.calculate_distance(None)
        self.assertEqual(0.0, actual)

    def test_calculates_0_distance_with_no_edges_and_empty_vertices_specified(self):
        path_master = PathMaster(None)
        actual = path_master.calculate_distance([])
        self.assertEqual(0.0, actual)
