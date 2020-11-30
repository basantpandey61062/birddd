import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
from typing import List
from read_data import *

class RegressionModel:
    # Private instance attribute
    _model: LinearRegression
    _ghg_data: List[float]
    _bird_data: List[float]

    def __init__(self, ghg_data: List[float], bird_data: List[float]) -> None:
        self._bird_data = bird_data
        self._ghg_data = ghg_data
        self._model = self._build_model()

    def _build_model(self) -> LinearRegression():
        """ Return the Linear Regression model from the given data """
        arrays = self._lists_to_array(self._ghg_data, self._bird_data)
        x_data = arrays[0]
        y_data = arrays[1]
        model = LinearRegression().fit(x_data, y_data)
        return model

    def _lists_to_array(self, x: list, y: list) -> tuple:
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

    def plot_data(self, title: str) -> None:
        x_range = [min(self._ghg_data), max(self._ghg_data)]
        y_range = [self.predict_data(x_range[0]),
                   self.predict_data(x_range[1])]

        fig = px.scatter(x=self._ghg_data,
                         y=self._bird_data,
                         title=title,
                         labels = {'x': "Greenhouse Gas Emissions (kt)",
                                   'y': "Percentage of Change in Bird Population from 1970"})

        fig.add_traces(go.Scatter(x=x_range, y=y_range, name="Regression Line"))
        fig.show()


#########################################################################################################################
# Example Usage
#########################################################################################################################

# ghg_data = read_ghg_data(50)  # reads the data
# alberta = Province(ghg_data['Alberta'])  # creates a Province object

# bird_data = read_bird_data()  # reads the bird data
# bird_data = filter_bird_data(bird_data, 8)  # filters the bird data so that only column 8 remains
# bird = Bird(bird_data)  # creates an Bird Object
# bird.trim_data(1990, 2016)  # trims the bird data to match the length of the GHG data

# model = RegressionModel(alberta.total, bird.list_data)  # creates the linear regression model
# model.plot_data('Test')  # plots the data
# model.predict(69)  # predicts the index of change of bird species for 69 kt of emission