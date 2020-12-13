"""
Interface Objects

Module Contains classes for program interface.
"""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass
import pygame
from read_data import Bird, GreenhouseGas, Region, filter_bird_data
from regression import RegressionModel, MultipleRegression


class Button:
    """Class to hold a button's image and it's coordinates on the screen.

    Instance Attributes:
        - tag: the type of button (three types: normal, output, display)
        - name: the name of the button
        - text: a pygame surface that displays the name
        - image: the image of the button that will be displayed
        - rect: a pygame rect that holds the button's dimensions and coordinates
    """
    # Private Instance Attributes:
    #   - _font: the font the button text will be displayed in

    tag: str
    name: str
    text: pygame.Surface
    image: Optional[pygame.Surface] = None
    rect: pygame.Rect
    _font: pygame.font.Font

    def __init__(self, tag: str, name: str, font: pygame.font.Font,
                 image: Optional[pygame.Surface] = None) -> None:
        self.tag = tag
        self.name = name
        self._font = font
        self.text = font.render(self.name, True, (0, 0, 0))
        self.image = image
        if image is not None:
            self.rect = self.image.get_rect()
        else:
            self.rect = self.text.get_rect()

    def update_name(self, name: str) -> None:
        """Reassigns text attribute based on name."""
        self.name = name
        self.text = self._font.render(self.name, True, (0, 0, 0))


class InputButton(Button):
    """A button that can hold inputs.

    Instance Attributes:
        - tag: the type of button (two types: normal, display)
        - name: the name of the button
        - text: a pygame surface that displays the name
        - image: the image of the button that will be displayed
        - rect: a pygame rect that holds the button's dimensions and coordinates
        - output_button: the button's corresponding output button that changes as
        - prompt: the input prompt the button displays
        the input changes
    """
    # Private Instance Attributes:
    #   - _font: the font the button text will be displayed in

    tag: str
    name: str
    text: pygame.Surface
    image: Optional[pygame.Surface] = None
    rect: pygame.Rect
    output_button: Button
    prompt: str
    _font: pygame.font.Font

    def __init__(self, tag: str, prompt: str, font: pygame.font.Font,
                 output_button: Button) -> None:
        Button.__init__(self, tag, prompt, font)
        self.output_button = output_button
        self.prompt = prompt
        self.name = self.prompt + '0'
        self.text = self._font.render(self.name, True, (0, 0, 0))


@dataclass
class Page:
    """Class to hold a page to be displayed on the screen with all it's buttons.

    Instance Attributes:
        - background: a pygame surface with the background image for the page
        - buttons: holds all the buttons that the page has
    """
    background: pygame.Surface
    buttons: List[Button]


class Selection:
    """Class to store and handle user's selections."""

    # Private Instance Attributes:
    #   - _region: the user selected region
    #   - _bird: the user selected bird
    #   - _ghg: the user selected greenhouse gas

    _region: Optional[str] = None
    _bird: Optional[int] = None
    _ghg: Optional[int] = None

    def __init__(self) -> None:
        self._region = None
        self._bird = None
        self._ghg = None

    def handle_selection(self, current_page: int, selection: str) -> None:
        """Handles what selection the user chooses and updates instance attributes
        accordingly."""
        if current_page == 0:
            self.change_region(selection)
        elif current_page == 1:
            self.change_bird(selection)
        elif current_page == 2:
            self.change_ghg(selection)

    def get_model(self, ghg_data: Dict[str, List[GreenhouseGas]],
                  bird_data: Dict[int, List[str]]) -> Union[RegressionModel, MultipleRegression]:
        """Returns RegressionModel for current selections (the bird index with respect
        to the amount of ghg's produced for the selected region).
        """
        # Filtering data
        filtered_bird_data = filter_bird_data(bird_data, self._bird)

        # Creating class instances
        region = Region(ghg_data[self._region])
        bird = Bird(filtered_bird_data)

        # Finding correct start year for the region
        if self._region == 'Northwest Territories' or self._region == 'Nunavut':
            start_year = 1999
        else:
            start_year = 1990

        bird.adjust_data(start_year, 2016)
        bird_list = bird.list_data
        if self._ghg == 9:
            region.initialize_lists(start_year, 2016)
            x_vars = {'CO2': region.co2,
                      'CH4': region.ch4,
                      'N2O': region.n2o,
                      'HFC': region.hfc,
                      'PFC': region.pfc,
                      'SF6': region.sf6,
                      'NF3': region.nf3}

            return MultipleRegression(x_vars, bird_list)

        else:
            ghg_list = region.adjust_list(start_year, 2016, self._ghg)

            return RegressionModel(ghg_list, bird_list)

    def change_region(self, province_name: str) -> None:
        """Changes region selection to selected region."""
        self._region = province_name

    def change_bird(self, bird_name: str) -> None:
        """Changes bird selection to selected bird based on bird_index."""
        bird_dict = {'Waterfowl': 0,
                     'Birds of Prey': 1,
                     'Wetland Birds': 2,
                     'Seabirds': 3,
                     'Forest Birds': 4,
                     'All Other Birds': 5,
                     'Shorebirds': 6,
                     'Grassland Birds': 7,
                     'Aerial Insectivores': 8}
        self._bird = bird_dict[bird_name]

    def change_ghg(self, ghg_name: str) -> None:
        """Changes ghg selection to selected ghg based on ghg_index."""
        ghg_dict = {'CO2': 0,
                    'CH4': 1,
                    'N2O': 2,
                    'HFC': 3,
                    'PFC': 4,
                    'SF6': 5,
                    'NF3': 6,
                    'Total': 7,
                    'Multiple Regression': 9}
        self._ghg = ghg_dict[ghg_name]


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
