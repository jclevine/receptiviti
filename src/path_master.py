class PathMaster:

    def __init__(self, edges):
        self._edges = edges

    def is_not_asking_for_distance_of_anything(self, path):
        return not self._edges and not path

    # TODO: jlevine - Could make it more "clever" possibly
    def validate_edges_and_vertices(self, path):
        if self._edges and not path:
            raise TypeError('No path specified: {}'.format(path))
        elif not self._edges and path:
            raise TypeError('No edges specified in path master: {}'.format(self._edges))

    def calculate_distance(self, path):
        if self.is_not_asking_for_distance_of_anything(path):
            return 0.0
        self.validate_edges_and_vertices(path)
