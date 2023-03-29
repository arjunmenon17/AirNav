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
    flights: dict[str, Route]


class Route:
    """
    A route (or "edge") connecting two aiports in a flight network.

    Instance Attributes:
    - source: the airport that the flight route starts at or flys out from
    - destination: the airport that the flight route ends at or lands.
    """
    source: str
    destination: str


class FlightNetwork:
    """
    A class for a network of flights.

    Instance Attributes:
    - airports: a list of all the airports in the network of flights.
    """
    airports: list[Airport]
