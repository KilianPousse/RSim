
##
#  @file food.py
#  @brief File containing the class *Food*
#  @date 2024-10-04
#  @author Rabyte Studio

from element import Element
from map import Map

##
#  @class Food
#  @brief Class representing food objects in the simulation.
#  
#  This class inherits from Element and represents food items placed on the map. Each food object has a
#  position and a point value (`pts`), which is the energy it provides when consumed.
#
class Food(Element):

    NBYTES_PTS = 2  ##< Number of bytes allocated for food points.
    
    PTS_MAX = 2**(NBYTES_PTS*8)  ##< Maximum point value a food item can have.
    PTS_DEFAULT = 100  ##< Default point value for new food items.

    list = []  ##< Class-level list to store all food items.

    MAXFOODS_DEF = 50
    maxFoods = MAXFOODS_DEF

    ##
    #  @brief Initializes a new food object with coordinates and point value.
    #  @param coord A tuple (x, y) representing the coordinates of the food item on the map.
    #  @param pts An integer representing the energy value of the food, default is 100.
    def __init__(self, coord, pts=PTS_DEFAULT):
        super().__init__(coord)
        self.pts = pts

    ##
    #  @brief Represents the Food object as a string.
    #  @return A string representation of the food's coordinates and points.
    def __repr__(self) -> str:
        return f"<Food: {super().__repr__()}, pts={self.pts}>"
    
    ##
    #  @brief Property getter for the point value.
    #  @return The point value (`pts`) of the food.
    @property
    def pts(self):
        return self._pts

    ##
    #  @brief Property setter for the point value.
    #  @param value New point value for the food.
    #  @throws TypeError if the point value is not an integer.
    #  @details Clamps the point value between 1 and PTS_MAX. If the value is out of bounds,
    #  the default point value is used.
    @pts.setter
    def pts(self, value):
        if not isinstance(value, int):
            raise TypeError(f"pts must be an integer!")
        if not (0 < value <= Food.PTS_MAX):
            self._pts = Food.PTS_DEFAULT
        else:
            self._pts = value

    ##
    #  @brief Creates a new food object and adds it to the list.
    #  @param coord A tuple (x, y) representing the coordinates of the food.
    #  @param pts The point value of the food.
    #  @return The number of food items in the list after addition.
    @classmethod
    def new(cls, coord, pts):
        # Create an instance of Food
        food = cls(coord, pts)
        cls.list.append(food)
        return cls.len()
    
    ##
    #  @brief Generates a new food object at a random map coordinate.
    #  If a valid coordinate is found, a new food item is created and added to the list.
    @classmethod
    def generate(cls):
        if cls.len() < cls.maxFoods:
            coord = Map.rmdCoord(cls.list)
            if coord:
                cls.new(coord, cls.PTS_DEFAULT)


if __name__ == "__main__":
    Map.size = (5, 5)
    
    while True:
        Food.generate()
        print(Food.list)