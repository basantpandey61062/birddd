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

        Preconditions:
            - ghg_data is a list of floats representing the greenhouse gas emissions
              of a region and is a value directly from the dictionary returned by the
              read_ghg_data function

            - bird_data is a list of percentage changes for a specific bird species and
              is directly from the Bird class
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
        """Return a float representing the r squared value of the model"""
        x, y = _lists_to_array(self._ghg_data, self._bird_data)
        return round(self._model.score(x, y), 6)

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
    _model: LinearRegression

    def __init__(self, x_variables: Dict[str, List[float]], y_values: List[float]) -> None:
        """Initialize the _model attribute

        Preconditions:
            - x_variables is a dictionary mapping names of GHGs to a list of floats
              representing the annual emissions of a region

            - y_values is a list of floats representing the index change for a species of birds
              and comes directly from the Bird class
        """
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

        Preconditions:
            - all(value >= 0 for value in {co2, ch4, n2o, hfc, pfc, sf6, nf3})
        """
        return float(self._model.predict([[co2, ch4, n2o, hfc, pfc, sf6, nf3]]))

    def _get_coef(self) -> Dict[str, float]:
        """Return a dictionary mapping the name of a greenhouse gas to
        the multiple regression coefficient
        """
        coefficients = self._model.coef_
        mapping = {'CO2': coefficients[0],
                   'CH4': coefficients[1],
                   'N2O': coefficients[2],
                   'HFC': coefficients[3],
                   'PFC': coefficients[4],
                   'SF6': coefficients[5],
                   'NF3': coefficients[6]}

        return mapping

# Helper Function
def _lists_to_array(x: list, y: list) -> Tuple[np.array, np.array]:
    """ Return the x and y as a tuple of numpy arrays and
    reshape the x array to (-1, 1), so that it is one dimensional
    """
    x_array = np.array(x).reshape(-1, 1)
    y_array = np.array(y)

    return (x_array, y_array)
