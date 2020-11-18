from read_data import *
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression


def build_model(gas_data: List[float],  sea_data: List[float]) -> tuple:
    arrays = lists_to_array(gas_data, sea_data)
    x_data = arrays[0]
    y_data = arrays[1]
    model = LinearRegression().fit(x_data, y_data)

    return model


def lists_to_array(x: list, y: list) -> tuple:
    x_array = np.array(x).reshape(-1, 1)
    y_array = np.array(y)

    return (x_array, y_array)


def predict_data(x: float , model: LinearRegression) -> float:
    m = float(model.coef_)
    b = float(model.intercept_)
    return m * x + b


def plot_data(x_values: List[float], y_values: List[float], model: LinearRegression, title: str) -> None:
    x_range = [min(x_values), max(x_values)]
    y_range = [predict_data(x_range[0], model), predict_data(x_range[1], model)]

    fig = px.scatter(x=x_values,
                     y=y_values,
                     title=title,
                     labels = {'x': "Greenhouse Gas Emissions (kt)", 'y': "Mean Sea Level (mm)"})
    fig.add_traces(go.Scatter(x=x_range, y=y_range, name="Regression Line"))
    fig.show()


ghg_data = read_ghg_data('GHG.csv', 30)
sea_data = read_sea_level_data('sea_levels.csv')
sea_dict = sea_level_to_dict(sea_data)


total = [datapoint.total for datapoint in ghg_data if datapoint.year in range(1992, 2019)]
sea_level =[sea_dict[year] for year in range(1992, 2019)]

model = build_model(total, sea_level)
plot_data(total, sea_level, model, 'Data')
