from unittest import TestCase

from src.networkx_helper import parse_tracks_into_networkx_edge_list


class TestNetworkxHelper(TestCase):
    def test_returns_empty_list_with_no_track_list(self):
        actual = parse_tracks_into_networkx_edge_list(None)
        self.assertEqual([], actual)

    def test_returns_empty_list_with_empty_track_list(self):
        actual = parse_tracks_into_networkx_edge_list([])
        self.assertEqual([], actual)

    def test_returns_edge_list_with_one_track(self):
        actual = parse_tracks_into_networkx_edge_list(['AB3'])
        self.assertEqual(['A B 3'], actual)

    def test_returns_edge_list_with_three_tracks(self):
        actual = parse_tracks_into_networkx_edge_list(['AB3', 'BC4', 'CD8'])
        self.assertEqual(['A B 3', 'B C 4', 'C D 8'], actual)
