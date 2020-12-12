"""
Main
"""

import pygame
from interface_objects import InputButton
from interface_system import InterfaceSystem
from system_constants import WINDOW_WIDTH, WINDOW_HEIGHT


def run(i_system: InterfaceSystem) -> None:
    """Runs the main program allowing the user to use the program."""
    pygame.init()

    # Set up screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('CSC110 Final Project')

    # Program Loop
    while True:
        i_system.mouse_clicked = False
        page = i_system.pages[i_system.current_page]

        # Handling events
        i_system.handle_events()

        # Handles mouse motion and selection
        for button in page.buttons:
            if button.rect.collidepoint(i_system.mouse_x, i_system.mouse_y) \
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
    interface_system = InterfaceSystem()
    run(interface_system)
