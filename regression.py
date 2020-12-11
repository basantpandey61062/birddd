"""
Module that contains class and functions for computations
and the creation of regression models
"""
import numpy as np
import pandas
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
from typing import List, Tuple, Dict


class RegressionModel:
    """ A class representing the linear regression model of the given data """

    # Private instance attributes
    #   -_model: the linear regression model
    #   -_ghg_data: a list of floats representing the ghg emissions of a region
    #   -_bird_data: a list of floats representing the percentage change of a
    #    species of birds since 1970
    _model: LinearRegression
    _ghg_data: List[float]
    _bird_data: List[float]

    def __init__(self, ghg_data: List[float], bird_data: List[float]) -> None:
        """ Initialize the RegressionModel

        Preconditins:
            - ghg_data is a list of floats representing the greenhouse gas emissions
              of a region
            - bird_data is a list of percentage changes for a specific bird species
        """
        self._bird_data = bird_data
        self._ghg_data = ghg_data
        self._model = self._build_model()

    def _build_model(self) -> LinearRegression:
        """ Return the Linear Regression model from the given data """
        arrays = _lists_to_array(self._ghg_data, self._bird_data)
        x_data = arrays[0]
        y_data = arrays[1]
        model = LinearRegression().fit(x_data, y_data)
        return model

    def predict_y(self, x: float) -> float:
        """ Return the predicted y value for the given x value based
        off of the LinearRegression model.

        In other words, given the quantity of greenhouse gas emissions,
        Return the expected index of change for the bird species
        """
        m = float(self._model.coef_)
        b = float(self._model.intercept_)
        return m * x + b

    def predict_x(self, y: float) -> float:
        """ Return a float representing the projected change in ghg emissions
        for an index of change of y based off the LinearRegression model.
        """
        m = float(self._model.coef_)
        b = float(self._model.intercept_)
        return (y - b) / m

    def get_r_squared(self) -> float:
        """"Return a float representing the r squared value of the model"""
        x, y = _lists_to_array(self._ghg_data, self._bird_data)
        return self._model.score(x, y)

    def plot_data(self, title: str, x_label: str, y_label: str) -> None:
        """Plot the given data with a line of best fit generated from the
        regression model
        """
        x_range = [min(self._ghg_data), max(self._ghg_data)]
        y_range = [self.predict_y(x_range[0]),
                   self.predict_y(x_range[1])]

        fig = px.scatter(x=self._ghg_data,
                         y=self._bird_data,
                         title=f'{title} {" " * 10} R^2 = {self.get_r_squared()}',
                         labels={'x': x_label,
                                 'y': y_label})

        fig.add_traces(go.Scatter(x=x_range, y=y_range, name="Regression Line"))
        fig.show()


class MultipleRegression:
    """Class Representing the multiple regression model for the given data

    Instance Attributes:
        - coef: a dictionary mapping the name of the GHG to the corresponding
          coefficient/weighting
    """
    coef: Dict[str, float]

    # Private Attributes
    #   - _model: the multiple regression model
    #   -_x_variables: a pandas Dataframe representing the given ghg data
    _model: LinearRegression
    _x_variables: pandas.DataFrame

    def __init__(self, x_variables: Dict[str, List[float]], y_values: List[float]) -> None:
        """Initialize the _model attribute
        Preconditions:
            - x_variables is a dictionary mapping names of GHGs to a list of floats
              representing the annual emissions of a region
            - y_values is a list of floats representing the index change for a species of birds
        """
        self._x_variables = pandas.DataFrame(x_variables)
        self._model = LinearRegression().fit(pandas.DataFrame(x_variables), y_values)
        self.coef = self._get_coef()

    def predict_value(self,
                      co2: float,
                      ch4: float,
                      n2o: float,
                      hfc: float,
                      pfc: float,
                      sf6: float,
                      nf3: float
                    ) -> float:
        """ Return the estimated percentage change since 1970 of birds for the given
        greenhouse gas values base off of the LinearRegression Model.
        """
        return float(self._model.predict(co2, ch4, n2o, hfc, pfc, sf6, nf3))

    def _get_coef(self) -> Dict[str, float]:
        """Return a dictionary mapping the name of a greenhouse gas to
        the multiple regression coefficient
        """
        coefficients = self._model.coef_
        mapping = {'co2': coefficients[0],
                   'ch4': coefficients[1],
                   'n2o': coefficients[2],
                   'hfc': coefficients[3],
                   'pfc': coefficients[4],
                   'sf6': coefficients[5],
                   'nf3': coefficients[6]}

        return mapping

# Helper Function
def _lists_to_array(x: list, y: list) -> Tuple[np.array, np.array]:
    """ Return the x and y as a tuple of numpy arrays and
    reshape the x array to (-1, 1), so that it is one dimensional
    """
    x_array = np.array(x).reshape(-1, 1)
    y_array = np.array(y)

    return (x_array, y_array)


########################################################################################################################
# Example Usage
########################################################################################################################
# from read_data import *

# ghg_data = read_ghg_data(398)  # reads the data
# # # keys = ghg_data.keys()  # gets all the possible keys
# # alberta = Province(ghg_data['Alberta'])  # creates a Province object
# canada = Region(ghg_data['Alberta'])
# bird_data = read_bird_data()  # reads the bird data
# bird_data = filter_bird_data(bird_data, 8)  # filters the bird data so that only column 8 remains
# bird = Bird(bird_data)  # creates an Bird Object
# bird.adjust_data(1990, 2016)  # trims the bird data to match the length of the GHG data
# model = RegressionModel(canada.total, bird.list_data)  # creates the linear regression model
# # model.predict_y(69)  # predicts the index of change of bird species for 69 kt of emission
# model.plot_data('Test', 'x', 'y')  # plots the data


########################################################################################################################
# Multiple Regression Usage
########################################################################################################################

# some default thing you need to set
# df =  pandas.DataFrame({'co2': canada.co2,
#                         'ch4': canada.ch4,
#                         'n2o': canada.n2o,
#                         'hfc': canada.hfc,
#                         'pfc': canada.pfc,
#                         'sf6': canada.sf6,
#                         'nf3': canada.nf3})
# canada.initialize_lists(1990, 2016)
# x = {'co2': canada.co2,
#     'ch4': canada.ch4,
#     'n2o': canada.n2o,
#     'hfc': canada.hfc,
#     'pfc': canada.pfc,
#     'sf6': canada.sf6,
#     'nf3': canada.nf3}

# model = MultipleRegression(x, bird.list_data)
# print(model._model.coef_)
# model.plot()
