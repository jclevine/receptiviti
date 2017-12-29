from unittest import TestCase

from src.edge_parser import parse_edge_list


class TestEdgeParser(TestCase):
    def test_return_empty_list_with_no_list(self):
        actual = parse_edge_list(None)
        self.assertEqual([], actual)
