import data.py as dt
import math

class Route:
    """
    A route (or "edge") connecting two aiports in a flight network.

    Instance Attributes:
    - source: the airport that the flight route starts at or flys out from
    - destination: the airport that the flight route ends at or lands.
    - weight: the weight of the flight based on the distance between source and destination
    """
    source: tuple[str, tuple[float, float]]
    destination: tuple[str, tuple[float, float]]
    weight: float

    def __init__(self, source: tuple[str, tuple[float, float]], destination: tuple[str, tuple[float, float]]) -> None:
        """
        Docstring here
        """
        self.source = source
        self.destination = destination
        self.weight =  self.calculate_weight()

    def calculate_weight(self) -> float:
        """
        Calculates the distance between two points on the globe based on their latitude and longitudes, and
        returns the distance in kilometers as a float.
        """
        first_point = self.source[1]
        second_point = self.destination[1]

        lat1, lon1, = math.radians(first_point[0]), math.radians(first_point[1])
        lat2, lon2 = math.radians(second_point[0]), math.radians(second_point[1])

        a = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = 6371 * c
        return distance        


class Airport:
    """
    An airport that represents one location or airport in the network. Each airport is connected to another airport if
    it there is a flight route that goes from one airport to another, respectively.

    Instance Attributes:
    - code:
        The 3 character code for the airport which is a unique identifier for each airport.
        This replaces the "item" attribute in the _Vertex class from lecture.
    - flights:
        A mapping containing the flights for this airport.
        Each key in the mapping is the 3 character code of a neighbour airport,
        and the corresponding value is the route or flight path leading to that airport.
        This replaces the "neighbours" attribute in the _Vertex class from lecture.

    """
    code: str
    flights: list[Route]

    def __init__(self, cd) -> None:
        self.code = cd
        self.flights = []
        self.load_routes(dt.get_location(cd))

    def load_routes(self, source_address: tuple(float, float)) -> list[Route]:
        for destination in dt.get_destinations(self.code):
            self.flights.append(Route((self.code, source_address), (destination[0], destination[1])))


class FlightNetwork:
    """
    A class for a network of flights.

    Instance Attributes:
    - airports: a list of all the airports in the network of flights.
    """
    airports: list[Airport]
    
    def __init__(self):
        pass
