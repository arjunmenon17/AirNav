import pandas as pd
import numpy as np

def get_dataframe1(csv_file: str):
    
    airport_cols = ['3 Char Code', 'Facility Name', 'Lat', 'Long',
                    'rand', 'rand1', 'rand2', 'rand3', 'rand4', 'rand5']
    df_airports = pd.read_csv('airports.csv', skiprows=1, names=airport_cols)

    df1 = df_airports[['3 Char Code', 'Lat', 'Long']]

    return df1
    
def get_dataframe2(csv_file: str) -> list[list[str, str]]:
    route_cols = ['Airline', 'Airline ID', 'Source', 'Source Airport ID',
                'Dest', 'Dest Airport ID', 'Codeshare', 'Stops', 'equipment']
    routes_df = pd.read_csv(csv_file, skiprows=1, names=route_cols)

    df2 = routes_df[['Source', 'Dest']]

    return df2

def get_location(airport_key: str) -> tuple[float, float]:
    """
    Returns the latitude/longtidude of a given airport
    """
    df_airports = get_dataframe1('airports.csv')
    for ind in df_airports.index:
        if df_airports['3 Char Code'][ind] == airport_key:
            return (df_airports['Lat'][ind], df_airports['Long'][ind])


def get_destinations(airport_key: str) -> list[tuple[str, tuple[float, float]]]:
    """
    Returns the list of destinations with their airport codes and latitude/longitude for the given airport
    """
    df_routes = get_dataframe2('flight_routes.csv')
    df_airports = get_dataframe1('airports.csv')
    for ind in df_routes.index:
        if df_routes['3 Char Code'][ind] == airport_key:
            return [(route[1], route[2]) for route in df_routes if df_routes[0] == df_airports[1]]

def get_airports():