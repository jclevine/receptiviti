from unittest import TestCase

from src.path_master import PathMaster


class TestQuiz(TestCase):
    edges = ['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7']
    path_master = PathMaster(edges)

    def test_1(self):
        actual = self.path_master.calculate_distance(['A', 'B', 'C'])
        self.assertEqual(9, actual)

    def test_2(self):
        actual = self.path_master.calculate_distance(['A', 'D'])
        self.assertEqual(5, actual)

    def test_3(self):
        actual = self.path_master.calculate_distance(['A', 'D', 'C'])
        self.assertEqual(13, actual)
