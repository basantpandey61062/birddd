import csv
from dataclasses import dataclass
import plotly.express as px
from typing import List, Dict


@dataclass
class GreenhouseGas:
    """ dataclass representing greenhouse gas emissions of a region in a given year

    Instance Attributes:
        - year: year of the given data
        - region: region of the given data
        - co2: amount of co2 emissions in the given year for the given region
        - ch4: amount of ch4 emissions in the given year for the given region
        - hfc: amount of HPC emissions in the given year for the given region
        - pfc: amount of PFC emissions in the given year for the given region
        - sf6: amount of sf6 emissions in the given year for the given region
        - nf3: amount of nf3 emissions in the given year for the given region
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


class Province:
    """ A class representing the data of a Province"""

    # Private Attributes
    _data: List[GreenhouseGas]
    _dict_data: dict

    name: str
    co2: List[float]
    ch4: List[float]
    n2o: List[float]
    total: List[float]

    def __init__(self, data: List[GreenhouseGas]) -> None:
        self.name = data[0].region
        self._data = data
        self._dict_data = self.sort_ghg_data()
        self.co2 = self.combine_as_list(0)
        self.ch4 = self.combine_as_list(1)
        self.n2o = self.combine_as_list(2)
        self.total = self.combine_as_list(3)

    def sort_ghg_data(self) -> List[GreenhouseGas]:
        """Return a dictionary mapping year to a list of greenhouse gas
        emissions for that year
        """

        sorted_dict = {}
        for row in self._data:
            sorted_dict[row.year] = [row.co2, row.ch4, row.n2o, row.total]

        return sorted_dict

    def combine_as_list(self, index: int) -> List[float]:
        """ Return a list containing all greenhouse gas with index <index>

        The index is based off of the order which the greenhouse gasses appear
        in the dictionary values (e.g. 0 = co2, 1 = ch4, 2 = n2o ... etc)

        Preconditions:
         - 0 <= index < 4  # change this as you add more ghg
        """
        list_so_far = []
        for year in self._dict_data:
            list_so_far.append(self._dict_data[year][index])

        return list_so_far

    def trim_data(self, start: int, end: int) -> None:
        """ Trim and reassign all attributes to new values
        so that only data between start and end remain.

        Note: After the data is trimmed it cannot be reverted or untrimmed.

        Preconditions:
         - start < end
         - 1990 <= start <= 2018
         - 1990 <= end <= 2018
        """
        trimmed_dict = {year: self._dict_data[year] for year in range(start, end + 1)}

        # updating dict_data
        self._dict_data = trimmed_dict

        # trimming the lists by updating them
        self.co2 = self.combine_as_list(0)
        self.ch4 = self.combine_as_list(1)
        self.n2o = self.combine_as_list(2)
        self.total = self.combine_as_list(3)


class Bird:
    """ An class representing a the data of a bird species """
    dict_data: dict
    list_data: list

    def __init__(self, bird_data: dict) -> None:
        self.dict_data = bird_data
        self.list_data = self.data_to_list()

    def trim_data(self, start: int, end: int) -> None:
        """ Create a new dict that contains all bird data from the year <start> to
        the year <end> and reassign self.data to it.

        Note: After the data is trimmed it cannot be reverted or untrimmed.

        Preconditions:
         - start < end
         - 1970 <= end <= 2016
         - 1970 <= start <= 2016

        >>> bird = Bird({2000: 1.0, 2001: 2.0, 2003: 3.0})
        >>> bird.trim_data(2000, 2001)
        >>> bird.data
        {2000: 1.0, 2001: 2.0}
        """
        self.dict_data = {year: self.dict_data[year] for year in range(start, end + 1)}

        # updates the list attribute to match the trimmed data
        self.list_data = self.data_to_list()

    def find_first_point(self) -> int:
        """ Return the first year where the data is not 'n/a' """
        for year in self.dict_data:
            if self.dict_data[year] != 'n/a':
                return year

    def data_to_list(self) -> float:
        """ Return a list containing all the datapoints in data ordered by year
        >>> bird = Bird({2000: 1.0, 2001: 2.0, 2003: 3.0})
        >>> bird.data_to_list()
        [1.0, 2.0, 3.0]
        """
        return [self.dict_data[year] for year in range(1990, 2017)]


def read_ghg_data(last_row: int) -> List[GreenhouseGas]:
    """ Return a list of GreenhouseGas instances, where each instance in
        the list represents a row in the data set.

        The function will read last_row number of rows
    """
    with open('GHG.csv') as csvfile:
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


def read_bird_data() -> dict:
    """ Read the 'bird_data.csv' file and Return a dictionary
    mapping each year to a list of
    """
    with open('bird_data.csv') as csvfile:
        reader = csv.reader(csvfile)
        # skips headers
        for _ in range(3):
            next(reader)

        bird_data = {}

        for _ in range(47):
            row = next(reader)
            bird_data[int(row[0])] = [row[1],
                                      row[2],
                                      row[3],
                                      row[4],
                                      row[5],
                                      row[6],
                                      row[7],
                                      row[8],
                                      row[9]]
    return bird_data


def filter_bird_data(bird_data: dict, column: int) -> dict:
    """ Return a dictionary mapping the years in bird_data to a
        specific column in the data

        Preconditions:
         - 0 <= column <= 8

    >>> filter_bird_data({2002: ['0', '1', '2', '3', '4', '5'],\
                          2003: ['0', '1', '2', '3', '4', '5'] }, 0)
    {2002: 0, 2003: 0}
    """
    filtered_dict = {}
    for year in bird_data:
        column_data = bird_data[year][column]
        if column_data != 'n/a':
            filtered_dict[year] = float(column_data)
        else:
            filtered_dict[year] = 'n/a'

    return filtered_dict

