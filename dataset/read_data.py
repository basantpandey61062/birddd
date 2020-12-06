"""
Module that contains classes and functions which
read and process the data
"""
import csv
from dataclasses import dataclass
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
    """ A class representing the greenhouse gas emission data of a specific region
    in Canada (a province or territory)
    """
    # Private Attributes
    _data: List[GreenhouseGas]  # total GHG data of the province
    _dict_data: Dict[int, List[float]]  # mapping of year to GHG emissions for that year

    # Public Attributes
    # co2: List[float]
    # ch4: List[float]
    # n2o: List[float]
    # hfc: List[float]
    # pfc: List[float]
    # sf6: List[float]
    # nf3: List[float]
    # total: List[float]

    def __init__(self, data: List[GreenhouseGas]) -> None:
        self._data = data
        self._dict_data = self._sort_ghg_data()

        # self.co2 = self.adjust_list(1990, 2016, 0)
        # self.ch4 = self.adjust_list(1990, 2016, 1)
        # self.n2o = self.adjust_list(1990, 2016, 2)
        # self.hfc = self.adjust_list(1990, 2016, 3)
        # self.pfc = self.adjust_list(1990, 2016, 4)
        # self.sf6 = self.adjust_list(1990, 2016, 5)
        # self.nf3 = self.adjust_list(1990, 2016, 6)
        # self.total = self.adjust_list(1990, 2016, 7)

    def _sort_ghg_data(self) -> Dict[int, List[float]]:
        """ Return a dictionary mapping year to a list of greenhouse gas
        emissions for that year

        Note: This is a private method used only to initialize _dict_data.
        """
        sorted_dict = {}
        for row in self._data:
            sorted_dict[row.year] = [row.co2,
                                     row.ch4,
                                     row.n2o,
                                     row.hfc,
                                     row.pfc,
                                     row.sf6,
                                     row.nf3,
                                     row.total]

        return sorted_dict

    def adjust_list(self, start: int, end: int, index: int) -> List[float]:
        """ Return a list representing the data of a specific greenhouse gas
        emissions for self, which starts from <start> year and ends on <end> year
        in chronological order.

        The index is based off of the order which the greenhouse gasses appear
        in the dictionary values.

        That is:
         - co2 = 0
         - ch4 = 1
         - n20 = 2
         - hfc = 3
         - pfc = 4
         - sf6 = 5
         - nf3 = 6
         - total = 7

        Preconditions:
         - 0 <= index < 8
         - start < end
         - 1990 <= start <= 2016
         - 1990 <= end <= 2016
        """
        trimmed_list = []
        for year in range(start, end + 1):
            trimmed_list.append(self._dict_data[year][index])

        return trimmed_list


class Bird:
    """ An class representing a the data of a bird species

    Instance Attributes:
        - list_data: list of all indexes of change since 1970,
                     ordered by year (oldest data to most recent)

    Representation Invariants:
        - min(self.dict_data) >= 1990
        - max(self.dict_data) <= 2016
        - len(list_data) <= len(dict_data)
        - all(year in self.dict_data for year in range(1990, 2016))
        - all(element in self.dict_data.values() for element in self.list_data)

    Sample Usage:
    >>> bird_data = {year: year for year in range(1990, 2017)}
    >>> bird = Bird(bird_data)
    >>> bird.list_data == [n for n in range(1990, 2017)]
    True
    """
    list_data: list

    # Private Attributes
    _dict_data: Dict[int, float]  # dictionary mapping year to the bird's index of change

    def __init__(self, bird_data: dict) -> None:
        self._dict_data = bird_data
        self.list_data = _data_to_list(self._dict_data)

    def adjust_data(self, start: int, end: int) -> None:
        """ Adjust self.list_data to start from the year <start> to
        the year <end>.

        Preconditions:
         - start < end
         - 1990 <= end <= 2016
         - 1990 <= start <= 2016

        >>> bird_data = {1999: 1.0, 2000: 2.0, 2001: 3.0, 2002: 4.0}  # an example possible data
        >>> bird = Bird(bird_data)
        >>> bird.list_data == [1, 2, 3, 4]
        True
        >>> bird.adjust_data(2000, 2001)
        >>> bird.list_data
        [2.0, 3.0]
        """
        adjusted_dict = {year: self._dict_data[year] for year in range(start, end + 1)}

        # updates the list attribute to match the trimmed data
        self.list_data = _data_to_list(adjusted_dict)


