"""
Interface System
"""

import pygame
import sys
from pygame.locals import *
from interface_objects import Button, InputButton, Page, Selection
from system_constants import create_pages
from typing import List, Optional


class InterfaceSystem:
    """Class to hold all objects for the main program.

    Instance Attributes:
        - pages: a list holding all the Page objects in the program
        - current_page: a number indicating which page is currently displayed
        - mouse_x: the x coordinate of the mouse
        - mouse_y: the y coordinate of the mouse
        - mouse_clicked: whether the mouse is clicked or not
        - selection: holds the region, bird, and gas chosen by the user
        - typing: whether the user can type or not
        - focused_button: the button the user is typing on
    """
    pages: List[Page]
    current_page: int
    mouse_x: int
    mouse_y: int
    mouse_clicked: bool
    selection: Selection
    typing: bool
    focused_button: Optional[InputButton] = None

    def __init__(self) -> None:
        self.pages = create_pages()
        self.current_page = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_clicked = False
        self.selection = Selection()
        self.typing = False
        self.focused_button = None

    def handle_events(self) -> None:
        """Handles the events the pygame receives(handles mouse movement, mouse clicking
        and typing).
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                self.mouse_x, self.mouse_y = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = event.pos
                self.mouse_clicked = True
            elif self.typing and event.type == KEYDOWN:
                if event.key == K_0:
                    self.update_input('0')
                elif event.key == K_1:
                    self.update_input('1')
                elif event.key == K_2:
                    self.update_input('2')
                elif event.key == K_3:
                    self.update_input('3')
                elif event.key == K_4:
                    self.update_input('4')
                elif event.key == K_5:
                    self.update_input('5')
                elif event.key == K_6:
                    self.update_input('6')
                elif event.key == K_7:
                    self.update_input('7')
                elif event.key == K_8:
                    self.update_input('8')
                elif event.key == K_9:
                    self.update_input('9')
                elif event.key == K_BACKSPACE:
                    self.update_input('BACKSPACE')

    def handle_mouse_click(self, button: Button) -> None:
        """Tells program what to do based on what the mouse clicks."""
        if button.name == 'BACK':
            self.clear_all_input()
            self.current_page -= 1
            self.typing = False
            if self.current_page == len(self.pages) - 2:
                self.current_page -= 1
        elif button.name == 'Show Graph':
            self.plot_graph()
        elif button.name == 'Multiple Regression':
            self.selection.handle_selection(self.current_page, button.name)
            self.current_page += 2
        elif button.tag == 'normal' and self.current_page < len(self.pages) - 2:
            self.selection.handle_selection(self.current_page, button.name)
            self.current_page += 1
        elif isinstance(button, InputButton):
            self.typing = True
            self.focused_button = button

    def plot_graph(self) -> None:
        """Plots a graph based on current selections."""
        model = self.selection.get_model()
        model.plot_data('Test', 'x', 'y')

    def update_ghg_coefs(self) -> None:
        """Updates the names of buttons that display the greenhouse gases'
        multiple regression coefficients.
        """
        page = self.pages[self.current_page]
        for button in page.buttons:
            if button.tag == 'display':
                ...

    def clear_all_input(self) -> None:
        """Sets all inputs to 0."""
        page = self.pages[self.current_page]
        for button in page.buttons:
            if isinstance(button, InputButton):
                button.name = button.prompt + '0'
                button.update_text()

    def update_input(self, character: str) -> None:
        """Updates button that shows user input.

        Changes button name to be displayed according to user input.
        """
        button = self.focused_button
        input_so_far = list(button.name.replace(button.prompt, ''))
        if character == 'BACKSPACE' and len(input_so_far) > 1:
            input_so_far.pop()
        elif character == 'BACKSPACE' and len(input_so_far) == 1:
            input_so_far[0] = '0'
        elif character != 'BACKSPACE' and input_so_far[0] == '0':
            input_so_far[0] = character
        elif character != 'BACKSPACE':
            input_so_far.append(character)

        button.name = button.prompt + ''.join(input_so_far)
        button.update_text()

    def update_output(self, input_button: InputButton) -> None:
        """Updates button that shows predicted output from user's input.

        Gets input from the input button's name, gets the corresponding output, and changes
        the output button's name accordingly to be displayed.
        """
        model = self.selection.get_model()

        # Handles multiple regression page
        if self.current_page == len(self.pages) - 1:
            amounts_ghg = self.get_multiple_regression_inputs()
            output = round(model.predict_value(amounts_ghg[0], amounts_ghg[1], amounts_ghg[2],
                                               amounts_ghg[3], amounts_ghg[4], amounts_ghg[5],
                                               amounts_ghg[6]), 2)
        # Handles single variable prediction
        else:
            amount_ghg = float(input_button.name.replace(input_button.prompt, ''))
            output = round(model.predict_y(amount_ghg), 2)

        output_button = input_button.output_button
        output_button.name = f'Bird Population Change(From 1970): {output} %'
        output_button.update_text()

    def get_multiple_regression_inputs(self) -> List[float]:
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
            if button.tag not in ('display', 'output') and button.rect.collidepoint(self.mouse_x, self.mouse_y):
                surf = create_trans_surf(button.rect.width, button.rect.height, 50, (100, 255, 100))
                screen.blit(surf, button.rect)


def create_trans_surf(width: int, height: int, transparency: int, colour: tuple) -> pygame.Surface:
    """Create a transparent surface to highlight things."""
    surf = pygame.Surface((width, height))
    surf.set_alpha(transparency)
    surf.fill(colour)

    return surf
