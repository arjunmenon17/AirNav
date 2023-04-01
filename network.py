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
    - name:
        The name of the airport
    - country:
        The country the airport is in
    - city:
        The city the airport is in

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
        self._airports = {}
        for airport in dt.get_airports():
            self._airports[airport[0]] = Airport(airport[0], airport[1], airport[2], airport[3])
        
        # Initializes the routes between the airports in the flight network
        for airport in self._airports:
            for destination in dt.get_destination(airport):
                weight = calculate_weight(dt.get_location(airport), destination[1])
                self._airports[airport].routes[destination[0]] = tuple(self._airports[destination[1]], weight)
    

    def find_shortest_route(self, src_airport: str, dest_airport: str) -> list[Airport]:
        """
        Returns the shortest route as a list of airports between two airports based on their distances using Djikstra's algorithm

        Preconditions:
            - len(src_airport) == 3 and len(dest_airport) == 3
        """
        # Initialize the distance dictionary with infinite distances to all airports except the source
        dist = {airport: math.inf for airport in self._airports}
        dist[src_airport] = 0
        
        # Initialize the priority queue with the source airport
        queue = [(0, self._airports[src_airport])]
        
        # Initialize the visited set
        visited = set()
        
        while len(queue) != 0:
            # Get the airport with the smallest distance from the priority queue
            curr_dist, curr_airport = min(queue, key=lambda x: x[0])
            queue.remove((curr_dist, curr_airport))
            
            # Check if the airport has been visited
            if curr_airport.code in visited:
                continue
            
            # Add the airport to the visited set
            visited.add(curr_airport.code)
            
            # Check if the current airport is the destination, and then return the path
            if curr_airport.code == dest_airport:
                path = [curr_airport]
                while path[-1].code != src_airport:
                    path.append(dist[path[-1].code][1])
                return [self._airports[airport_code] for airport_code in path[::-1]]
            
            # Update the distances to the neighbours of the current airport
            for neighbour_code, (neighbour, weight) in curr_airport.routes.items():
                if neighbour.code not in visited:
                    new_dist = curr_dist + weight
                    if new_dist < dist[neighbour_code]:
                        dist[neighbour_code] = new_dist
                        queue.append((new_dist, neighbour))
        
        # If the queue is empty then there is no path (empty path is returned)
        return []

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
