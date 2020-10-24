class Location:

    def __init__(self, address) -> None:
        """Constructor to initialize a new Location object."""
        self.address = address
        self.distance = float("inf")
        self.pre_location = None

    def __str__(self):
        return self.address


class Map:

    def __init__(self) -> None:
        """Constructor to initialize a new Map object."""
        self.location_adjacency_list = {}
        self.route_distance = {}

    def add_location(self, new_location) -> None:
        "Adds a new location key to the location adjacency list."
        self.location_adjacency_list[new_location] = []

    def add_undirected_route(self, first, second, distance=0.0) -> None:
        """Creates bi-directional routes(edges) for the locations."""
        self.add_directed_route(first, second, distance)
        self.add_directed_route(second, first, distance)

    def add_directed_route(self, origin, destination, distance=0.0) -> None:
        """
        Creates a directional route(edge) for origin to destination location.
        The distance is saved in the route_distance dictionary and
        it's adjacancy location in the location_adjacency_list dictionary.
        """
        self.route_distance[(origin, destination)] = distance
        self.location_adjacency_list[origin].append(destination)
