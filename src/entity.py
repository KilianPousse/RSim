## 
#  @file entity.py
#  @brief File containing the class *Entity*.
#  @date 2024-10-03
#  @author Rabyte Studio

from element import Element
from map import Map
from food import Food
from random import choices, randint
from math import log, exp

## 
#  @class Entity
#  @brief Class representing an entity that extends *Element* and includes properties for energy, time, and age.
class Entity(Element):

    NBYTES_ID = 2
    NBYTES_ENERGY = 2  ##< Number of bytes for energy in the binary representation.
    NBYTES_TIME = 2    ##< Number of bytes for time in the binary representation.

    ENERGY_MAX = 9999  ##< Maximum possible energy value for an entity.
    ENERGY_DEF = 200   ##< Default energy value when an entity is generated.
    TIME_MAX = 4000    ##< Maximum possible time value for an entity.

    RANGE_DEF = 10     ##< Default viewing range for the entity.

    list = []  ##< Class-level list to store all instances of Entity.

    nEntities = 0
    MAX_ID = 2 ** (NBYTES_ID * 8)

    TIME_IN_AGE = 40

    AGE_REPROD = range(18, 60)
    MIN_REPROD = 500
    REPROD = 200

    _ln_10 = log(10)

    ## 
    #  @brief Initializes an entity with a position, energy, and time.
    #  @param coord A tuple (x, y) representing the coordinates of the entity.
    #  @param energy An integer representing the initial energy of the entity.
    #  @param time An integer representing the time the entity has lived (default is 0).
    def __init__(self, coord, energy, time=0):
        super().__init__(coord)  # Initialize position from the Element class.
        self.energy = energy     # Set the entity's energy.
        self.time = time         # Set the entity's time.
        self.range = Entity.RANGE_DEF

        Entity.nEntities = Entity.nEntities + 1 if Entity.nEntities < Entity.MAX_ID else 1
        self.id = Entity.nEntities

    ## 
    #  @brief Returns a string representation of the entity, including its position, energy, time, and age.
    #  @return A string in the format "pos=(x, y), energy=..., time=..., age=...".
    def __repr__(self) -> str:
        return f"<Entity #{self.id:04X}: "+super().__repr__() + f", energy={self.energy}, time={self.time}, age={self.age}>"

    ## 
    #  @brief Property getter for the entity's energy.
    #  @return The current energy of the entity.
    @property
    def energy(self):
        return self._energy

    ## 
    #  @brief Property setter for energy.
    #  @param value New energy value for the entity.
    #  @throws TypeError if energy is not an integer.
    #  @details Clamps the energy to [0, ENERGY_MAX] if the input exceeds those limits.
    @energy.setter
    def energy(self, value):
        if not isinstance(value, int):
            raise TypeError("energy must be an integer!")
        if value > Entity.ENERGY_MAX:
            self._energy = Entity.ENERGY_MAX
        elif value < 0:
            self._energy = 0
        else:
            self._energy = value

    ## 
    #  @brief Property getter for time.
    #  @return The current time value of the entity.
    @property
    def time(self):
        return self._time

    ## 
    #  @brief Property setter for time.
    #  @param value New time value for the entity.
    #  @throws TypeError if time is not an integer.
    #  @details Sets time; if time is invalid, resets it to -1 and sets energy and age to default values.
    @time.setter
    def time(self, value):
        if not isinstance(value, int):
            raise TypeError("time must be an integer!")
        if value not in range(Entity.TIME_MAX):
            self._time = -1
            self._energy = 0
            self._age = 0  
        else:
            self._time = value
            self._age = self.time // Entity.TIME_IN_AGE  # Calculate age based on time.

    ## 
    #  @brief Property getter for age.
    #  @return The age of the entity, calculated from the time.
    @property
    def age(self):
        return self._age

    ## 
    #  @brief Class method to create a new entity and add it to the class list.
    #  @param coord A tuple (x, y) representing the coordinates of the new entity.
    #  @param energy Initial energy value of the new entity.
    #  @param time Initial time value of the new entity (default is 0).
    #  @return The total number of entities after adding the new one.
    @classmethod
    def new(cls, coord, energy, time=0):
        entity = cls(coord, energy, time)
        cls.list.append(entity)
        return cls.len()

    ## 
    #  @brief Class method to generate an entity at a random position.
    #  @details Uses the Map class to generate a random coordinate and creates a new entity with default energy.
    @classmethod
    def generate(cls):
        coord = Map.rmdCoord()
        cls.new(coord, cls.ENERGY_DEF)
    
    ## 
    #  @brief Allows the entity to eat food located at the same coordinates.
    #  @details This method checks if the entity's energy is less than the maximum energy.
    #  If food is found at the same location, the entity consumes it, increasing its energy.
    def eat(self):
        if self.energy < self.ENERGY_MAX:
            # Find food at the current coordinates
            food_at_location = next((food for food in Food.list if food.x == self.x and food.y == self.y), None)
            if food_at_location:
                # Eat the food and remove it from the list
                self.energy = min(self.ENERGY_MAX, self.energy + food_at_location.pts)
                Food.list.remove(food_at_location)

    ## 
    #  @brief Determines possible moves based on the entity's position and the map size.
    #  @return A list of valid neighboring coordinates.
    def possibleMoves(self):
        size_x, size_y = Map.size
        x, y = self.x, self.y
        return [
            (dx, dy)
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if  0 <= x + dx < size_x 
            and 0 <= y + dy < size_y
        ]

    ## 
    #  @brief Randomly move the entity to a neighboring position.
    #  @return A tuple of (dx, dy) representing the movement direction.
    def rdmMove(self) -> tuple:
        dx, dy = choices(self.possibleMoves())[0]
        self.x += dx
        self.y += dy
        return (dx, dy)

    ## 
    #  @brief Move the entity by choosing a random valid direction or towards food.
    #  @details The entity will first try to eat if food is available, then move towards food if it is nearby. 
    #  If no food is found, it makes a random move.
    def move(self):
        # Decrease energy, ensuring it does not go below 0
        self.energy = max(0, self.energy - 1)

        self.time += 1

        # Try to eat food first
        self.eat()

        self.reproduction()

        # Attempt to move towards food
        move = self.moveTowardsFood()
        if move is None:
            # Make a random move if no food is nearby
            self.rdmMove()
    
    ## 
    #  @brief Finds and moves towards the closest food within the entity's viewing range.
    #  @details Searches the `Food.list` for the closest food that is within `self.range` of the entity.
    #  If no food is found, the entity does not move.
    #  @return A tuple of (dx, dy) representing the movement direction, or None if no food is found.
    def moveTowardsFood(self):
        closest_food = None
        min_distance = float('inf')

        # Search through the food list.
        for food in Food.list:
            dist = self.distance(food)  # Ensure this distance function is valid

            # Check if the food is within the entity's range.
            if dist <= self.range and dist < min_distance:
                closest_food = food
                min_distance = dist

        # If food is found within range, move towards it.
        if closest_food:
            
            # Accessing coord property (no need for parentheses)
            x = closest_food.x  
            y = closest_food.y 
            
            dx = x - self.x
            dy = y - self.y

            # Normalize the movement to move only one step per movement.
            if dx != 0:
                dx = int(dx / abs(dx))
            if dy != 0:
                dy = int(dy / abs(dy))

            # Update the entity's position.
            self.x += dx
            self.y += dy

            return (dx, dy)  # Return the movement direction.
        else:
            # No food found within range.
            return None
    

    def reproduction(self):
        if self.age in Entity.AGE_REPROD and self.energy >= Entity.MIN_REPROD:
            self.energy -= Entity.REPROD
            Entity.new( (self.x, self.y), Entity.ENERGY_DEF )

    

    def survive(self) -> bool:
        if self.energy <= 0 or self.age > Entity.TIME_MAX :
            return False
        return True
    


            
if __name__ == "__main__":
    Map.size = Map.DEFAULT_SIZE
    for _ in range(10):
        Entity.generate()
        print(Entity.list[-1])
    
    Entity.list[0].move()
    print(Entity.list[0])







