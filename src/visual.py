## 
#  @file simulation.py
#  @brief File containing the class *Visual*.
#  @date 2024-10-05
#  @author Rabyte Studio

import pygame
from config import Config

from map import Map
from food import Food
from entity import Entity

# Colors
COLOR_WHITE =  (0xFF, 0xFF, 0xFF)
COLOR_BLACK =  (0x00, 0x00, 0x00)
COLOR_RED   =  (0xFF, 0x00, 0x00)
COLOR_GREEN =  (0x00, 0xFF, 0x00)
COLOR_BLUE  =  (0x00, 0x00, 0xFF)

COLOR_BACKGROUND = COLOR_WHITE
COLOR_FOODS = COLOR_GREEN
COLOR_ENTITIES = COLOR_BLUE
COLOR_PAUSE = COLOR_RED
COLOR_SAVE = COLOR_RED

DEFAULT_CELL_SIZE = 5
MAX_CELL_SIZE = 50
DEFAULT_CAMERA = (0, 0)
DELTA_CAMERA = 5


## 
#  @class Visual
#  @brief Class that allows you to manage the visual aspect of the simulator.
class Visual:
    ## 
    #  @brief Initializes the Visual class and sets up the display.
    #
    #  This constructor initializes Pygame, sets the window size and caption, 
    #  and initializes camera and cell size variables. It also prepares for mouse 
    #  dragging events.
    def __init__(self):
        # Initialize pygame
        pygame.init()

        self.screen = pygame.display.set_mode((Config.visual.window_width, Config.visual.window_height), pygame.RESIZABLE)
        pygame.display.set_caption(Config.visual.window_name)

        self.clock = pygame.time.Clock()

        self.camera_x = DEFAULT_CAMERA[0]
        self.camera_y = DEFAULT_CAMERA[1]

        self.cell_size = DEFAULT_CELL_SIZE

        # Variables for mouse dragging
        self.dragging = False
        self.last_mouse_pos = (0, 0)

        self.time = 0

    ## 
    #  @brief Closes the Pygame window and quits the application.
    #
    #  This method should be called to properly close the Pygame environment
    #  and release resources.
    def close(self):
        pygame.quit()

    ## 
    #  @brief Handles camera movement.
    #
    #  This method is currently empty and can be filled in with logic to 
    #  manage camera movement based on user input, allowing for free movement.
    def camera(self):
        # Remove clamping; allow free movement
        pass

    ## 
    #  @brief Handles mouse scroll events for adjusting cell size.
    #
    #  This method modifies the cell size based on mouse wheel scroll events.
    #
    #  @param event The Pygame event to handle.
    def handle_mouse_scroll(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                if self.cell_size < MAX_CELL_SIZE:
                    self.cell_size = min(MAX_CELL_SIZE, self.cell_size + 1)
            elif event.button == 5:  # Scroll down
                if self.cell_size > 1:  # Ensure it doesn't go below 1
                    # Apply new cell size
                    self.cell_size = max(1, self.cell_size - 1)

    ## 
    #  @brief Handles mouse drag events to move the camera.
    #
    #  This method updates the camera position based on mouse movement while 
    #  dragging with the left mouse button.
    #
    #  @param event The Pygame event to handle.
    def handle_mouse_drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.dragging = True
                self.last_mouse_pos = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - self.last_mouse_pos[0]
                dy = mouse_y - self.last_mouse_pos[1]
                self.camera_x -= dx  # Move camera based on mouse motion
                self.camera_y -= dy
                self.last_mouse_pos = (mouse_x, mouse_y)

    ## 
    #  @brief Draws the background of the simulation.
    #
    #  This method fills the screen with the background color and draws the 
    #  boundaries of the map.
    def _draw_background(self):
        self.screen.fill(COLOR_BLACK)
        pygame.draw.rect(self.screen, COLOR_BLACK, (-1 - self.camera_x, -1 - self.camera_y, self.cell_size * Map.size[0], self.cell_size * Map.size[1]), 1)
        pygame.draw.rect(self.screen, COLOR_BACKGROUND, (-1 - self.camera_x, -1 - self.camera_y, self.cell_size * Map.size[0], self.cell_size * Map.size[1]))

    ## 
    #  @brief Draws food items on the screen.
    #
    #  This method iterates through the list of food items and draws them 
    #  at their respective positions.
    def _draw_foods(self):
        for food in Food.list:
            pygame.draw.rect(self.screen, COLOR_FOODS, (food.x * self.cell_size - self.camera_x, food.y * self.cell_size - self.camera_y, self.cell_size, self.cell_size))

    ## 
    #  @brief Draws entities on the screen.
    #
    #  This method iterates through the list of entities and draws them 
    #  at their respective positions.
    def _draw_entities(self):
        for entity in Entity.list:
            pygame.draw.rect(self.screen, COLOR_ENTITIES, (entity.x * self.cell_size - self.camera_x, entity.y * self.cell_size - self.camera_y, self.cell_size, self.cell_size))

    ## 
    #  @brief Displays the entire visual representation of the simulation.
    #
    #  This method calls the background, food, and entity drawing methods 
    #  to render the current state of the simulation on the screen.
    def show(self):
        self._draw_background()
        self._draw_foods()
        self._draw_entities()

    ## 
    #  @brief Displays a pause message on the screen.
    #
    #  This method renders a pause message when the simulation is paused.
    def pause(self):
        height = Config.visual.window_height // 30
        pause_text = pygame.font.SysFont(None, height).render("▮▮ Pause...", True, COLOR_PAUSE)
        self.screen.blit(pause_text, (10, 10))

    ## 
    #  @brief Displays a saving message on the screen.
    #
    #  This method renders a "Saving..." message during save operations, 
    #  positioned at the bottom right corner of the window.
    #
    #  @param duration The duration of the saving operation.
    #  @return The duration parameter for potential use elsewhere.
    def save(self, duration):
        height = Config.visual.window_height // 30
        save_text = pygame.font.SysFont(None, height).render("Saving...", True, COLOR_SAVE)
        
        # Retrieve text dimensions
        text_rect = save_text.get_rect()
        
        # Calculate position to place it at bottom right
        text_x = Config.visual.window_width - text_rect.width - 10  # 10 pixels margin right
        text_y = Config.visual.window_height - text_rect.height - 10  # 10 pixels margin bottom
        
        # Position the text rectangle
        text_rect.topleft = (text_x, text_y)
        
        # Render text to the screen
        self.screen.blit(save_text, text_rect)
        return duration
