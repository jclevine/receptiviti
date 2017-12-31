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

    def test_4(self):
        actual = self.path_master.calculate_distance(['A', 'E', 'B', 'C', 'D'])
        self.assertEqual(22, actual)

    def test_5(self):
        actual = self.path_master.calculate_distance(['A', 'E', 'D'])
        self.assertEqual('NO SUCH ROUTE', actual)

    def test_6(self):
        actual = self.path_master.trip_cardinality('C', 'C', list(range(1, 4)))
        self.assertEqual(2, actual)

    def test_7(self):
        actual = self.path_master.trip_cardinality('A', 'C', 4)
        self.assertEqual(3, actual)

    def test_8(self):
        actual = self.path_master.shortest_path_distance('A', 'C')
        self.assertEqual(9, actual)

    def test_9(self):
        actual = self.path_master.shortest_path_distance('B', 'B')
        self.assertEqual(9, actual)

    def test_10(self):
        actual = self.path_master.count_routes('C', 'C', 30)
        self.assertEqual(7, actual)
