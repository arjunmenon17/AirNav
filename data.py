"""CSC111 Winter 2023 Course Project: AirNav

Module Information: data.py
===============================

This Python module contains the data parsing functions for building dataframes of
the flight network's data and export functions for this data to be used in other
parts of the program such as the GUI and the network module.

Copyright and Usage Information
===============================

This file is provided solely for the submission of the CSC111 Course Project and to be
used by instructors and TAs while marking and assessing this project.

This file is Copyright (c) 2023 Arjun Menon, Azlan Naeem, Hadi Naqvi, and Rohan Regi.
"""
from __future__ import annotations

# import os
import numpy as np
import pandas as pd
# from python_ta.contracts import check_contracts


def get_dataframe1(csv_file: str) -> pd.DataFrame:
    """
    Extracts the 3 character code for an airport along with its given geographical location in terms of latitude and
    longitude. Preconditions: - csv_file in os.getcwd() - csv_file is a valid dataset
    """
    df_airports = pd.read_csv(csv_file)
    df = df_airports.replace('\\N', np.NaN)
    df = df.dropna()  # Drops rows with NaN values
    df = df.reset_index()
    df1 = df[['3 Char Code', 'Lat', 'Long', 'Airport Name', 'City', 'Country']]

    return df1


# @check_contracts
def get_dataframe2(csv_file: str) -> pd.DataFrame:  # list[list[str, str]]
    """
    Returns a nested list of real life flight paths. Each list inside the original list is a single flight path
    with a source airport and a destination airport.
    Preconditions:
        - csv_file in os.getcwd()
        - csv_file is a valid dataset
    """
    airport_codes = DATAFRAME1['3 Char Code'].tolist()

    route_cols = ['Airline', 'Airline ID', 'Source', 'Source Airport ID',
                  'Dest', 'Dest Airport ID', 'Codeshare', 'Stops',
                  'equipment']  # Sets new column names for the dataframe
    routes_df = pd.read_csv(csv_file, names=route_cols, skiprows=1, low_memory=False)  # Has too many columns
    routes_df = routes_df[routes_df['Source'].isin(airport_codes) & routes_df['Dest'].isin(airport_codes)]

    df = routes_df.reset_index()
    df2 = df[['Source', 'Dest']]

    return df2


# @check_contracts
def get_location(airport_key: str) -> tuple[float, float] | None:
    """
    Returns the latitude/longtidude of a given airport.
    Preconditions:
        - len(airport_key) == 3
    """
    for ind in DATAFRAME1.index:
        if DATAFRAME1['3 Char Code'][ind] == airport_key:
            return (DATAFRAME1['Lat'][ind], DATAFRAME1['Long'][ind])

    return None


# @check_contracts
def get_destinations(airport_key: str) -> set[tuple[str, tuple[float, float]]]:
    """
    Returns the list of destinations with their airport codes and latitude/longitude for the given airport.
    Preconditions:
        - len(airport_key) == 3
    """
    lat_lon_dict = {row_vals['3 Char Code']: (row_vals['Lat'], row_vals['Long'])
                    for _, row_vals in DATAFRAME1.iterrows()}
    # Filter route DataFrame to get all routes departing from the given airport
    departures = DATAFRAME2.loc[DATAFRAME2['Source'] == airport_key]

    # Create an empty list to store the destination airports and their latitude/longitude
    destinations = []

    # Loop through each departure to get the destination airport and its latitude/longitude
    for _, row in departures.iterrows():
        dest_key = row['Dest']
        dest_lat, dest_lon = lat_lon_dict[dest_key]
        destinations.append((dest_key, (dest_lat, dest_lon)))
    return set(destinations)


def get_airports() -> set[tuple[str, str, str, str]]:
    """
    Returns the set of tuples containing every airport's name, country, city, and code.
    """
    airports = []
    for ind in DATAFRAME1.index:
        airports.append((DATAFRAME1['3 Char Code'][ind], DATAFRAME1['Airport Name'][ind], DATAFRAME1['Country'][ind],
                         DATAFRAME1['City'][ind]))
    return set(airports)


DATAFRAME1 = get_dataframe1("airports.csv")
DATAFRAME2 = get_dataframe2("flight_routes.csv")
route_airports = set(DATAFRAME2['Source']).union(set(DATAFRAME2['Dest']))
DATAFRAME1 = DATAFRAME1[DATAFRAME1['3 Char Code'].isin(route_airports)]

if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pandas', 'numpy', 'os'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'disable': ['E9992', 'E9997'],
        'max-line-length': 120
    })
