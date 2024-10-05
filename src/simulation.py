## 
#  @file simulation.py
#  @brief File containing the class *RSim*, responsible for running the simulation of the environment.
#  @date 2024-10-04
#  @author Rabyte Studio

from map import Map
from save import Save
from entity import Entity
from food import Food
from visual import Visual, MAX_CELL_SIZE
from config import Config
import path
import pygame
from cmd import Cmd

## 
#  @class RSim
#  @brief Class managing the main simulation loop and environment interactions.
#  @details This class handles the initialization, running, and stepping of the simulation.
class RSim(Cmd):

    FPS_DEFAULT = 180  ##< Default frames per second for the simulation.

    save = None  ##< Instance of the Save class for managing save operations.
    visual = None  ##< Instance of the Visual class for rendering the simulation.

    _fps = FPS_DEFAULT  ##< Current frames per second setting.

    _running = False  ##< Flag indicating if the simulation is currently running.
    _pause = False  ##< Flag indicating if the simulation is paused.
    mouse_clicking = False  ##< Flag for mouse clicking state.

    save_duration = 0  ##< Duration for displaying save messages.

    verbose = False

    ## 
    #  @brief Initializes the simulation environment.
    #  @param numSave Number of saves to initialize (default is 0).
    #  @param size Size of the map (default is Map.DEFAULT_SIZE).
    #  @details Sets up the configuration, map size, and initializes save and visual components.
    @classmethod
    def init(cls, numSave=0, size=Map.DEFAULT_SIZE):
        Config.init()
        Map.size = size
        cls.save = Save(numSave)
        cls.visual = Visual()
        cls._running = False

        # Calculate the maximum number of foods based on the map size.
        Food.maxFoods = (Map.size[0] * Map.size[1]) // 9

    ##
    #  @brief Generates a specified number of entities and food items.
    #
    #  This class method creates the specified number of entities and food items 
    #  by calling their respective `generate()` methods.
    #
    #  @param nEntities The number of entities to generate.
    #  @param nFoods The number of food items to generate.
    #
    #  @details
    #  - The method iterates over the range `nEntities` and generates an entity for each iteration.
    #  - Similarly, it iterates over the range `nFoods` to generate food items.
    #
    @classmethod
    def generate(self, nEntities: int, nFoods: int):
        for _ in range(nEntities):
            Entity.generate()
        for _ in range(nFoods):
            Food.generate()

    ## 
    #  @brief Executes a single simulation step.
    #  @details Moves all entities, checks their survival, and generates new food.
    @classmethod
    def step(cls):
        for entity in Entity.list:
            entity.move()  ## Move the entity.
            if not entity.survive():  ## Check if the entity is alive.
                Entity.delete(entity)  ## Remove dead entities.

        cls.save.time += 1  ## Increment the simulation time.
        Food.generate()  ## Generate new food items.

    ## 
    #  @brief Runs the main simulation loop.
    #  @details Handles user input, updates simulation state, and renders visuals.
    @classmethod
    def run(cls):
        cls._running = True
        dragging = False  ## Flag to indicate if the user is dragging the mouse.
        last_mouse_pos = (0, 0)  ## Store the last mouse position.
        tempPause = cls._pause  ## Temporarily store the pause state.

        cls.startCmd()        

        while cls._running:
            # Handle events (e.g., closing the window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cls._running = False  ## Exit the simulation.

                if event.type == pygame.VIDEORESIZE:
                    Config.visual.window_width = event.w
                    Config.visual.window_height = event.h

                if event.type == pygame.KEYDOWN:  # Check for key press
                    if event.key == pygame.K_SPACE:  # Toggle pause
                        cls._pause = not cls._pause

                    if event.key == pygame.K_s:  # Save
                        cls.save.save()
                        cls.save_duration = 60  ## Set duration for save message display.

                # Detect mouse button down for dragging
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        tempPause = cls._pause
                        dragging = True
                        last_mouse_pos = pygame.mouse.get_pos()
                        cls._pause = True  # Pause the simulation

                # Detect mouse button up
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left mouse button
                        dragging = False
                        cls._pause = tempPause

                # Detect mouse scroll events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4 or event.button == 5: 
                        cls.visual.handle_mouse_scroll(event)

            # Handle camera movement while dragging
            if dragging:
                current_mouse_pos = pygame.mouse.get_pos()
                dx = current_mouse_pos[0] - last_mouse_pos[0]
                dy = current_mouse_pos[1] - last_mouse_pos[1]

                # Update camera position
                cls.visual.camera_x -= dx
                cls.visual.camera_y -= dy

                last_mouse_pos = current_mouse_pos  # Update last mouse position

            # Check which keys are currently pressed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                cls.visual.camera_x += cls.visual.cell_size
            if keys[pygame.K_LEFT]:
                cls.visual.camera_x -= cls.visual.cell_size
            if keys[pygame.K_DOWN]:
                cls.visual.camera_y += cls.visual.cell_size
            if keys[pygame.K_UP]:
                cls.visual.camera_y -= cls.visual.cell_size

            cls.visual.camera()  ## Update camera view.

            # Manage save message duration
            if cls.save_duration > 0:
                cls.save_duration -= 1

            if not cls._pause and ((cls.visual.time % int(cls._fps*0.1)) == 0):
                cls.step()  ## Execute a simulation step if not paused.
            
            # Render visuals
            cls.visual.show()

            if cls._pause:
                cls.visual.pause()  ## Display pause screen.
            if cls.save_duration > 0:
                cls.visual.save(cls.save_duration)  ## Show save message.

            pygame.display.flip()  ## Update the display.

            # Control frame rate
            cls.visual.time += 1
            cls.visual.clock.tick(cls._fps)  ## Limit the frame rate.

        
        cls.processCmd("")
        cls.visual.close()  ## Close visual components when done.
        cls.stopCmd()

if __name__ == "__main__":
    RSim.init()
    RSim.run()
