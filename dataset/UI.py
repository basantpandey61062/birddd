"""
CSC110 Final Project
"""

import pygame
import sys
from pygame.locals import *
import read_data
import regression
from typing import List, Optional


class Button:
    """Class to hold a bird's image and it's coordinates on the screen."""

    name: str
    text: pygame.Surface
    image: Optional[pygame.Surface] = None
    rect: pygame.Rect

    def __init__(self, name, font: pygame.font.Font, image: Optional[pygame.Surface] = None) -> None:
        self.name = name
        self.text = font.render(self.name, True, BLACK)
        self.image = image
        if image is not None:
            self.rect = self.image.get_rect()
        else:
            self.rect = self.text.get_rect()


class Page:
    """Class to hold a page with all it's buttons."""

    background: pygame.Surface
    buttons: List[Button]

    def __init__(self, background: pygame.Surface, buttons: List[Button]) -> None:
        self.background = background
        self.buttons = buttons


# '''
class Selection:
    """Class to store and handle user's selections."""
    # Private Instance Attributes
    #   _province: Optional[str] = None
    #   _bird: Optional[int] = None
    #   _ghg: Optional[int] = None
    
    def __init__(self) -> None:
        self._province = None
        self._bird = None
        self._ghg = None

    def handle_selection(self, current_page: int, selection: str) -> None:
        """Handles what selection the user chooses."""
        if current_page == 0:
            self.change_province(selection)
        elif current_page == 1:
            self.change_bird(selection)
        elif current_page == 2:
            self.change_ghg(selection)

    def get_model(self) -> regression.RegressionModel:
        """Returns RegressionModel for current selections."""
        # Reading and filtering data
        all_ghg_data = read_data.read_ghg_data(398)
        all_bird_data = read_data.read_bird_data()
        filtered_bird_data = read_data.filter_bird_data(all_bird_data, self._bird)

        # Creating class instances
        province = read_data.Province(all_ghg_data[self._province])
        bird = read_data.Bird(filtered_bird_data)
        bird.trim_data(1990, 2016)

        # Obtaining data in list form
        ghg_list = province.adjust_list(1990, 2016, self._ghg)
        bird_list = bird.list_data

        return regression.RegressionModel(ghg_list, bird_list)

    def interact(self) -> None:
        """Interacts with user input and plots data."""
        model = self.get_model()
        x = int(input('How many kt of gas?: '))
        y = model.predict_y(x)
        print(y)
        model.plot_data('Test', 'x', 'y')

    def change_province(self, province_name: str) -> None:
        """Changes province selection to selected province."""
        self._province = province_name

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
                    'Total': 7}
        self._ghg = ghg_dict[ghg_name]
# '''