def read_ghg_data(last_row: int) -> Dict[str, List[GreenhouseGas]]:
    """ Return a mapping of province names to a list of GreenhouseGas instances,
    where each instance in the list represents a row in the data set.

    The function will read <last_row> number of rows

    Note: The list of GreenhouseGas are ordered by year
    """
    with open('GHG.csv') as csvfile:
        reader = csv.reader(csvfile)
        ghg_data = {}

        # skips header
        next(reader)

        # reads each row in the dataset, up to the <last_row> row
        for _ in range(last_row):
            row = next(reader)
            province = str(row[1])

            if province in ghg_data:
                ghg_data[province].append(GreenhouseGas(year=int(row[0]),
                                                        region=row[1],
                                                        co2=float(row[5]),
                                                        ch4=float(row[6]),
                                                        n2o=float(row[8]),
                                                        hfc=float(row[10]),
                                                        pfc=float(row[11]),
                                                        sf6=float(row[12]),
                                                        nf3=float(row[13]),
                                                        total=float(row[14])))
            else:
                ghg_data[province] = [GreenhouseGas(year=int(row[0]),
                                                    region=row[1],
                                                    co2=float(row[5]),
                                                    ch4=float(row[6]),
                                                    n2o=float(row[8]),
                                                    hfc=float(row[10]),
                                                    pfc=float(row[11]),
                                                    sf6=float(row[12]),
                                                    nf3=float(row[13]),
                                                    total=float(row[14]))]

    return ghg_data


def read_bird_data() -> Dict[int, List[str]]:
    """ Read the 'bird_data.csv' file and Return a dictionary
    mapping each year to a list representing a row of bird data
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


def filter_bird_data(bird_data: Dict[int, List[str]], column: int) -> Dict[int, float]:
    """ Return a dictionary mapping the years between 1990-2016 inclusive in bird_data
    to a specific column in the data

        Preconditions:
            - 0 <= column <= 8
            - all(year in bird_data for year in range(1990, 2017))

    >>> data = {year: ['0.0', '1.0', '2.0', '3.0'] for year in range(1970, 2020)}
    >>> filtered_data = filter_bird_data(data, 0)
    >>> filtered_data == {year: 0.0 for year in range(1990, 2017)}
    True
    >>> filtered_data = filter_bird_data(data, 1)
    >>> filtered_data == {year: 1.0 for year in range(1990, 2017)}
    True
    """
    filtered_dict = {}
    for year in range(1990, 2017):
        column_data = bird_data[year][column]
        filtered_dict[year] = float(column_data)

    return filtered_dict


# helper function
def _data_to_list(data: Dict[int, float]) -> list:
    """ Return a list containing all the datapoints in data ordered by year

    The function isn't for the user to use. The doctest below is just to exemplify
    how the function works.

    >>> data = {2000: 0.0, 2001: 1.0, 2002: 2.0}
    >>> _data_to_list(data)
    [0.0, 1.0, 2.0]
    """
    start = min(data)
    end = max(data) + 1
    return [data[year] for year in range(start, end)]


if __name__ == '__main__':
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'extra-imports': ['python_ta.contracts', 'dataclasses', 'datetime'],
    #     'disable': ['R1705', 'C0200'],
    # })

    # import python_ta.contracts
    # python_ta.contracts.DEBUG_CONTRACTS = False
    # python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()
