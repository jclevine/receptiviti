from unittest import TestCase

from src.path_master import PathMaster


class TestPathMaster(TestCase):
    edges = ['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7']

    def test_initialize_graph(self):
        self.assertIsNotNone(PathMaster(self.edges))

    # def
