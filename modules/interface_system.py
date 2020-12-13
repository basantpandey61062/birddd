"""
Interface System

Module contains InterfaceSystem class that allows
user inputs and interface objects to interact with each other.
"""

import sys
from typing import Dict, List, Optional, Tuple
import pygame
from pygame.locals import *
from modules.interface_objects import Button, InputButton, Page, Selection
from modules.read_data import GreenhouseGas
from modules.create_pages import create_pages


class InterfaceSystem:
    """Class to hold all objects for the main program.

    Instance Attributes:
        - pages: a list holding all the Page objects in the program
        - current_page: a number indicating which page is currently displayed
        - mouse_pos: the coordinates of the mouse
        - mouse_clicked: whether the mouse is clicked or not
    """
    # Private Instance Attributes:
    #   - _selection: holds the region, bird, and gas chosen by the user
    #   - _focused_button: the button the user is typing on
    #   - _datasets: a tuple containing 2 mappings. The first index has a mapping of
    #     region names to a list of GreenhouseGas instances. The second index has a
    #     mapping of years to a list representing a row of bird data.

    pages: List[Page]
    current_page: int
    mouse_pos: Tuple[int, int]
    mouse_clicked: bool
    _selection: Selection
    _focused_button: Optional[InputButton] = None
    _datasets: Tuple[Dict[str, List[GreenhouseGas]], Dict[int, List[str]]]

    def __init__(self, ghg_data: Dict[str, List[GreenhouseGas]],
                 bird_data: Dict[int, List[str]]) -> None:
        self.pages = create_pages()
        self.current_page = 0
        self.mouse_pos = (0, 0)
        self.mouse_clicked = False
        self._selection = Selection()
        self._focused_button = None
        self._datasets = (ghg_data, bird_data)

    def handle_events(self) -> None:
        """Handles the events the pygame receives(handles mouse movement, mouse clicking
        and typing).
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                self.mouse_pos = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse_pos = event.pos
                self.mouse_clicked = True
            elif self._focused_button is not None and event.type == KEYDOWN:
                self._handle_key_press(event)

    def handle_mouse_click(self, button: Button) -> None:
        """Tells program what to do based on what the mouse clicks."""
        if button.name == 'BACK':
            self._clear_all_input()
            self.current_page -= 1
            self._focused_button = None
            if self.current_page == len(self.pages) - 2:
                self.current_page -= 1
        elif button.name == 'Show Graph':
            self._plot_graph()
        elif button.name == 'Multiple Regression':
            self._selection.handle_selection(self.current_page, button.name)
            self.current_page += 2
            self._update_ghg_coefs()
        elif button.tag == 'normal' and self.current_page < len(self.pages) - 2:
            self._selection.handle_selection(self.current_page, button.name)
            self.current_page += 1
        elif isinstance(button, InputButton):
            self._focused_button = button

    def update_output(self, input_button: InputButton) -> None:
        """Updates button that shows predicted output from user's input.

        Gets input from the input button's name, gets the corresponding output, and changes
        the output button's name accordingly to be displayed.
        """
        ghg_data, bird_data = self._datasets
        model = self._selection.get_model(ghg_data, bird_data)

        # Handles multiple regression page
        if self.current_page == len(self.pages) - 1:
            amounts_ghg = self._get_multiple_regression_inputs()
            output = round(model.predict_value(amounts_ghg[0], amounts_ghg[1], amounts_ghg[2],
                                               amounts_ghg[3], amounts_ghg[4], amounts_ghg[5],
                                               amounts_ghg[6]), 2)
        # Handles single variable prediction
        else:
            amount_ghg = float(input_button.name.replace(input_button.prompt, ''))
            output = round(model.predict_y(amount_ghg), 2)

        output_button = input_button.output_button
        output_button.update_name(f'Bird Population Change(From 1970): {output} %')

    def draw(self, screen: pygame.Surface) -> None:
        """Draws images onto the screen, displaying all visual aspects."""
        page = self.pages[self.current_page]
        # Draw background
        screen.blit(page.background, (0, 0))
        # Draw buttons to screen
        for button in page.buttons:
            if button.image is not None:
                screen.blit(button.image, button.rect)
            screen.blit(button.text, button.rect)
            # Draw highlights if mouse is hovering over button
            if button.tag not in ('display', 'output') and \
                    button.rect.collidepoint(self.mouse_pos):
                surf = create_trans_surf(button.rect.width, button.rect.height, 50, (100, 255, 100))
                screen.blit(surf, button.rect)

    def _handle_key_press(self, event: pygame.event.Event) -> None:
        """Finds which key is pressed and updates input button."""
        if event.key == K_0:
            self._update_input('0')
        elif event.key == K_1:
            self._update_input('1')
        elif event.key == K_2:
            self._update_input('2')
        elif event.key == K_3:
            self._update_input('3')
        elif event.key == K_4:
            self._update_input('4')
        elif event.key == K_5:
            self._update_input('5')
        elif event.key == K_6:
            self._update_input('6')
        elif event.key == K_7:
            self._update_input('7')
        elif event.key == K_8:
            self._update_input('8')
        elif event.key == K_9:
            self._update_input('9')
        elif event.key == K_BACKSPACE:
            self._update_input('BACKSPACE')

    def _plot_graph(self) -> None:
        """Plots a graph based on current selections."""
        ghg_data, bird_data = self._datasets
        model = self._selection.get_model(ghg_data, bird_data)
        model.plot_data('Percent Change in Bird population (from 1970) vs '
                        'Amount of Greenhouse gas produced in a year',
                        'Amount of Greenhouse gas produced in a year (kt)',
                        'Percent Change in Bird population (from 1970)')

    def _update_ghg_coefs(self) -> None:
        """Updates the names of buttons that display the greenhouse gases'
        multiple regression coefficients.
        """
        ghg_data, bird_data = self._datasets
        model = self._selection.get_model(ghg_data, bird_data)
        page = self.pages[self.current_page]
        for button in page.buttons:
            if button.tag == 'display':
                gas = button.name[0:3]
                weight = '{:.2e}'.format(model.coef[gas])
                button.update_name(f'{gas} Weight: {weight}')

    def _clear_all_input(self) -> None:
        """Sets all inputs to 0."""
        page = self.pages[self.current_page]
        for button in page.buttons:
            if isinstance(button, InputButton):
                button.update_name(button.prompt + '0')

    def _update_input(self, character: str) -> None:
        """Updates button that shows user input.

        Changes button name to be displayed according to user input.
        """
        button = self._focused_button
        input_so_far = list(button.name.replace(button.prompt, ''))
        if character == 'BACKSPACE' and len(input_so_far) > 1:
            input_so_far.pop()
        elif character == 'BACKSPACE' and len(input_so_far) == 1:
            input_so_far[0] = '0'
        elif character != 'BACKSPACE' and input_so_far[0] == '0':
            input_so_far[0] = character
        elif character != 'BACKSPACE':
            input_so_far.append(character)

        button.update_name(button.prompt + ''.join(input_so_far))

    def _get_multiple_regression_inputs(self) -> List[float]:
        """Returns a list of all of the gases to the quantities of gas the user inputted
        for the multiple regression.
        """
        list_so_far = []
        page = self.pages[self.current_page]

        for button in page.buttons:
            if isinstance(button, InputButton):
                amount = float(button.name.replace(button.prompt, ''))
                list_so_far.append(amount)

        return list_so_far


def create_trans_surf(width: int, height: int, transparency: int, colour: tuple) -> pygame.Surface:
    """Returns a transparent surface to highlight things."""
    surf = pygame.Surface((width, height))
    surf.set_alpha(transparency)
    surf.fill(colour)

    return surf


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
