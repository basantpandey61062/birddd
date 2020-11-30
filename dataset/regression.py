import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
from typing import List, Tuple
from read_data import *

class RegressionModel:
    """ A class representing the linear regression model of the given data """

    # Private instance attribute
    _model: LinearRegression
    _ghg_data: List[float]
    _bird_data: List[float]

    def __init__(self, ghg_data: List[float], bird_data: List[float]) -> None:
        self._bird_data = bird_data
        self._ghg_data = ghg_data
        self._model = self._build_model()

    def _build_model(self) -> LinearRegression:
        """ Return the Linear Regression model from the given data """
        arrays = self._lists_to_array(self._ghg_data, self._bird_data)
        x_data = arrays[0]
        y_data = arrays[1]
        model = LinearRegression().fit(x_data, y_data)
        return model

    def _lists_to_array(self, x: list, y: list) -> Tuple[np.array, np.array]:
        """ Return the x and y as a tuple of numpy arrays and
        reshape the x array to (-1, 1), so that it is one dimensional
        """
        x_array = np.array(x).reshape(-1, 1)
        y_array = np.array(y)

        return (x_array, y_array)

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

    def plot_data(self, title: str, x_label: str, y_label: str) -> None:
        """Plot the given data with a line of best fit generated from the
        regression model
        """
        x_range = [min(self._ghg_data), max(self._ghg_data)]
        y_range = [self.predict_y(x_range[0]),
                   self.predict_y(x_range[1])]

        fig = px.scatter(x=self._ghg_data,
                         y=self._bird_data,
                         title=title,
                         labels = {'x': x_label,
                                   'y': y_label})

        fig.add_traces(go.Scatter(x=x_range, y=y_range, name="Regression Line"))
        fig.show()


# class MultipleRegression:
#     _model: LinearRegression
#     _ghg_data: List[List[float]]
#     _bird_data: List[float]

#     def __init__(self, ghg_data: List[List[float]], bird_data: List[float]) -> None:
#         self._ghg_data = ghg_data
#         self._bird_data = bird_data
#         self._model = self._build_model()

#     def _build_model(self) -> LinearRegression:
#         x_values = np.array(self._ghg_data).reshape(1, -1)
#         y_values = np.array(self._bird_data)
#         model = LinearRegression().fit(x_values, y_values)
#         return model

#     def plot_data(self, title: str, x_label: str, y_label: str) -> None:
#         """Plot the given data with a line of best fit generated from the
#         regression model
#         """
#         x_range = [min(self._ghg_data), max(self._ghg_data)]
#         y_range = [self.predict_data(x_range[0]),
#                    self.predict_data(x_range[1])]

#         fig = px.scatter(x=self._ghg_data,
#                          y=self._bird_data,
#                          title=title,
#                          labels = {'x': x_label,
#                                    'y': y_label})

#         fig.add_traces(go.Scatter(x=x_range, y=y_range, name="Regression Line"))
#         fig.show()

#########################################################################################################################
# Example Usage
#########################################################################################################################

# ghg_data = read_ghg_data(100)  # reads the data
# # keys = ghg_data.keys()  # gets all the possible keys
# alberta = Province(ghg_data['Alberta'])  # creates a Province object

# bird_data = read_bird_data()  # reads the bird data
# bird_data = filter_bird_data(bird_data, 8)  # filters the bird data so that only column 8 remains
# bird = Bird(bird_data)  # creates an Bird Object
# bird.trim_data(1990, 2016)  # trims the bird data to match the length of the GHG data

# # model = RegressionModel(alberta.total, bird.list_data)  # creates the linear regression model
# # model.predict(69)  # predicts the index of change of bird species for 69 kt of emission
# x = [alberta.co2, alberta.ch4, alberta.sf6]
# model = MultipleRegression(x, [bird.list_data])
# model.plot_data('Test', 'x', 'y')  # plots the data