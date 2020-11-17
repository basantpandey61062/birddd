from pprint import pprint
import csv
from dataclasses import dataclass
import plotly.express as px
from typing import List


@dataclass
class GreenhouseGas:
    """ dataclass representing greenhouse gas emissions of a province in a given year

    Instance Attributes:
        - year: year of the given data
        - region: province/territory of the given data
        - co2: amount of co2 emissions in the given year for the given province
        - ch4: amount of ch4 emissions in the given year for the given province
        - hfc: amount of HPC emissions in the given year for the given province
        - pfc: amount of PFC emissions in the given year for the given province
        - sf6: amount of sf6 emissions in the given year for the given province
        - nf3: amount of nf3 emissions in the given year for the given province
        - total: the total amount of greenhouse gas emissions in data
    """
    year: int
    region: str
    co2: float
    ch4: float
    n2o: float
    hfc: float
    pfc: float
    sf6: float
    nf3: float
    total: float


def read_ghg_data(filename: str, last_row: int) -> List[GreenhouseGas]:
    """ Return a list of GreenhouseGas instances, where each instance in
        the list represents a row in the data set.

        The function will read last_row number of rows
    """
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        ghg_data = []

        # skips header
        next(reader)

        # reads each row in the dataset, up to the last_row row
        for _ in range(last_row):
            row = next(reader)
            ghg_data.append(GreenhouseGas(year=int(row[0]),
                                          region=row[1],
                                          co2=float(row[5]),
                                          ch4=float(row[6]),
                                          n2o=float(row[8]),
                                          hfc=float(row[10]),
                                          pfc=float(row[11]),
                                          sf6=float(row[12]),
                                          nf3=float(row[13]),
                                          total=float(row[14])))

    return ghg_data


def read_sea_level_data(filename) -> List[List]:
    """ Return a list containing each row in the dataset as a
        list.
    """
    # sea level data processing
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        sea_level = []
        for row in reader:
            sea_level.append(row)

    return sea_level[6:]  # trims the data, first 6 rows are headers and text


def sea_level_to_dict(sea_level: list) -> dict:
    """ Return the mapping of year to average sea level during
        that year
    """
    sea_mapping = {}  # mapping of year to average sea level
    for row in sea_level:
        # turns the year from a string into an int
        # consequently floors the year, as wanted
        year = int(float(row[0]))

        # average sea level for given datapoint
        average = average_sea_level(row)

        # appends the average sea level for a certain part of the year to the dict
        if year in sea_mapping:
            sea_mapping[year].append(average)
        else:
            sea_mapping[year] = [average]

    return average_per_year(sea_mapping)


def average_sea_level(row: list) -> float:
    """ Return the average sea level for the given row """
    total_sea_level = sum([float(num) for num in row[1:] if num != ''])
    data_sources = (4 - row[1:].count(''))

    return total_sea_level / data_sources


def average_per_year(sea_mapping: dict) -> dict:
    """ Return the average sea level per year """
    sealevel_per_year = {}
    for year in sea_mapping:
        total_per_year = sum(sea_mapping[year])
        datapoints_per_year = len(sea_mapping[year])

        sealevel_per_year[year] = total_per_year / datapoints_per_year

    return sealevel_per_year


def build_figure(x, y):
    return px.scatter(x=x, y=y)



data = read_sea_level_data('C:/Users/mengh/Desktop/csc110/FINAL PROJECT/dataset/sea_levels.csv')
sd = sea_level_to_dict(data)


pprint(sd)
