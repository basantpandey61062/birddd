"""
Main

Module to with a function to run the main program.
"""

import pygame
from interface_objects import InputButton
from interface_system import InterfaceSystem
from read_data import read_bird_data, read_ghg_data


def run(i_system: InterfaceSystem) -> None:
    """Runs the main program allowing the user to use the program."""
    pygame.init()

    # Set up screen
    screen = pygame.display.set_mode((960, 720))
    pygame.display.set_caption('CSC110 Final Project')

    # Program Loop
    while True:
        i_system.mouse_clicked = False
        page = i_system.pages[i_system.current_page]

        # Handling events
        i_system.handle_events()

        # Handles mouse motion and selection
        for button in page.buttons:
            if button.rect.collidepoint(i_system.mouse_pos) \
                    and i_system.mouse_clicked:
                i_system.handle_mouse_click(button)

            # Updates output displayed
            if isinstance(button, InputButton):
                i_system.update_output(button)

        # Draws to screen
        i_system.draw(screen)

        # Updates screen
        pygame.display.update()


if __name__ == '__main__':
    ghg_data = read_ghg_data(398)
    bird_data = read_bird_data()
    interface_system = InterfaceSystem(ghg_data, bird_data)
    run(interface_system)