def run_game() -> None:
    """Runs the program."""
    # Fonts
    small_font = pygame.font.SysFont('arial', 20)
    large_font = pygame.font.SysFont('arial', 40)

    # Images
    waterfowl_img = pygame.transform.scale(pygame.image.load('images/waterfowl.jpg'),
                                           (IMG_SIZE, IMG_SIZE))
    birds_of_prey_img = pygame.transform.scale(pygame.image.load('images/birds_of_prey.jpg'),
                                               (IMG_SIZE, IMG_SIZE))
    wetland_birds_img = pygame.transform.scale(pygame.image.load('images/wetland_birds.jpg'),
                                               (IMG_SIZE, IMG_SIZE))
    seabirds_img = pygame.transform.scale(pygame.image.load('images/seabirds.jpg'),
                                          (IMG_SIZE, IMG_SIZE))
    forest_birds_img = pygame.transform.scale(pygame.image.load('images/forest_birds.jpg'),
                                              (IMG_SIZE, IMG_SIZE))
    shorebirds_img = pygame.transform.scale(pygame.image.load('images/shorebirds.jpg'),
                                            (IMG_SIZE, IMG_SIZE))
    grassland_birds_img = pygame.transform.scale(pygame.image.load('images/grassland_birds.jpg'),
                                                 (IMG_SIZE, IMG_SIZE))
    aerial_insectivores_img = pygame.transform.scale(pygame.image.load('images/aerial_insectivores.jpg'),
                                                     (IMG_SIZE, IMG_SIZE))
    all_other_birds_img = pygame.transform.scale(pygame.image.load('images/all_other_birds.png'),
                                                 (IMG_SIZE, IMG_SIZE))
    canada_map_img = pygame.transform.scale(pygame.image.load('images/canada_map.jpg'),
                                            (WINDOW_WIDTH, WINDOW_HEIGHT))
    grass_img = pygame.transform.scale(pygame.image.load('images/grass.jpeg'),
                                       (WINDOW_WIDTH, WINDOW_HEIGHT))
    sky_img = pygame.transform.scale(pygame.image.load('images/sky.jpg'),
                                     (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Button objects
    back = Button('BACK', large_font)

    waterfowl = Button('Waterfowl', small_font, waterfowl_img)
    birds_of_prey = Button('Birds of Prey', small_font, birds_of_prey_img)
    wetland_birds = Button('Wetland Birds', small_font, wetland_birds_img)
    seabirds = Button('Seabirds', small_font, seabirds_img)
    forest_birds = Button('Forest Birds', small_font, forest_birds_img)
    shorebirds = Button('Shorebirds', small_font, shorebirds_img)
    grassland_birds = Button('Grassland Birds', small_font, grassland_birds_img)
    aerial_insectivores = Button('Aerial Insectivores', small_font, aerial_insectivores_img)
    all_other_birds = Button('All Other Birds', small_font, all_other_birds_img)

    all_birds = [waterfowl, birds_of_prey, wetland_birds, seabirds, forest_birds, shorebirds,
                 grassland_birds, aerial_insectivores, all_other_birds]

    alberta = Button('Alberta', small_font)
    british_colombia = Button('British Colombia', small_font)
    manitoba = Button('Manitoba', small_font)
    new_brunswick = Button('New Brunswick', small_font)
    newfoundland_and_labrador = Button('Newfoundland and Labrador', small_font)
    northwest_territories = Button('Northwest Territories', small_font)
    nova_scotia = Button('Nova Scotia', small_font)
    nunavut = Button('Nunavut', small_font)
    ontario = Button('Ontario', small_font)
    prince_edward_island = Button('Prince Edward Island', small_font)
    quebec = Button('Quebec', small_font)
    saskatchewan = Button('Saskatchewan', small_font)
    yukon = Button('Yukon', small_font)
    canada = Button('Canada', large_font)

    all_provinces = [alberta, british_colombia, manitoba, new_brunswick, newfoundland_and_labrador,
                     northwest_territories, nova_scotia, nunavut, ontario, prince_edward_island,
                     quebec, saskatchewan, yukon, canada]

    co2 = Button('CO2', large_font)
    ch4 = Button('CH4', large_font)
    n20 = Button('N2O', large_font)
    hfc = Button('HFC', large_font)
    pfc = Button('PFC', large_font)
    sf6 = Button('SF6', large_font)
    nf3 = Button('NF3', large_font)
    total = Button('Total', large_font)

    all_ghgs = [co2, ch4, n20, hfc, pfc, sf6, nf3, total]

    # Page objects
    page0 = Page(canada_map_img, all_provinces)
    page1 = Page(grass_img, all_birds + [back])
    page2 = Page(sky_img, all_ghgs + [back])
    page3 = Page(sky_img, [back])

    # set up button coordinates
    back.rect.topleft = (10, 10)

    # page0
    alberta.rect.center = (254, 487)
    british_colombia.rect.center = (129, 463)
    manitoba.rect.center = (416, 510)
    new_brunswick.rect.center = (790, 561)
    newfoundland_and_labrador.rect.center = (793, 411)
    northwest_territories.rect.center = (250, 327)
    nova_scotia.rect.center = (867, 609)
    nunavut.rect.center = (463, 254)
    ontario.rect.center = (532, 561)
    prince_edward_island.rect.center = (817, 520)
    quebec.rect.center = (678, 506)
    saskatchewan.rect.center = (323, 550)
    yukon.rect.center = (109, 291)
    canada.rect.topleft = (10, 10)

    # page1
    count = 0
    for i in range(len(all_birds)):
        all_birds[i].rect.center = ((X_MARGIN + GRID_BOX_SIZE * (count % GRID_LENGTH) + GRID_BOX_SIZE // 2),
                                    (Y_MARGIN + GRID_BOX_SIZE * (count // GRID_LENGTH) + GRID_BOX_SIZE // 2))
        count += 1

    # page2
    count = 0
    for i in range(len(all_ghgs)):
        all_ghgs[i].rect.center = ((X_MARGIN + GRID_BOX_SIZE * (count % GRID_LENGTH) + GRID_BOX_SIZE // 2),
                                   (Y_MARGIN + GRID_BOX_SIZE * (count // GRID_LENGTH) + GRID_BOX_SIZE // 2))
        count += 1

    all_pages = [page0, page1, page2, page3]
    current_page = 0

    # Set up screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('CSC110 Final Project')

    # Set up mouse coordinates
    mousex, mousey = 0, 0

    # Keeps track of the user's selections
    selection = Selection()

    # Program Loop
    while True:
        mouse_clicked = False
        page = all_pages[current_page]

        # Handling events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouse_clicked = True

        # Handles selections
        for button in page.buttons:
            if button.rect.collidepoint(mousex, mousey) and mouse_clicked and button == back:
                current_page -= 1
            elif button.rect.collidepoint(mousex, mousey) and mouse_clicked \
                    and current_page < len(all_pages) - 1:
                selection.handle_selection(current_page, button.name)
                current_page += 1

        # Handles input and prediction
        if current_page == 3:
            selection.interact()
            current_page -= 1

        # Draws to screen
        draw(screen, page, mousex, mousey)

        # Updates screen
        pygame.display.update()


def draw(screen: pygame.Surface, page: Page, mousex, mousey) -> None:
    """Draws images onto the screen"""
    # Draw background
    screen.blit(page.background, (0, 0))
    # Draw buttons to screen
    for button in page.buttons:
        if button.image is not None:
            screen.blit(button.image, button.rect)
        screen.blit(button.text, button.rect)
        # Draw highlights if mouse is hovering over button
        if button.rect.collidepoint(mousex, mousey):
            surf = create_trans_surf(button.rect.width, button.rect.height, 50, GREEN)
            screen.blit(surf, button.rect)


def create_trans_surf(width: int, height: int, transparency: int, colour: tuple) -> pygame.Surface:
    """Create a transparent surface to highlight things."""
    surf = pygame.Surface((width, height))
    surf.set_alpha(transparency)
    surf.fill(colour)

    return surf


if __name__ == '__main__':
    pygame.init()

    # Constants
    WINDOW_WIDTH = 960
    WINDOW_HEIGHT = 720
    GRID_LENGTH = 3
    IMG_SIZE = 200
    X_MARGIN = (WINDOW_WIDTH - GRID_LENGTH * IMG_SIZE) // 2
    Y_MARGIN = (WINDOW_HEIGHT - GRID_LENGTH * IMG_SIZE) // 2
    GRID_BOX_SIZE = (WINDOW_WIDTH - X_MARGIN * 2) // GRID_LENGTH

    GREEN = (100, 255, 100)
    BLACK = (0, 0, 0)

    run_game()
