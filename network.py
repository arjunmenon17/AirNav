"""CSC111 Winter 2023 Course Project: AirNav

Module Information: network.py
===============================

This Python module contains the graph and vertex classes for the flight network
represented by airports and flight networks. It contains the graph constructor/initializer
methods, the shortest path finder algorithm between airports, and a function that
computes the distance between two points on Earth.

Copyright and Usage Information
===============================

This file is provided solely for the submission of the CSC111 Course Project and to be
used by instructors and TAs while marking and assessing this project.

This file is Copyright (c) 2023 Arjun Menon, Azlan Naeem, Hadi Naqvi, and Rohan Regi.
"""
from __future__ import annotations
# from python_ta.contracts import check_contracts
import math
import heapq
from data import get_airports, get_location, get_destinations


# @check_contracts
class Airport:
    """
    An airport that represents one location or airport in the network. Each airport is connected to another airport
    if it there is a flight route that goes from one airport to another, respectively. Instance Attributes: - code:
    The 3 character code for the airport which is a unique identifier for each airport. This replaces the "item"
    attribute in the _Vertex class from lecture. - routes: A mapping containing the flights for this airport. Each
    key in the mapping is the 3 character code of a neighbour airport, and the corresponding value is a tuple that
    contains the Airport object for that airport and its corresponding distance-based weight. This replaces the
    "neighbours" attribute in the _Vertex class from lecture. - name: The name of the airport - country: The country
    the airport is in - city: The city the airport is in

    Represenation Invariants:
        - len(self.code) == 3
        - all(self.routes[airport][0].code == airport for airport in self.routes)
    """
    code: str
    name: str
    country: str
    city: str
    routes: dict[str, tuple[Airport, float]]

    def __init__(self, code: str, airport_name: str, country: str, city: str) -> None:
        """
        Initializes an airport with its corresponding metadata
        """
        self.code = code
        self.name = airport_name
        self.country = country
        self.city = city
        self.routes = {}


# @check_contracts
class FlightNetwork:
    """
    A class for a network of flights.

    Private Instance Attributes: - _airports: a dictionary of all the airports in the network of flights. The key
    corresponds to the 3 character code of the airport. The corresponding value refers the Airport object for
    that 3 character code.

    Representation Invariants:
        - all(code == self._airports[code].code for code in self._airports)
    """
    _airports: dict[str, Airport]

    def __init__(self) -> None:
        """
        Initializes an empty FlightNetwork
        """
        # Initializes the list of airports in the flight network
        self._airports = {}
        for airport in get_airports():
            self._airports[airport[0]] = Airport(airport[0], airport[1], airport[2], airport[3])

        # Initializes the routes between the airports in the flight network
        for airport in self._airports:
            destinations = get_destinations(airport)
            for destination in destinations:
                weight = calculate_weight(get_location(airport), destination[1])
                self._airports[airport].routes[destination[0]] = (self._airports[destination[0]], weight)

    # @check_contracts
    def find_shortest_route(self, src_airport: str, dest_airport: str) -> list[Airport]:
        """
        Returns the shortest route as a list of airports between two airports based on their distances using
        Djikstra's algorithm

        Preconditions:
            - len(src_airport) == 3 and len(dest_airport) == 3
        """
        # Check if there is a direct flight between source and destination airports
        if dest_airport in self._airports[src_airport].routes:
            return [self._airports[src_airport], self._airports[dest_airport]]

        # Set up initial distances and previous airports
        distances = {code: float("inf") for code in self._airports}
        distances[src_airport] = 0
        prev_airports = {code: None for code in self._airports}

        # Set up heap (priority queue) with the initial vertex
        heap = [(0, src_airport)]

        # Run Djikstra's algorithm
        while heap:
            # Pop vertex with smallest distance so far
            curr_distance, curr_vertex = heapq.heappop(heap)

            # Check if we've reached the destination vertex
            if curr_vertex == dest_airport:
                # Reconstruct path and return it
                path = []
                while curr_vertex is not None:
                    path.append(self._airports[curr_vertex])
                    curr_vertex = prev_airports[curr_vertex]
                return path[::-1]

            # Check if we've already found a better path to this vertex
            if curr_distance > distances[curr_vertex]:
                continue

            # Look at all neighbouring vertices and update their distances if necessary
            for neighbour_code, (_, weight) in self._airports[curr_vertex].routes.items():
                distance_to_neighbour = curr_distance + weight
                if distance_to_neighbour < distances[neighbour_code]:
                    distances[neighbour_code] = distance_to_neighbour
                    prev_airports[neighbour_code] = curr_vertex
                    heapq.heappush(heap, (distance_to_neighbour, neighbour_code))

        # If we reach this point, there is no path between the two vertices
        return []


# @check_contracts
def calculate_weight(first_point: tuple[float, float], second_point: tuple[float, float]) -> float:
    """
    Calculates the distance between two points on the globe based on their latitude and longitudes, and
    returns the distance in kilometers as a float.

    Preconditions:
        - all(0 <= first_point[i] <= (90 + i * 90) and 0 <= second_point[i] <= (90 + i * 90) for i in range(2))
    """
    lon1, lat1, lon2, lat2 = map(math.radians, [first_point[0], first_point[1], second_point[0], second_point[1]])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    earth_radius = 6371
    return c * earth_radius


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['data', 'math', 'heapq'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
