"""
Constant values
"""

import pygame
from typing import List
from interface_objects import Button, InputButton, Page
pygame.init()

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720
GRID_LENGTH = 3
IMG_SIZE = 200
X_MARGIN = (WINDOW_WIDTH - GRID_LENGTH * IMG_SIZE) // 2
Y_MARGIN = (WINDOW_HEIGHT - GRID_LENGTH * IMG_SIZE) // 2
GRID_BOX_SIZE = (WINDOW_WIDTH - X_MARGIN * 2) // GRID_LENGTH
SMALL_FONT = pygame.font.SysFont('arial', 20)
LARGE_FONT = pygame.font.SysFont('arial', 40)


def create_pages() -> List[Page]:
    """Creates the Page objects for the system.

    First gets images, then creates buttons, then creates pages.
    """
    # Images
    canada_map_img = pygame.transform.scale(pygame.image.load('images/canada_map.jpg'),
                                            (WINDOW_WIDTH, WINDOW_HEIGHT))
    grass_img = pygame.transform.scale(pygame.image.load('images/grass.jpeg'),
                                       (WINDOW_WIDTH, WINDOW_HEIGHT))
    sky_img = pygame.transform.scale(pygame.image.load('images/sky.jpg'),
                                     (WINDOW_WIDTH, WINDOW_HEIGHT))

    image_files = ['waterfowl.jpg', 'birds_of_prey.jpg', 'wetland_birds.jpg', 'seabirds.jpg',
                   'forest_birds.jpg', 'shorebirds.jpg', 'grassland_birds.jpg', 'aerial_insectivores.jpg',
                   'all_other_birds.png']
    bird_images = [pygame.transform.scale(pygame.image.load(f'images/{image_file}'), (IMG_SIZE, IMG_SIZE))
                   for image_file in image_files]

    # Button objects
    back = Button('normal', 'BACK', LARGE_FONT)

    # Bird Buttons
    bird_names = ['Waterfowl', 'Birds of Prey', 'Wetland Birds', 'Seabirds', 'Forest Birds', 'Shorebirds',
                  'Grassland Birds', 'Aerial Insectivores', 'All Other Birds']
    all_birds = [Button('normal', bird_names[i], SMALL_FONT, bird_images[i])
                 for i in range(len(bird_names))]

    # Region Buttons
    region_names = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador',
                    'Northwest Territories', 'Nova Scotia', 'Nunavut', 'Ontario', 'Prince Edward Island',
                    'Quebec', 'Saskatchewan', 'Yukon', 'Canada']
    all_regions = [Button('normal', region, SMALL_FONT) for region in region_names]

    # GHG Buttons
    total = Button('normal', 'Total', LARGE_FONT)
    multiple_regression = Button('normal', 'Multiple Regression', SMALL_FONT)

    ghg_names = ['CO2', 'CH4', 'N2O', 'HFC', 'PFC', 'SF6', 'NF3']
    all_ghgs = [Button('normal', ghg, LARGE_FONT) for ghg in ghg_names] + [total, multiple_regression]

    # Page 3 Buttons
    bird_index_output = Button('output', 'Bird Population Change (From 1970): 0 %', LARGE_FONT)
    ghg_input = InputButton('input', 'Amount of Gas (kt): ', LARGE_FONT, bird_index_output)
    show_graph = Button('normal', 'Show Graph', SMALL_FONT)

    page3_buttons = [ghg_input, bird_index_output, show_graph, back]

    # Page 4 Buttons
    multiple_regression_output = Button('output', 'Bird Population Change (From 1970): 0 %', LARGE_FONT)

    all_ghg_input = [InputButton('input', f'{ghg} (kt): ', SMALL_FONT, multiple_regression_output)
                     for ghg in ghg_names]
    all_ghg_coef = [Button('display', f'{ghg} Weight: ', SMALL_FONT) for ghg in ghg_names]

    # Page objects
    page0 = Page(canada_map_img, all_regions)
    page1 = Page(grass_img, all_birds + [back])
    page2 = Page(sky_img, all_ghgs + [back])
    page3 = Page(sky_img, page3_buttons)
    page4 = Page(sky_img, all_ghg_coef + all_ghg_input + [multiple_regression_output, back])

    # set up button coordinates
    back.rect.topleft = (10, 10)

    # page0
    region_coords = [(254, 487), (129, 463), (425, 510), (790, 561), (793, 411), (265, 343), (867, 609),
                     (463, 254), (532, 561), (817, 520), (678, 506), (335, 550), (124, 291), (50, 20)]
    for i in range(len(all_regions)):
        all_regions[i].rect.center = region_coords[i]

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

    # page3
    ghg_input.rect.topleft = (X_MARGIN, WINDOW_HEIGHT * 0.6)
    bird_index_output.rect.topleft = (X_MARGIN, WINDOW_HEIGHT * 0.4)
    show_graph.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.8)

    # page4
    count = 0
    for i in range(len(all_ghg_input)):
        all_ghg_input[i].rect.topleft = (X_MARGIN, WINDOW_HEIGHT * 0.4 + count * 30)
        all_ghg_coef[i].rect.topleft = (WINDOW_WIDTH // 2 + X_MARGIN,
                                        WINDOW_HEIGHT * 0.4 + count * 30)
        count += 1

    multiple_regression_output.rect.topleft = (X_MARGIN, WINDOW_HEIGHT * 0.3)

    return [page0, page1, page2, page3, page4]
