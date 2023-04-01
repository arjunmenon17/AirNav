import os
import pandas as pd
import numpy as np
import network

def get_dataframe1(csv_file: str) -> pd.DataFrame:
    """
    Extracts the 3 character code for an airport along with its given geographical location in terms of latitude and longitude.

    Preconditions:
        - csv_file in os.getcwd()
        - csv_file is a valid dataset
    """
    df_airports = pd.read_csv('airports.csv')
    df = df_airports.dropna() # Drops rows with NaN values
    df1 = df[['3 Char Code', 'Lat', 'Long', 'Airport Name', 'City', 'Country']]

    return df1
    
def get_dataframe2(csv_file: str) -> pd.DataFrame:  # list[list[str, str]]
    """
    Returns a nested list of real life flight paths. Each list inside the original list is a single flight path 
    with a source airport and a destination airport.

    Preconditions:
        - csv_file in os.getcwd()
        - csv_file is a valid dataset
    """
    route_cols = ['Airline', 'Airline ID', 'Source', 'Source Airport ID',
                'Dest', 'Dest Airport ID', 'Codeshare', 'Stops', 'equipment'] # Sets new column names for the dataframe
    routes_df = pd.read_csv('flight_routes.csv', names=route_cols, skiprows=1, low_memory=False) # Has too many columns

    df = routes_df.dropna() # Drops rows with NaN values
    df2 = df[['Source', 'Dest']]

    return df2

def get_location(airport_key: str) -> tuple[float, float]:
    """
    Returns the latitude/longtidude of a given airport.

    Preconditions:
        - len(airport_key) == 3
    """
    df_airports = get_dataframe1('airports.csv')
    for ind in df_airports.index:
        if df_airports['3 Char Code'][ind] == airport_key:
            return (df_airports['Lat'][ind], df_airports['Long'][ind])


def get_destinations(airport_key: str) -> list[tuple[str, tuple[float, float]]]:
    """
    Returns the list of destinations with their airport codes and latitude/longitude for the given airport.

    Preconditions:
        - len(airport_key) == 3
    """
    df_routes = get_dataframe2('flight_routes.csv')
    df_airports = get_dataframe1('airports.csv')
    for ind in df_routes.index:
        if df_routes['3 Char Code'][ind] == airport_key:
            return [(route[1], route[2]) for route in df_routes if df_routes[0] == df_airports[1]]

def get_airports() -> list[tuple[str]]:
    """
    Returns the list of tuples containing every airport's name, country, city, and code.
    """
    df_airports = get_dataframe1('airports.csv')
    airports = []
    for ind in df_airports.index:
        airports.append((df_airports['3 Char Code'][ind], df_airports['Airport Name'][ind], df_airports['Country'][ind], df_airports['City'][ind]))
    return airports
