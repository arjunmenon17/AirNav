from __future__ import annotations
import data as dt
import math

class Airport:
    """
    An airport that represents one location or airport in the network. Each airport is connected to another airport if
    it there is a flight route that goes from one airport to another, respectively.
    Instance Attributes:
    - code:
        The 3 character code for the airport which is a unique identifier for each airport.
        This replaces the "item" attribute in the _Vertex class from lecture.
    - routes:
        A mapping containing the flights for this airport.
        Each key in the mapping is the 3 character code of a neighbour airport,
        and the corresponding value is a tuple that contains the Airport object for that airport and its corresponding distance-based weight.
        This replaces the "neighbours" attribute in the _Vertex class from lecture.

    Represenation Invariants:
    - len(self.code) == 3
    - all(self.routes[airport][0].code == airport for airport in self.routes)
    """
    code: str
    routes: dict[str, tuple[Airport, float]]

    def __init__(self, code: str) -> None:
        """
        Initializes an empty Airport
        """
        self.code = code
        self.routes = {}


class FlightNetwork:
    """
    A class for a network of flights.

    Private Instance Attributes:
        - _airports: a dictionary of all the airports in the network of flights. The key corresponds to the 3 character code of the airport.
        The corresponding value refers the the Airport object for that 3 character code.

    Representation Invariants:
        - all(code == self._airports[code].code for code in self._airports)
    """
    _airports: dict[str, Airport]

    def __init__(self):
        """
        Initializes an empty FlightNetwork 
        """
        # Initializes the list of airports in the flight network
        for airport in dt.get_airports():
            self._airports[airport] = Airport(airport)
        
        # Initializes the routes between the airports in the flight network
        for airport in self._airports:
            for destination in dt.get_destination(airport):
                weight = calculate_weight(dt.get_location(airport), destination[1])
                self._airports[airport].routes[destination[0]] = tuple(self._airports[destination[1]], weight)
    
    def find_shortest_route(self, src_airport: str, dest_airport: str) -> list[str]:
        """
        Returns the shortest route between two airports based on their distances using Djikstra's algorithm

        Preconditions:
            - len(src_airport) == 3 and len(dest_airport) == 3
        """
        # Initialize the distances and visited dictionaries
        distances = {airport_code: float('inf') for airport_code in self._airports}
        distances[src_airport] = 0
        visited = {airport_code: False for airport_code in self._airports}
        
        # Loop until all airports visited
        while not all(visited.values()):
            # Find the unvisited airport with the shortest distance so far
            current_airport = None
            for airport_code, airport_visited in visited.items():
                if not airport_visited and (current_airport is None or distances[airport_code] < distances[current_airport]):
                    current_airport = airport_code
            visited[current_airport] = True
            
            # Update the distances of the neighboring airports
            for neighbor_code, (neighbor_airport, weight) in self._airports[current_airport].routes.items():
                new_distance = distances[current_airport] + weight
                if new_distance < distances[neighbor_code]:
                    distances[neighbor_code] = new_distance
        
        # Reconstruct the shortest path using the distances
        path = [dest_airport]
        current_airport = dest_airport
        while current_airport != src_airport:
            for neighbor_code, (neighbor_airport, weight) in self._airports[current_airport].routes.items():
                if distances[neighbor_code] + weight == distances[current_airport]:
                    path.append(neighbor_code)
                    current_airport = neighbor_code
                    break
        
        return path[::-1]

def calculate_weight(first_point: tuple[float, float], second_point: tuple[float, float]) -> float:
    """
    Calculates the distance between two points on the globe based on their latitude and longitudes, and
    returns the distance in kilometers as a float.

    Preconditions:
        - all(0 <= first_point[i] <= (90 + i * 90) and 0 <= second_point[i] <= (90 + i * 90) for i in range(2))
    """
    # Calculates the latitude and longitude of each point
    lat1, lon1, = math.radians(first_point[0]), math.radians(first_point[1])
    lat2, lon2 = math.radians(second_point[0]), math.radians(second_point[1])

    # Haversine formula used to return the distance in kilometers between the two points
    a = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371 * c
