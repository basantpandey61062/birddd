from read_data import *
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression



class RegressionModel:
    # Private instance attribute
    _model: LinearRegression
    _ghg_data: List[float]
    _bird_data: List[float]

    def __init__(self, ghg_data: List[float], bird_data: List[float]) -> None:
        self._bird_data = bird_data
        self._ghg_data = ghg_data
        self._model = self.build_model()

    def build_model(self) -> LinearRegression():
        """ Return the Linear Regression model from the given data """
        arrays = lists_to_array(self._ghg_data, self._bird_data)
        x_data = arrays[0]
        y_data = arrays[1]
        model = LinearRegression().fit(x_data, y_data)

        return model

    def predict_data(self, x: float) -> float:
        """ Return the predicted y value for the given x value based
        of the LinearRegression model
        """
        m = float(self._model.coef_)
        b = float(self._model.intercept_)
        return m * x + b

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

# helper function
def lists_to_array(x: list, y: list) -> tuple:
    """ Return the x and y as a tuple of numpy arrays and
        reshape the x array to (-1, 1), so that it is one dimensional
    """
    x_array = np.array(x).reshape(-1, 1)
    y_array = np.array(y)

    return (x_array, y_array)

#########################################################################################################################
#########################################################################################################################

ghg_data = read_ghg_data(29)
co2 = [data.co2 for data in ghg_data if 1990 <= data.year <= 2016]


bird_data = read_bird_data()
waterfowl_data = filter_bird_data(bird_data, 8)
waterfowl = Bird(waterfowl_data)
waterfowl.trim_data(1990, 2016)


model = RegressionModel(co2, waterfowl_data)
model.plot_data(co2, waterfowl_data, 'Test')



